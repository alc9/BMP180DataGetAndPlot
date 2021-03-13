#Filename: BMP180Data.py
#Description: receive data from esp8266 via serial and save in csv file
#Author: Alex
#Email: alc5@hw.ac.uk
#Date: 13/03/2021
#List of sources:
#Tutorial on how to transfer data from esp8266 to python 
#https://techtutorialsx.com/2017/12/02/esp32-esp8266-arduino-serial-communication-with-python/

import serial 
import numpy as np
import argparse
from os import path
import time  
import csv
import schedule
import re
#regular expressions for sanity checking data
sensorOkPattern=re.compile(".*?OK.*?")
sensorNotOkPattern=re.compile(".*?fail.*?")
def getInputs():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-p','--port',
                        default=False, 
                        type=str, 
                        help='port for serial communication'
                        )
    parser.add_argument('-b','--baudrate',
                        default=False, 
                        type=int, 
                        help='baudrate that esp8266 is transfering data at'
                        )
    parser.add_argument('-o','--outFile',
                            default=False,
                            type=str,
                            help='output csv file name - 2barResults.csv')
    args = parser.parse_args()
    #get user inputs
    port = args.port
    baudrate = args.baudrate
    outputFileName=args.outFile
    return port, baudrate,outputFileName

def dataIO(outputFile,ser):
    #remove carriage return and line end and decode byte
    rawData=ser.readline().rstrip(b'\r\n').decode("utf-8")
    if len(rawData)==0:
        ser.close()
        raise Exception ("Serial timed out")
    decodedValuesString=str(rawData[0:len(rawData)])
    #split data from commas
    decodedValues=decodedValuesString.split(",")
    if sensorOkPattern.match(decodedValuesString):
        print("Bosch BMP180/BMP085 sensor is OK")
        return
    if sensorNotOkPattern.match(decodedValuesString):
        ser.close()
        raise Exception("Bosch BMP180/BMP085 is not connected or fail to read calibration coefficients")
    dataArray=np.array(decodedValues).astype(np.float64)
    if len(dataArray)!=3:
        return
    f=open(outputFile,'a')
    np.savetxt(f,[dataArray],delimiter=',')
    f.close()
"""
----------------------------------------------
----------------Main run----------------------
---------------------------------------------- 
"""
def main():
    port,baudrate,outputFileName=getInputs()
    #check that it doesn't already exist
    if path.exists(outputFileName):
        print("Filename ",outputFileName," already exists")
    #check its extension is csv
    _,fileExtension=path.splitext(outputFileName)
    if fileExtension!=".csv":
        print("Filename ",outputFileName," must be a csv file exiting...")
        exit(1)
    ser = serial.Serial()
    #115200
    ser.baudrate=baudrate
    try:
        #'COM4' for me
        ser.port=port
        #timeout when using readlines
        ser.timeout=10
        ser.open()
    except Exception as e:
        print(e," exiting...")
        exit(1)
    #set headers
    f = open(outputFileName,"w")
    writer=csv.DictWriter(f,fieldnames=["Time (s)","Temperature (c)","Pressure (Pa)"])
    writer.writeheader()
    f.close()
    schedule.every(0.1).seconds.do(lambda: dataIO(outputFileName,ser))
    while True:
        schedule.run_pending()
    time.sleep(1)
    ser.close()
    print("end")
if __name__=="__main__":
    main()