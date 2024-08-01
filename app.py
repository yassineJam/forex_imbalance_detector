import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.patches import Rectangle
import matplotlib.dates as mdates
import sys

def main():    
    inputFile = "eurusd_hour.csv"
    index_start = int(sys.argv[1])
    index_end = int(sys.argv[2])
    app = App(inputFile, index_start, index_end)
    app.launch()


class App:
    def __init__(self, inputFile, index_start, index_end):
        self.inputFile = inputFile
        self.index_start = index_start
        self.index_end = index_end

    def launch(self):
        print("app started")
        print(self.index_end, self.index_start)
        data = self.loadCsv(self.inputFile)
        data_cleaned = self.dataCleaning(data)
        #self.plotCandleStick(data_cleaned,400,500)
        imbalance = self.generateImbalance(data_cleaned)
        self.plotCandleStickImbalance(data_cleaned,self.index_start,self.index_end)
        return 1
    
    def loadCsv(self, fileLocation):
        data = pd.read_csv(fileLocation)
        return data
    
    def resetDate(self, data):
        data['Date and Time'] = pd.to_datetime(data['Date'] + ' ' + data['Time'], format="%Y-%m-%d %H:%M")
        for index, row in data.iterrows():
            if index>1:
                previousDate = data.iloc[index-1]['Date and Time']
                data.at[index, 'Date and Time'] = previousDate + pd.DateOffset(hours=1)
    
    def addCandlestickSign(self, data):
        data['isUp'] = True
        data.loc[data['BO'] >= data['BC'], 'isUp'] = False

    def addHeight(self, data):
        data['total_height'] = abs(data["BH"] - data["BL"])
        data['height'] = abs(data["BO"] - data["BC"])

    def dataCleaning(self, data):
        self.resetDate(data)
        self.addCandlestickSign(data)
        self.addHeight(data)
        return data

    def plotCandleStick(self, data, start,end):
        data = data.iloc[start:end]
        up_price_bottom = data.loc[data['isUp']][['BO','BL', 'height', 'Date and Time', 'total_height']]
        down_price_bottom = data.loc[~data['isUp']][['BC', 'BL', 'height', 'Date and Time', 'total_height']]

        width = 0.02
        width_narrow= 0.002

        fig, ax = plt.subplots()
        ax.bar(up_price_bottom['Date and Time'], up_price_bottom['height'], width=width, bottom=up_price_bottom['BO'], color='green')
        ax.bar(up_price_bottom['Date and Time'], up_price_bottom['total_height'], width=width_narrow, bottom=up_price_bottom['BL'], color='green')
        ax.bar(down_price_bottom['Date and Time'], down_price_bottom['height'], width=width, bottom=down_price_bottom['BC'], color='red')
        ax.bar(down_price_bottom['Date and Time'], down_price_bottom['total_height'], width=width_narrow, bottom=down_price_bottom['BL'], color='red')
        formatDate = DateFormatter("%d-%m")
        ax.xaxis.set_major_formatter(formatDate)
        fig.autofmt_xdate()
        plt.show() 

    def _check_imbalance(self, data, index):
        if data.iloc[index, data.columns.get_loc("isUp")]:
            high = data.iloc[index, data.columns.get_loc("BH")]
            low = data.iloc[index+2, data.columns.get_loc("BL")]
            if high < low:
                return True
        else:
            high = data.iloc[index+2, data.columns.get_loc("BH")]
            low = data.iloc[index, data.columns.get_loc("BL")]
            if low > high:
                return True
        return False

    def generateImbalance(self, data):
        data_imbalance =[]
        data = data.reset_index(drop=True)
        size, col = data.shape
        for index, row in data.iterrows():
            first_color = row['isUp']
            if index<size-1:
                second_color = data.iloc[index+1, data.columns.get_loc("isUp")]
                if  second_color == first_color:
                    if index<size-2 and data.iloc[index+2, data.columns.get_loc("isUp")] == first_color:
                        #Three consecutive values
                        if self._check_imbalance(data, index):
                            data_imbalance.append(data.iloc[index:index+3])
        print(data_imbalance)
        return data_imbalance
    
    def plotCandleStickImbalance(self, data, start, end):
        data = data.iloc[start:end]
        data_imbalance = self.generateImbalance(data)
        up_price_bottom = data.loc[data['isUp']][['BO','BL', 'height', 'Date and Time', 'total_height']]
        down_price_bottom = data.loc[~data['isUp']][['BC', 'BL', 'height', 'Date and Time', 'total_height']]
        width = 0.02
        width_narrow= 0.007
        fig, ax = plt.subplots()
        ax.bar(up_price_bottom['Date and Time'], up_price_bottom['height'], width=width, bottom=up_price_bottom['BO'], color='green')
        ax.bar(up_price_bottom['Date and Time'], up_price_bottom['total_height'], width=width_narrow, bottom=up_price_bottom['BL'], color='green')
        ax.bar(down_price_bottom['Date and Time'], down_price_bottom['height'], width=width, bottom=down_price_bottom['BC'], color='red')
        ax.bar(down_price_bottom['Date and Time'], down_price_bottom['total_height'], width=width_narrow, bottom=down_price_bottom['BL'], color='red')
        
        for imbalance in data_imbalance:
            imbalance = imbalance.reset_index(drop = True)
            if imbalance.iloc[0]['isUp']:
                x_rec = imbalance.loc[0]['Date and Time']
                y_rec = imbalance.loc[0]['BH']
                rec_height = imbalance.loc[2]['BL']-imbalance.loc[0]['BH']
            else:
                x_rec = imbalance.loc[0]['Date and Time']
                y_rec = imbalance.loc[2]['BH']
                rec_height = imbalance.loc[0]['BL']-imbalance.loc[2]['BH']
            start = mdates.date2num(x_rec)
            end = mdates.date2num(x_rec)
            rec_width = 0.2
            ax.add_patch(Rectangle((mdates.date2num(x_rec), y_rec), rec_width, rec_height,facecolor='yellow', alpha=0.4,edgecolor='orange',linewidth=0.5))
        
        formatDate = DateFormatter("%d-%m")
        ax.xaxis.set_major_formatter(formatDate)
        fig.autofmt_xdate()
        plt.show() 
       
if __name__ == '__main__':
    main()