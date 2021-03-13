import matplotlib.pyplot as plt
import argparse
import matplotlib.animation as animation 
from matplotlib import style
from os import path
import pandas as pd
fig=plt.figure()
ax1=fig.add_subplot(1,1,1)
plt.style.use('fivethirtyeight')
def getInputs():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-o','--dataFile',
                            default=False,
                            type=str,
                            help='dataFile being output to - example.csv')
    args = parser.parse_args()
    #get user inputs
    dataFile=args.dataFile
    return dataFile
def animate(i):
    data=pd.read_csv(dataFile)
    x=data["Time (s)"]
    yTemp=data["Temperature (c)"]
    ax1.clear()
    ax1.plot(x[1::10],yTemp[1::10])
    ax1.set_title("Live Temperature Data")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Temperature (\u2103)")
    fig.tight_layout()
"""
----------------------------------------------
----------------Main run----------------------
---------------------------------------------- 
"""
def main():
    global dataFile
    dataFile=getInputs()
    #check that it doesn't already exist
    if path.exists(dataFile):
        print("Filename ",dataFile," already exists")
    #check its extension is csv
    _,fileExtension=path.splitext(dataFile)
    if fileExtension!=".csv":
        print("Filename ",dataFile," must be a csv file exiting...")
        exit(1)
    while True:
        ani=animation.FuncAnimation(fig,animate,interval=1000)
        plt.show()
if __name__=="__main__":
    main()
        

