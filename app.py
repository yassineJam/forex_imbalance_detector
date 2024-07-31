import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def main():    
    inputFile = ""
    app = App(inputFile)
    app.launch()


class App:
    def __init__(self, inputFile):
        self.inputFile = inputFile

    def launch(self):
        print("app started")
        return 1
    
if __name__ == '__main__':
    main()