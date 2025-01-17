# forex_imbalance_detector

## Context
This project has been built to create an Imbalance detector on stock/forex data.
> In trading, "imbalance" refers to a situation in the market where there is a significant disparity between buy and sell orders. This can lead to sharp price movements as the market adjusts to the excess demand or supply. Imbalances often occur during periods of high volatility and can be indicators of future price direction.
 
![Imbalance concept](img/Imbalance_concept.png)

 ## Language and Dependencies
 This project has been built in Python, using the following dependencies:
 - Numpy
 - Panda
 - Matplotlib
 - Jupyter

 ## Data Sample
 The Data used in the Jupyter Notebook is the eurusd stock price from 2002 to 2020.
 This file can be found on [kaggle - EUR USD Forex Pair Historical Data (2002 - 2020)](https://www.kaggle.com/datasets/imetomi/eur-usd-forex-pair-historical-data-2002-2019?select=eurusd_hour.csv)
 
## How to launch the script
The csv file needed needs to be named "eurusd_hour.csv"
To launch the script, the following command needs to be used: `python app.py index_start index_end`
- index_start is the first index to use from the dataset (int)
- index_end is the last index to use from the dataset (int)

## Example
![Test Case 1](img/Sample_case.png)
![Test Case 2](img/Sample_case_2.png)


 >[!NOTE]
 >Any Stock and Prices data can be used but the following convention must be used for the labels:
 > - Date
 > - Time
 > - BO[^1]
 > - BH[^2]
 > - BL[^3]
 > - BC[^4]


 [^1]: Opening Price
 [^2]: Highest Price on the period
 [^3]: Lowest Price on the period
 [^4]: Closing Price