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

import pandas as pd #Handling datasets


class Preprocessing:
        """
        Preprocesses dataframe to change missing values to mean values.
        Also, There is a function to reverse dataframe when it is necessary
        """
        def __init__(self):
                pass
    
        def changeNanMean(self, serie):
                """
                Finds missing value indexes and change the to mean values
                
                Parameters
                ----------
                serie: pandas serie
                        pandas serie with missing values
                
                Returns
                -------
                serie: pandas serie
                        pandas serie changing missing values to mean values
                nanIndex: array
                        missing values indexes
                """
                serie = serie.copy()
                nanIndex = serie[serie.isna()].index
                serie.fillna(value = serie.mean(axis=0), axis=0, inplace=True)
                return serie, nanIndex
        
        def reverseChangeNanMean(self, serie):
                """
                Reverses the pandas serie and finds missing value indexes and change the to mean values
                
                Parameters
                ----------
                serie: pandas serie
                        pandas serie with missing values
                
                Returns
                -------
                reverseSerie: pandas serie
                        Reversed pandas serie changing missing values to mean values
                reverseNanIndex: array
                        missing values indexes
                """
                reverseSerie= serie[::-1].copy()
                reverseSerie.index = serie.index
                reverseSerie, reverseNanIndex = self.changeNanMean(reverseSerie)
                return reverseSerie, reverseNanIndex
        
        def changeDfNanMean(self, df):
                """
                Finds missing value indexes and change the to mean values
                
                Parameters
                ----------
                df: pandas dataframe
                        pandas dataframe with missing values
                
                Returns
                -------
                df: pandas dataframe
                        pandas dataframe changing missing values to their respective column mean values
                nanIndexColumns: array
                        missing values in each column indexes 
                """
                df = df.copy()
                nanIndexColumns = [df[column][df[column].isna()].index for column in df.columns]
                df.fillna(value = df.mean(axis=0), axis=0, inplace=True)   
                return df, nanIndexColumns    