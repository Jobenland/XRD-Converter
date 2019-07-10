#!/usr/bin/env python
'''
XRD format converter. Makes a XLSX of multiple xrd (.out) files given with the header removed and an extra column
'''

__author__ = "Jonathan Obenland"
__copyright__ = "Copyright 2019, MEII"
__credits__ = ["Jonathan Obenland","Mikethewatchguy"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Jonathan Obenland"
__email__ = "jobenland1@gmail.com"
__status__ = "Production"


#all imports
#TODO clean this up it looks terrible
import sys
import tkinter
from tkinter import ttk
import abc
import os
import csv
import os, sys
import numpy as np
import pandas as pd
import pandas
import glob as gb
import glob 
import datetime, time
import itertools as itls
import time
from zipfile import ZipFile
import xlsxwriter
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
import fnmatch
import zipfile
import shutil
import fileinput
import re
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg

print = sg.EasyPrint

def mainWin():
    form_rows = [
                 [sg.Text("Place all XRD's in a folder to start")],
                 [sg.Text('Select new XRD folder', size=(25,1)),sg.InputText(key = 'xrdFolder'),sg.FolderBrowse()],
                 [sg.Button('start'),sg.Exit()]]

    window = sg.Window("XRD Conversion Program")
    event,values = window.Layout(form_rows).Read()

    #start the event listener
    while True:
        if event is None or event == 'Exit':
            break
        if event == 'start':
            files = values['xrdFolder']
            if files =='':
                window.Close()
                sg.PopupError("Insufficent data or Null Pointers given")
                mainWin()
            elif files != '':
                window.Close()
                listOut = createListOut(files)
                removeHeader(listOut,files)
                listOfCSV = xrdCsv(listOut)
                generateSheets(listOfCSV)
                sg.Popup('Complete')
            break

def createListOut(files):
    listOut = []
    os.chdir(files)
    fileList = os.listdir(files)  
    for file in fileList:
        filename, file_extension = os.path.splitext(file)     
        if file_extension == '.out':
            print(file ," Is a useable OUT file. Reading... ")
            listOut.append(file)
        if file_extension != '.out':
            print(file ," Is not a usable OUT file. Ignoring...")
        else:
            print(file, " Is Unrecognized by OS. Ignoring...")
    return listOut

def removeHeader(listOut,files):
    os.chdir(files)
    for outFile in listOut:
        with open (outFile, 'r', encoding = 'ISO-8859-1') as openedFile:
            rowNumber=0
            for row in openedFile:
                rowNumber+=1
                try:
                    removedFormatting = row.replace('\n','')
                    removedFormatting = removedFormatting.replace('\t','')
                    removedFormatting = removedFormatting.replace(' ', '')
                    float(removedFormatting)
                    print('end of header indicated at ', rowNumber-1, ' Getting following data...')
                    endHeaderRow = rowNumber-1
                    break
                except ValueError:
                    print('row ', row, ' was not end of header. Retrying next row...')
        print('Opening file and ammending lines')
        removeHeader = open(outFile, 'r')
        dataToRemove = removeHeader.readlines()
        removeHeader.close
        print('System STANDBY. awaiting user approval...')
        sg.Popup(outFile,"System is ready to purge the header. THIS ACTION CANNOT BE UNDONE. CREATE A BACKUP NOW!")
        print('Deleting lines 0 -> ' , endHeaderRow)
        del dataToRemove[0:endHeaderRow]
        print('Deleted. Rewriting files...')
        headerLess = open(outFile,'w')
        headerLess.writelines(dataToRemove)
        headerLess.close()
        print ("Header Successfully Removed")

def xrdCsv(listOut):
    listOfCSV = []
    for outFile in listOut:
        filename, file_extension = os.path.splitext(outFile)
        stringAngle=[]
        stringIntensity=[]
        normalizedIntensity=[]
        print('Opening ',outFile,'. Getting Data...')
        with open (outFile, 'r', encoding = 'ISO-8859-1') as f:           
            for row in f:
                for x in f:
                    sentence = " ".join(re.split("\s+", x, flags=re.UNICODE))
                    stringAngle.append(sentence.split(' ')[0])
                    stringIntensity.append(sentence.split(' ')[1])
                intAngle = [float(i) for i in stringAngle]
                intIntensity = [float(i) for i in stringIntensity]
                maxIntensity = max(intIntensity)
                normalizedIntensity = [((intIntensity[i])/(maxIntensity)) for i in range(len(intAngle))]
            print('All Data Found. Creating CSV...')
            csvName = filename +'.csv'
            dataf = {'Angle' : intAngle, 'Intensity' : intIntensity, 'Normalized Intensity' : normalizedIntensity}
            df = pd.DataFrame(data=dataf)
            df.to_csv(csvName, index = False)
            print( csvName, ' created. adding to CSV creation list...')
            listOfCSV.append(csvName)
    return listOfCSV

def generateSheets(listOfCSV):
    print('System STANDBY. awaiting user input')
    csvname = sg.PopupGetText("Enter a name for the combined excel file")
    print('Ready to ammend to ', csvname)
    writer = pd.ExcelWriter(csvname + '.xlsx', engine = 'xlsxwriter')
    for csv in listOfCSV:
        filename, file_extension = os.path.splitext(csv)
        print('found ', filename, ' adding to ',csvname) 
        df = pd.read_csv(csv)
        df.to_excel(writer, sheet_name=filename)
    writer.save()  

if __name__ == '__main__':
    mainWin()