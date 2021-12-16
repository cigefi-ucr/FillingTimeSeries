# Filling Time Series (v.1.0.0)

## Filling missing values in geophysical time series
### Contact
- Rolando Jesus Duarte Mejias (rolando.duartemejias@ucr.ac.cr)
- Erick Rivera Fernandez (erick.rivera@ucr.ac.cr)

![FTS|FillingTimeSeries](https://repository-images.githubusercontent.com/404879203/f4deb7ec-6b24-4ca9-89eb-f1efc8d2fd55)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/FillingTimeSeries.svg)](https://pypi.python.org/pypi/FillingTimeSeries/) [![PyPI status](https://img.shields.io/pypi/status/FillingTimeSeries.svg)](https://pypi.python.org/pypi/FillingTimeSeries/) [![PyPI license](https://img.shields.io/pypi/l/FillingTimeSeries.svg)](https://pypi.python.org/pypi/FillingTimeSeries/)

## About Filling Time Series
Filling Time Series is a Python package to help the users to work with geophysical time series by filling missing values in their data. Filling Time Series was developed at the Centro de Investigaciones Geofísicas (CIGEFI), Universidad de Costa Rica (UCR).

## Last updates
- Stable version.

## Documentation
The documentation is available on [https://github.com/cigefi-ucr/FillingTimeSeriesGUI](https://github.com/cigefi-ucr/FillingTimeSeriesGUI)

## Features

- Autoregression-based method
- Principal-components-based method
- Full method (Autoregression - Principal components)

## Dependencies

- [Scikit-learn](https://scikit-learn.org) For principal-components-based method
- [Statsmodels](https://www.statsmodels.org/) For autoregression-based method
- [Matplotlib](https://matplotlib.org/) Plotting data
- [Pandas](https://pandas.pydata.org/) Data handler
- [Numpy](https://numpy.org/) Mathematical operations in arrays

## Installation

- Using pip:

```
pip install FillingTimeSeries
```
- Graphical interface:
Visit  [https://github.com/cigefi-ucr/FillingTimeSeriesGUI](https://github.com/cigefi-ucr/FillingTimeSeriesGUI)

## Bug report
Bug reports can be submitted to the issue tracker at:

[https://github.com/cigefi-ucr/FillingTimeSeries/issues](https://github.com/cigefi-ucr/FillingTimeSeries/issues)

## References
- Alfaro, E., & Soley, J. (2009). Descripcion de dos metodos de rellenado de datos ausentes en series de tiempo metereologicos. Revista de matematica: Teoria y Aplicaciones, 16, 60 - 75.
- Urena, P., Alfaro, E., & Soley, J. (2016). Propuestas metodologicas para el rellenado de datos ausentes en series de tiempo geofisicas. Guia Practica de uso. Universidad de Costa Rica.

## License

MIT License

**Free Software**