"""
Note: V 0.9.2 Originally, filling data methods was developed by Eric Alfaro and Javier Soley in SCILAB
      Python version was developed by Rolando Duarte and Erick Rivera
      Centro de Investigaciones Geofísicas (CIGEFI)
      Universidad de Costa Rica (UCR)
"""

"""
MIT License
Copyright 2021 Rolando Jesus Duarte Mejias and Erick Rivera Fernandez
Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from matplotlib.pyplot import errorbar, figure, xlabel, ylabel, title, show #Graphs
from numpy import sqrt, abs, max, delete, where, arange, all, dot, nan #Handling arrays
from pandas import read_csv, DataFrame, options #Handles datasets
from sklearn.decomposition import PCA #Applies principal components transformations
from sklearn.preprocessing import StandardScaler #Normalizes data
from statsmodels.regression.linear_model import OLS #Linear regression
from FillingTimeSeries.PreprocessingFillingMethods import Preprocessing # Created module for data processing purporses

options.mode.chained_assignment = None #Avoiding warning messages


class Autoregression:
    """
    Applies Ulrich & Clayton autoregression method
    
    Parameters
    ----------
    df: pandas dataframe
        Dataframe
    """
    def __init__(self, df):
        self.df = df.copy()
        self.df.columns, self.preprocessing = self.df.columns.astype(str), Preprocessing() #Avoiding numpy errorExplainedVarienceors
        self.dfRows, self.dfColumns = self.df.shape

    def simpleAR(self, serie, nanIndex, k):
        """
        Applies a simple autoregression
        
        Parameters
        ----------
        serie: pandas serie
            pandas serie
        nanIndex: array
            array with missing value indexes
        k: int
            number of lags for AutoReg function

        Returns
        -------
        serie: pandas serie
            pandas serie changing the missing values using nanIndex
        """
        serie = serie.copy()
        shiftting = DataFrame({})
        for i in range(1, k + 1):
            s = "Lag" + str(i)
            shiftting[s] = serie.copy().shift(i, fill_value = nan)
        lags = shiftting
        
        model = OLS(serie, lags, missing = "drop")
        modelFitted = model.fit()
        tempSerie = serie.copy()
        for index in nanIndex:
            pred = dot(modelFitted.params.values, serie[index - k : index][::-1].values)
            tempSerie[index] = pred
        serie = tempSerie
        return serie
    
    def ULCLMethod(self,  lags=1, tol=1e-1, itermax=10, valueMin=0.0):
        """
        Ulrich & Clayton autoregression method and graphs with original and filled values
        
        Parameters
        ----------
        lags: int
            Lags value for autoregression
        tol: float
            Tolerance value of difference between previous filled serie and current filled serie
        itermax: int
            Maximum iterations to find a filled serie that complies tolerance condition
        valueMin: float
            The minimum value allowed after applying the autoregression method.

        Returns
        -------
        dfPF: pandas-dataframe
            Pandas dataframe using past and future values to fill missing values
        """
        dfPF = DataFrame({})
        for column in self.df.columns:
            pastValues, pastNanIndex = self.preprocessing.changeNanMean(self.df[column]) #Missing values -> mean value
            futureValues, futureNanIndex = self.preprocessing.reverseChangeNanMean(self.df[column]) #Reversed dataframe
            pastNanIndex = delete(pastNanIndex, where(pastNanIndex < lags)) #Deleting indexes values less than or equal to k value
            futureNanIndex = delete(futureNanIndex, where(futureNanIndex < lags))

            for iter in range(1, itermax + 1):
                pastPred = self.simpleAR(serie = pastValues.copy(), nanIndex = pastNanIndex, k = lags)
                futurePredTemp = self.simpleAR(serie = futureValues.copy(), nanIndex = futureNanIndex, k = lags)
                futurePred = futurePredTemp[::-1].copy() #Reverses serie
                futurePred.index = pastPred.index #Replacing index to original index
                pastPred[pastPred.index < lags] = 0
                futurePred[futurePred.index >= (len(futurePred) - lags)] = 0
                dfPF[column] = (pastPred + futurePred) / 2 #Dataframe with past and future values
                dfPF[column][dfPF[column].index < lags] = 2 * dfPF[column][dfPF[column].index < lags]
                dfPF[column][dfPF[column].index >= (len(futurePred) - lags)] = 2 * dfPF[column][dfPF[column].index >= (len(futurePred) - lags)]
                difference = max(abs(pastValues - dfPF[column])) #differenceerece previous prediction and current prediction
                if difference <= tol:
                    break
                else:
                    pastValues = dfPF[column].copy()
                    futureValues, _ = self.preprocessing.reverseChangeNanMean(dfPF[column])
            dfPF[column][dfPF[column] < valueMin] = valueMin

        return dfPF


class PrincipalComponentAnalysis:
    """
    Applies principal component method

    Parameters
    ----------
    df: pandas dataframe
        Dataframe
    """
    def __init__(self, df, **kwargs):
        self.df = df.copy()
        self.df.columns, self.preprocessing = self.df.columns.astype(str), Preprocessing() #Avoiding numpy errorExplainedVarienceors
        self.dfRows, self.dfColumns = self.df.shape
        if "nanIndex_columns" in kwargs.keys():
            self.dfMean, self.nanIndex_columns = self.df, kwargs["nanIndex_columns"]
        else:
            self.dfMean, self.nanIndex_columns = self.preprocessing.changeDfNanMean(self.df)
    
    def checkPrincipalComponents(self):
        """
        Graphs explained variance of principal components

        Returns
        -------
        upperError: int
            Maximum value to choose principal components 
        """
        #Scalating to get the best performance using PCA
        scale = StandardScaler()
        dfMeanScaled = scale.fit_transform(self.dfMean)
        pca = PCA(n_components = self.dfColumns, copy = True, svd_solver = "full", random_state = 0)
        vectorsPCA = pca.fit_transform(dfMeanScaled)
        explainedVariance = pca.explained_variance_
        errorExplainedVarience = []

        #Calculating error bars
        for index in arange(0, len(explainedVariance)):
            dfComponents = DataFrame({"Original": vectorsPCA[:, index]})
            dfComponents["Shift"] = dfComponents.Original.shift(1)
            corr = dfComponents.corr().iloc[0, 1]
            nEffective = self.dfRows * (1 - corr**2) / (1 + corr**2)
            errorExplainedVarience.append(explainedVariance[index] * sqrt(2 / nEffective))
        components = arange(1, len(explainedVariance) + 1)
        upperError = len(explainedVariance) - 1

        #Plotting eigenvalues and principal components
        errorbar(components, explainedVariance, 
                                    yerr=errorExplainedVarience, fmt="D", color="green", 
                                    ecolor="red", capsize=10,
                                    )
        title("Explained variance vs. principal components")
        xlabel("Principal components")
        ylabel("Explained variance")
        show()
        return upperError
    
    def PCAMethod(self, components=1, tol=1e-1, itermax=10, valueMin=0.0):
        """
        Principal components method
        
        Parameters
        ----------
        components: int
            principal component number
        tol: float
            Tolerance value of difference between previous filled dataframe and current filled dataframe
        itermax: int
            Maximum iterations to find a filled dataframe that complies tolerance condition
        valueMin: float
            The minimum value allowed after applying the principal components method.
        
        Returns
        -------
        dfActual: pandas dataframe
            pandas dataframe using principal components to fill missing values
        """
        dfPast = self.dfMean.copy()
        dfActual = self.dfMean.copy()
        
        for iters in range(1, itermax + 1):
            scale = StandardScaler()
            dfPastS = scale.fit_transform(dfPast)
            pca = PCA(n_components = components, copy = True, svd_solver = "arpack", random_state = 0)
            dfFitS = pca.fit_transform(dfPastS)
            dfFitS = pca.inverse_transform(dfFitS)
            dfFit = scale.inverse_transform(dfFitS)

            #Changing values in nan indexes using principal components
            for columnIndex in range(0, len(dfActual.columns)):
                for index in self.nanIndex_columns[columnIndex]:
                    dfActual[dfActual.columns[columnIndex]][index] = dfFit[index, columnIndex]
            difference = abs(dfActual - dfPast).max(axis = 0)

            if all(difference <= tol):
                break
            else:
                dfPast = dfActual.copy()

        for column in dfActual.columns:
            dfActual[column][dfActual[column] < valueMin] = valueMin

        return dfActual


class ComponentsAutoregression:
    """
    First, this class applies the autoregression method, then, principal components method
    
    Parameters
    ----------
    df: pandas dataframe
        Dataframe
    """
    def __init__(self, df):
        self.df = df.copy()
        self.df.columns, self.preprocessing = self.df.columns.astype(str), Preprocessing() #Avoiding numpy errors
        self.dfRows, self.dfColumns = self.df.shape
        _, self.nanIndex_columns = self.preprocessing.changeDfNanMean(self.df)

    def checkPrincipalComponents(self):
        """
        Graphs explained variance of principal components

        Returns
        -------
        upperError: int
            Maximum value to choose principal components 
        """
        upperError = PrincipalComponentAnalysis(self.df).checkPrincipalComponents()
        return upperError
    
    def FullMethod(self, lags=1, components=1, tol=1e-1, itermax=10, valueMin=0.0):
        """
        Full method
        
        Parameters
        ----------
        lags: int
            Lags value for autoregression
        components: int
            principal component number
        tol: float
            Tolerance value of difference between previous filled dataframe and current filled dataframe
        itermax: int
            Maximum iterations to find a filled dataframe that complies tolerance condition
        valueMin: float
            The minimum value allowed after applying the autoregression and principal components methods.
        
        Returns
        -------
        dfPCA: pandas dataframe
            pandas dataframe using autoregression and principal components to fill missing values
        """
        AR = Autoregression(self.df)
        dfAR = AR.ULCLMethod(lags = lags, tol = tol, itermax = itermax, valueMin = valueMin)
        pca = PrincipalComponentAnalysis(dfAR, nanIndex_columns = self.nanIndex_columns)
        dfPCA = pca.PCAMethod(components = components, tol = tol, itermax = itermax, valueMin = valueMin)
        return dfPCA  