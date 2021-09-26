"""
Note: V 0.7.3 Originally, filling data methods was developed by Eric Alfaro and Javier Soley in SCILAB
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

from matplotlib import rcParams
from numpy import sqrt, abs, max, delete, where, arange, all #Handling arrays
from pandas import read_csv, DataFrame, options #Handles datasets
from sklearn.decomposition import PCA #Applies principal components transformations
from sklearn.preprocessing import StandardScaler #Normalizes data
from statsmodels.tsa.ar_model import AutoReg #Autoregression library
from FillingTimeSeries.PreprocessingFillingMethods import Preprocessing # Created module for data processing purporses
from matplotlib.pyplot import errorbar, figure, xlabel, ylabel, title, show #Graphs

rcParams["font.family"] = "sans-serif"
options.mode.chained_assignment = None #Avoiding warning messages

class AutoRegression:
    """
    Applies Ulrich & Clayton autoregression method
    
    Parameters
    ----------
    inputPath: str
        File path .txt or .csv
    """
    def __init__(self, inputPath):
        self.df = read_csv(inputPath, header = None, sep = r"\s+", na_values = "Nan") #Getting dataset
        self.df.columns, self.pss = self.df.columns.astype(str), Preprocessing() #Avoiding numpy errors
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
        model = AutoReg(serie, lags = k, old_names = True) #Autoregression
        model_fit = model.fit()

        for index in nanIndex:
            pred = model_fit.predict(start = index, end = index)
            serie[index] = pred[index]
        return serie
    
    def ULCL(self,  k = 1, tol = 1e-1, itermax = 10, valueMin = 0.0):
        """
        Ulrich & Clayton autoregression method and graphs with original and filled values
        
        Parameters
        ----------
        k: int
            Lags value for autoregression
        tol: float
            Tolerance value of difference between previous filled serie and current filled serie
        itermax: int
            Maximum iterations to find a filled serie that complies tolerance condition
        valueMin: float
            The minimum value allowed after applying the regression method.

        Returns
        -------
        dfPF: pandas-dataframe
            Pandas dataframe using past and future values to fill missing values
        """
        dfPF = DataFrame({})
        for column in self.df.columns:
            pastValues, pastNanIndex = self.pss.changeNanMean(self.df[column]) #Missing values -> mean value
            futureValues, futureNanIndex = self.pss.reverseChangeNanMean(self.df[column]) #Reversed dataframe
            pastNanIndex = delete(pastNanIndex, where(pastNanIndex <= k)) #Deleting indexes values less than or equal to k value
            futureNanIndex = delete(futureNanIndex, where(futureNanIndex <= k))

            for iter in range(1, itermax + 1):
                past_pred = self.simpleAR(serie = pastValues.copy(), nanIndex = pastNanIndex, k = k)
                future_pred_temp = self.simpleAR(serie = futureValues.copy(), nanIndex = futureNanIndex, k = k)
                future_pred = future_pred_temp[::-1].copy() #Reverses serie
                future_pred.index = past_pred.index #Replacing index to original index
                dfPF[column] = (past_pred + future_pred) / 2 #Dataframe with past and future values
                diff = max(abs(pastValues - dfPF[column])) #Differece previous prediction and current prediction

                if diff <= tol:
                    break
                else:
                    pastValues = dfPF[column].copy()
                    futureValues, _ = self.pss.reverseChangeNanMean(dfPF[column])
            dfPF[column][dfPF[column] < valueMin] = valueMin
        
        return dfPF

class PrincipalComponentAnalysis:
    """
    Applies principal component method

    Parameters
    ----------
    inputPath: str
        File path .txt or .csv
    """
    def __init__(self, inputPath):
        self.df = read_csv(inputPath, header = None, sep = r"\s+", na_values = "Nan") #Getting dataset
        self.df.columns, self.pss = self.df.columns.astype(str), Preprocessing() #Avoiding numpy errors
        self.dfRows, self.dfColumns = self.df.shape
        self.dfMean, self.nanIndex_columns = self.pss.changeDfNanMean(self.df)
    
    def checkPrincipalComponents(self):
        """
        Graphs explained variance ratio of principal components

        Returns
        -------
        upperRange: int
            Maximum value to choose principal components 
        """
        scale = StandardScaler()
        dfMeanS = scale.fit_transform(self.dfMean)
        pca = PCA(n_components = self.dfColumns, copy = True, svd_solver = "full", random_state = 0)
        pca.fit(dfMeanS)
        evr = pca.explained_variance_ratio_
        err = evr * sqrt(2 / self.dfRows)
        xRange = arange(1, len(evr) + 1)
        upperRange = len(evr) - 1
        figure(figsize = (20, 20))
        errorbar(xRange, evr, yerr =  err, fmt = "o", color = "#9b6dff", ecolor = "black", capsize = 6)
        title("Explained variance ratio vs. principal components")
        xlabel("Principal components")
        ylabel("Explained variance ratio")
        show()
        return upperRange
    
    def PCAMethod(self, components = 1, tol = 1e-1, itermax = 10, valueMin = 0.0):
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
            The minimum value allowed after applying the regression method.
        
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
            for column in dfActual.columns:
                for index in self.nanIndex_columns[int(column)]:
                    dfActual[column][index] = dfFit[index, int(column)]
            diff = abs(dfActual - dfPast).max(axis = 0)

            if all(diff <= tol):
                break
            else:
                dfPast = dfActual.copy()

        for column in dfActual.columns:
            dfActual[column][dfActual[column] < valueMin] = valueMin

        return dfActual