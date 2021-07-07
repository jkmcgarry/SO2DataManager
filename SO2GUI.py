from tkinter.filedialog import askopenfilename, asksaveasfilename
from statistics import*
import tkinter as tk
import os
import shutil
import glob
import csv
import re
import itertools

##worked 1.5 hours on 5/19/2021
##worked 1.5 hours on 5/23/2021
##consider putting in class for buttons honestly
##implement data scrubbing
##if data scrubbing, probably  make a popup window when the calculate function is run
##will prompt for a yes or no
##otherwise, could make it a seperate button to use before running maybe? this is more plausible
##have function pull up that brings up window asking if data is to be scrubbed
##if yes call another function that will open window up to enter the parameters and scrub until closed
##if no, just move to stats calculations

runEverything = 0
firstTen = 29
lastTen  = 0
count  = 0
count1 = 0
setavg  = 0 ##Sets the average value for SO2
setavg2 = 0 ##Sets the average value for TRS
listCount  = 0 ##to indicate how many items per interval are used in calculations
listCount2 = 0 ##same thing, but for TRS instead of SO2
list1 = []  ##Stores SO2 during initial calculations and reads of the file
list2 = []  ##Stores SO2 data that fits parameters chosen for calculations from the initial SO2 list
list3 = []  ##Stores TRS during initial calculations and reads of the file
list4 = []  ##Stores TRS data that fits parameters chosen for calculations from the initial TRS list
list5 = []  ##Filtered list of SO2 values that have no values above 20 or less than 0.01
list6 = []  ##Filtered list of TRS values that have no values above 20 or less than 0.01
TRSCalorHolds = [] #List that says if TRS value is a Held value or not
SO2CalorHolds = [] #List that says if SO2 value is a Held value or not
SO2SamorHold = []
TRSSamorHold = []
calColFull = []
calCol = []
initialTime = ["Starting Time"]
stopTime = ["End Time"]
initialDate = ["Starting Date"]
stopDate = ["End Date"]
lastDate = 0
lastTime = 0
dateList = [] ##List for the Local Date mm/dd/yyyy
timeList = [] ##List for the Local Time in military
dateCheck = []
timeCheck = []
listOfMax = ["SO2_Max"]
listOfMin = ["SO2_Min"]
listOfAvg = ["SO2_Mean"]
listOfSdev = ["SO2_Standard_dev"]
listOfVal = ["SO2_Count"]
listOfMax2 = ["TRS_Max"]
listOfMin2 = ["TRS_Min"]
listOfAvg2 = ["TRS_Mean"]
listOfVal2 = ["TRS_Count"]
listOfSdev2 = ["TRS_Standard_dev"]
calibrationFile = "filename"

def clearLists():
    calibrationFile = 0
    runEverything = 0
    dateList.clear()
    timeList.clear()
    list1.clear()
    list3.clear()
    calColFull.clear()
    SO2CalorHolds.clear()
    TRSCalorHolds.clear()
    listCount = 0
    listCount2 = 0
    initialDate.clear()
    initialTime.clear()
    stopDate.clear()
    stopTime.clear()
    listOfMax.clear()
    listOfMin.clear()
    listOfAvg.clear()
    listOfVal.clear()
    listOfMax2.clear()
    listOfMin2.clear()
    listOfAvg2.clear()
    listOfVal2.clear()
    listOfSdev2.clear()
    stopTime.append("End Time")
    stopDate.append("End Date")
    initialTime.append("Starting Time")
    initialDate.append("Starting Date")
    listOfMax.append("SO2_Max")
    listOfMin.append("SO2_Min")
    listOfAvg.append("SO2_Mean")
    listOfSdev.append("SO2_Standard_dev")
    listOfVal.append("SO2_Count")
    listOfMax2.append("TRS_Max")
    listOfMin2.append("TRS_Min")
    listOfAvg2.append("TRS_Mean")
    listOfVal2.append("TRS_Count")
    listOfSdev2.append("TRS_Standard_dev")

def scrubData(fileName):
    badData = True
    while(badData == True):
        startDate = input("Enter start date: ")
        startTime = input("Enter start time: ")
        endDate = input("Enter end date: ")
        endTime = input("Enter end time: ")
        first = 0
        last = 0
        for j in range(len(dateList)):
            if(dateList[j] == startDate and timeList[j] == startTime):
                first = j
        for y in range(len(dateList)):
            if(dateList[y] == endDate and timeList[y] == endTime):
                last = y + 1
        for i in range(first,last):
            try:
                if(dateList[i] == endDate and timeList[i] == endTime):
                    calColFull[i] = "calibration"
                    print("Scrubbed this timeframe")
                    response = input("Continue scrubbing? (Y/N)")
                    if(response == "y" or response == "Y"):
                        break
                    else:
                        badData = False
                        print("Data finished being scrubbed, moving on to calculations")
                        break
                else:
                    print(i)
                    calColFull[i] = "calibration"
            except IndexError:
                calColFull[i] = "calibration"
                ExitResponse = input("Continue scrubbing? (Y/N)")
                if(ExitResponse == "y" or ExitResponse == "Y"):
                    break
                else:
                    badData = False
                    break
                
def shaveseconds():
    for i in range(len(list1)):
        timeList[i] = timeList[i][:-3]
        
def simplecsv(thefile, thearray, delimiter=','):
#Simple CSV format output function that takes a open fd and 2d array. It defaults to a ',' delimiter and closes the file at the end.
    for i in range(len(thearray)):
        for j in range(len(thearray[0])):
            if j != len(thearray[0])-1:
                thefile.write("%s%s" % (thearray[i][j],delimiter))
            else:
                thefile.write("%s%c" % (thearray[i][j],'\n'))
    thefile.close()

def tagNegatives(fileName):
    for i in range(len(list1)):
        if(list1[i] < 0.01):
            list1[i] = 0.01
        if(list3[i] < 0.01):
            list3[i] = 0.01
    calibrationFile = fileName
    with open(calibrationFile, "w") as txt_file:
        simplecsv(txt_file,list(zip(dateList,timeList,list1,list3,calColFull,SO2CalorHolds,TRSCalorHolds)))
        print("Seperate file made with negatives tagged.")
        
def makeCSV(fileName, time):
    global initialDate
    global initialTime
    global listCount
    global listCount2
    timeFrame = time
    removeExtension = fileName[:-4]
    if(timeFrame == "Daily" or timeFrame == "daily"):
        cdata = removeExtension + "Daily" + ".csv"
        with open(cdata, "w") as txt_file:
            writer = csv.writer(txt_file, delimiter='\t')
            writer.writerows(zip(initialDate,initialTime,stopDate,stopTime,listOfMin,listOfMax,listOfAvg,listOfSdev,listOfVal,listOfMin2,listOfMax2,listOfAvg2,listOfSdev2,listOfVal2))
    elif(timeFrame == "Hourly" or timeFrame == "hourly"):
        cdata = removeExtension + "Hourly" + ".csv"
        with open(cdata, "w") as txt_file:
            writer = csv.writer(txt_file, delimiter='\t')
            writer.writerows(zip(initialDate,initialTime,stopDate,stopTime,listOfMin,listOfMax,listOfAvg,listOfSdev,listOfVal,listOfMin2,listOfMax2,listOfAvg2,listOfSdev2,listOfVal2))
    elif(timeFrame == "Slice" or timeFrame == "slice"):
        for t in range(len(initialTime)):
            if initialTime[t] != "Starting Time":
                initialTime[t] = str(initialTime[t])
                if len(initialTime[t]) == 3:
                       initialTime[t] = initialTime[t][:1] + ":" + initialTime[t][1:]
                elif len(initialTime[t]) == 4:
                       initialTime[t] = initialTime[t][:2] + ":" + initialTime[t][2:]
        for r in range(len(stopTime)):
            if stopTime[r] != "End time":
                stopTime[r] = str(stopTime[r])
                if len(stopTime[r]) == 3:
                    stopTime[r] = stopTime[r][:1] + ":" + stopTime[r][1:]
                elif len(stopTime[r]) == 4:
                    stopTime[r] = stopTime[r][:2] + ":" + stopTime[r][2:]
                         
        cdata = removeExtension + "Slice" + ".csv"
        with open(cdata, "w") as txt_file:
            writer = csv.writer(txt_file, delimiter='\t')
            writer.writerows(zip(initialDate,initialTime,stopDate,stopTime,listOfMin,listOfMax,listOfAvg,listOfSdev,listOfVal,listOfMin2,listOfMax2,listOfAvg2,listOfSdev2,listOfVal2))
    elif(timeFrame == "Custom" or timeFrame == "custom"):
        cdata = removeExtension + "Custom" + ".csv"
        with open(cdata, "w") as txt_file:
            writer = csv.writer(txt_file, delimiter='\t')
            writer.writerows(zip(initialDate,initialTime,stopDate,stopTime,listOfMin,listOfMax,listOfAvg,listOfSdev,listOfVal,listOfMin2,listOfMax2,listOfAvg2,listOfSdev2,listOfVal2))
    print("Saved calcuation restuls file as: ", cdata)
    clearLists()
    
def removeNODATA():
    global listCount
    global listCount2
    emptyValue = 0
    lowerEndChanges = 0
    TRSEndChanges = 0
    for k in range(len(list2)):
        if(list2[k] < 0.01):
            list2[k] = 0.01
            lowerEndChanges = lowerEndChanges + 1
        if(list4[k] < 0.01):
            list4[k] = 0.01
            TRSEndChanges = TRSEndChanges + 1
    for i in range(len(list2)):
        try:
            if((list2[i] >= 0.01 and list2[i] < 40) and (calCol[i] != "calibration") and SO2SamorHold[i] == "sample..."):
                list5.append(list2[i])
            else:
                listCount = listCount - 1
        except IndexError:
            list5.append(list2[i])
    if(len(list5) == 0):
        list5.append(emptyValue)
        listCount2 = listCount2 + 1
    for j in range(len(list4)):
        try:
            if((list4[j] >= 0.01 and list4[j] < 40) and (calCol[j] != "calibration") and TRSSamorHold[j] == "sample..."):
                list6.append(list4[j])
            else:
                listCount2 = listCount2 - 1
        except IndexError:
            list6.append(list4[j])
    if(len(list6) == 0):
        list6.append(emptyValue)
        listCount2 = listCount2 + 1
        
def calculate():
    global listCount
    global listCount2
    removeNODATA()
    if(len(list5) == 0):
        list5.append(0)
    if(len(list5) > 0):
        listOfMin.append(min(list5))
        listOfMax.append(max(list5))
        setavg = mean(list5)
        listOfAvg.append(setavg)
        listOfVal.append(len(list5))
    elif(len(list5) == 0):
        listOfMin.append("NO_DATA")
        listOfMax.append("NO_DATA")
        listOfAvg.append("NO_DATA")
        listOfVal.append("NO_DATA")
    if(listCount <= 1):
        listOfSdev.append("NO_DATA")
    else:
        if(len(list5) >1):
            listOfSdev.append(stdev(list5))
            listCount = 0
        else:
            listOfSdev.append("NO_DATA")
    if(len(list6) > 0):
        listOfMin2.append(min(list6))
        listOfMax2.append(max(list6))
        setavg2 = mean(list6)
        listOfAvg2.append(setavg2)
        listOfVal2.append(len(list6))
    elif(len(list6) == 0):
        listOfMin.append("NO_DATA")
        listOfMax.append("NO_DATA")
        listOfAvg.append("NO_DATA")
        listOfVal.append("NO_DATA")
    if(listCount2 <= 1):
        listOfSdev2.append("NO_DATA")
    else:
        if(len(list6) > 1):
            listOfSdev2.append(stdev(list6))
            listCount2 = 0
        else:
            listOfSdev2.append("NO_DATA")
            

def getStats(event = None):
    global listCount
    global listCount2
    global initialDate
    global initialTime
    global calibrationFile
    global runEverything
    
    time = statEntry.get()
    startDate = startDateEntry.get()
    startTime = startTimeEntry.get()
    endDate = endDateEntry.get()
    endTime = endTimeEntry.get()
    if(runEverything == 0):
        fileName = a1.get()
    else:
        fileName = calibrationFile
    rangeCount = 0
    infile = open(fileName, 'r')
    while(True):
        line = infile.readline()
        if(line == ""):
            break
        word = line.split(' ')
        dateList.append(word[0])
        timeList.append(word[1])
        list1.append(word[6])
        list3.append(word[7])
        calColFull.append(word[8])
        SO2CalorHolds.append(word[9])
        TRSCalorHolds.append(word[10])   
    infile.close()
    for n in range(len(list1)):
        if(TRSCalorHolds[n].endswith('\n')):
           TRSCalorHolds[n] = TRSCalorHolds[n][:-1]
    for m in range(len(list1)):
        list1[m] = float(list1[m])
        if(list3[m] == ''):
            print(m)
        list3[m] = float(list3[m])
    shaveseconds()
    ##tagNegatives(fileName)
    for c in range(len(list1)):
        if(list1[c] < 0.01):
            list1[c] = 0.01
        if(list3[c] < 0.01):
            list3[c] = 0.01
    if(time == "Hourly" or time == "hourly"):
        lastTime = timeList[-1]
        for n in range(len(list1)):
            try:
                if(timeList[n].endswith('00') or listCount == 0): ##if on the hour or list is empty, make this value the start value
                    initialDate.append(dateList[n])
                    initialTime.append(timeList[n])
                    list2.append(list1[n])
                    list4.append(list3[n])
                    calCol.append(calColFull[n])
                    SO2SamorHold.append(SO2CalorHolds[n])
                    TRSSamorHold.append(TRSCalorHolds[n])
                    listCount = listCount + 1
                    listCount2 = listCount2 + 1
                elif((timeList[n].endswith('59') or (dateList[n] != dateList[n+1] and n < len(list1)))): ##if last minute of the hour or the next value's day is not the same and not at end of list, add value for the hour
                    stopDate.append(dateList[n])
                    stopTime.append(timeList[n])
                    calCol.append(calColFull[n])
                    SO2SamorHold.append(SO2CalorHolds[n])
                    TRSSamorHold.append(TRSCalorHolds[n])
                    list2.append(list1[n])
                    list4.append(list3[n])
                    listCount = listCount + 1
                    listCount2 = listCount2 + 1
                    calculate()
                    list2.clear()
                    list4.clear()
                    calCol.clear()
                    SO2SamorHold.clear()
                    TRSSamorHold.clear()
                    list5.clear()
                    list6.clear()
                    listCount = 0
                    listCount2 = 0
                elif((not timeList[n].endswith('00') or not timesList[n].endswith('59')) and timeList[n][:2] == timeList[n+1][:2] and n < len(list1)): ##if not on the hour or last minute and first two values are the same
                    dateCheck.append(dateList[n])
                    timeCheck.append(timeList[n])
                    list2.append(list1[n])
                    list4.append(list3[n])
                    calCol.append(calColFull[n])
                    SO2SamorHold.append(SO2CalorHolds[n])
                    TRSSamorHold.append(TRSCalorHolds[n])
                    listCount = listCount + 1
                    listCount2 = listCount2 + 1
                elif(timeList[n] == lastTime): ##if very last entry add to list
                    stopDate.append(dateList[n])
                    stopTime.append(timeList[n])
                    calCol.append(calColFull[n])
                    list2.append(list1[n])
                    list4.append(list4[n])
                    SO2SamorHold.append(SO2CalorHolds[n])
                    TRSSamorHold.append(TRSCalorHolds[n])
                    listCount = listCount + 1
                    listCount2 = listCount2 + 1
                    calculate()
                    list2.clear()
                    list4.clear()
                    list5.clear()
                    list6.clear()
                    calCol.clear()
                    SO2SamorHold.clear()
                    TRSSamorHold.clear()
                    listCount = 0
                    listCount2 = 0
                else:
                    dateCheck.append(dateList[n])
                    timeCheck.append(timeList[n])
                    list2.append(list1[n])
                    list4.append(list3[n])
                    calCol.append(calColFull[n])
                    SO2SamorHold.append(SO2CalorHolds[n])
                    TRSSamorHold.append(TRSCalorHolds[n])
                    listCount = listCount + 1
                    listCount2 = listCount2 + 1
            except IndexError:
                stopDate.append(dateList[n])
                stopTime.append(timeList[n])
                calCol.append(calColFull[n])
                list2.append(list1[n])
                list4.append(list3[n])
                SO2SamorHold.append(SO2CalorHolds[n])
                TRSSamorHold.append(TRSCalorHolds[n])
                listCount = listCount + 1
                listCount2 = listCount2 + 1
                calculate()
                list2.clear()
                list4.clear()
                list5.clear()
                list6.clear()
                calCol.clear()
                SO2SamorHold.clear()
                TRSSamorHold.clear()
                listCount = 0
                listCount2 = 0
        makeCSV(fileName, time)
    elif(time == "Daily" or time == "daily"):
        lastTime = timeList[-1]
        lastDate = dateList[-1]
        for n in range(len(list1)):
            try:
                if((timeList[n].startswith('00') and timeList[n].endswith('00')) or listCount == 0):
                    initialDate.append(dateList[n])
                    initialTime.append(timeList[n])
                    list2.append(list1[n])
                    list4.append(list3[n])
                    calCol.append(calColFull[n])
                    SO2SamorHold.append(SO2CalorHolds[n])
                    TRSSamorHold.append(TRSCalorHolds[n])
                    listCount = listCount + 1
                    listCount2 = listCount2 + 1 
                elif((timeList[n].startswith('23') and timeList[n].endswith('59')) or (dateList[n] != dateList[n+1] and n < len(list1))):
                    stopDate.append(dateList[n])
                    stopTime.append(timeList[n])
                    calCol.append(calColFull[n])
                    SO2SamorHold.append(SO2CalorHolds[n])
                    TRSSamorHold.append(TRSCalorHolds[n])
                    list2.append(list1[n])
                    list4.append(list3[n])
                    listCount = listCount + 1
                    listCount2 = listCount2 + 1 
                    calculate()
                    list2.clear()
                    list4.clear()
                    list5.clear()
                    list6.clear()
                    calCol.clear()
                    SO2SamorHold.clear()
                    TRSSamorHold.clear()
                    listCount = 0
                    listCount2 = 0            
                elif(timeList[n] == lastTime and dateList[n] == lastDate):
                    stopDate.append(dateList[n])
                    stopTime.append(timeList[n])
                    calCol.append(calColFull[n])
                    SO2SamorHold.append(SO2CalorHolds[n])
                    TRSSamorHold.append(TRSCalorHolds[n])
                    list2.append(list1[n])
                    list4.append(list3[n])
                    listCount = listCount + 1
                    listCount2 = listCount2 + 1 
                    calculate()
                    list2.clear()
                    list4.clear()
                    list5.clear()
                    list6.clear()
                    calCol.clear()
                    SO2SamorHold.clear()
                    TRSSamorHold.clear()
                    listCount = 0
                    listCount2 = 0
                else:
                    dateCheck.append(dateList[n])
                    timeCheck.append(timeList[n])
                    calCol.append(calColFull[n])
                    SO2SamorHold.append(SO2CalorHolds[n])
                    TRSSamorHold.append(TRSCalorHolds[n])
                    list2.append(list1[n])
                    list4.append(list3[n])
                    listCount = listCount + 1
                    listCount2 = listCount2 + 1
            except IndexError:
                stopDate.append(dateList[n])
                stopTime.append(timeList[n])
                calCol.append(calColFull[n])
                SO2SamorHold.append(SO2CalorHolds[n])
                TRSSamorHold.append(TRSCalorHolds[n])
                list2.append(list1[n])
                list4.append(list3[n])
                listCount = listCount + 1
                listCount2 = listCount2 + 1 
                calculate()
                list2.clear()
                list4.clear()
                list5.clear()
                list6.clear()
                calCol.clear()
                SO2SamorHold.clear()
                TRSSamorHold.clear()
                listCount = 0
                listCount2 = 0
        makeCSV(fileName, time)
    elif(time == "Custom" or time == "custom"): ##might need to convert the dates into integers to compare them.
        firstPoint = 0
        finalPoint = 0
        startFound = 0
        endFound = 0
        startTimeFound = 0
        endTimeFound = 0
        initialDate.append(startDate)
        initialTime.append(startTime)
        stopDate.append(endDate)
        stopTime.append(endTime)
        startDate = int(startDate.translate({ord('/'): None}))
        endDate = int(endDate.translate({ord('/'): None}))
        startTime = startTime.replace("'","")
        startTime = startTime.replace(":","")
        endTime = endTime.replace("'","")
        endTime = endTime.replace(":","")
        
        startTime = int(startTime)
        endTime = int(endTime.replace("'",""))
        
        for x in range(len(dateList)):
            dateList[x] = int(dateList[x].translate({ord('/'): None}))
            if(len(timeList[x]) == 4):
                timeList[x] = timeList[x][:1] + timeList[x][3:]
                timeList[x] = int(timeList[x])
            else:
                timeList[x] = timeList[x][:2] + timeList[x][3:]
                timeList[x] = int(timeList[x])
        for z in range(len(dateList)):
            if dateList[z] == endDate and timeList[z] == endTime:
                endDate = dateList[z]
                endTime = timeList[z]
                finalPoint = z
        for j in range(len(dateList)):
            try:
                if (dateList[j] == startDate and timeList[j] == startTime):
                    firstPoint = j
                    startFound = 1
                    startTimeFound = 1
                    
                elif(dateList[j] != startDate):
                    if dateList[j] > startDate and dateList[j-1] < startDate and startFound == 0:
                        if(str(dateList[j])[-1:] == str(startDate)[-1:]):
                            firstPoint = j
                            startFound = 1
                            startDate = dateList[j]
                            initialDate.pop()
                            initialDate.append(dateList[j])
                        
                if (dateList[j] == endDate and timeList[j] == endTime):
                    finalPoint = z
                    endDate = dateList[z]
                    endTime = timeList[z]
                    endFound = 1
                    endTimeFound = 1
                    
                elif(dateList[j] != endDate):
                    if (dateList[j] < endDate and dateList[j+1] > endDate) and endFound == 0:
                        if(str(dateList[j])[-1:] == str(endDate)[-1:]):
                            finalPoint = j
                            endDate = dateList[j]
                            stopDate.pop()
                            stopDate.append(dateList[j])
                        
            except IndexError:
                finalPoint = j
                endDate = dateList[j]
                stopDate.pop()
                stopDate.append(dateList[j])
                break
                
        for l in range(len(timeList)):
            try:
                if dateList[l] == startDate and timeList[l] != startTime:
                    if timeList[l] > startTime and startTimeFound == 0:
                        startTimeFound = 1
                        startTime = timeList[l]
                        initialTime.pop()
                        initialTime.append(timeList[l])
                        
                if dateList[l] == endDate and timeList[l] != endTime:
                    if timeList[l] < endTime and timeList[l+1] > endTime and endTimeFound == 0:
                        endTimeFound = 1
                        endTime = timeList[l]
                        stopTime.pop()
                        stopTime.append(timeList[l])
                        
            except IndexError:
                if endTimeFound == 0:
                    endTimeFound = 1
                    endTime = timeList[l]
                    finalPoint = l
                    stopTime.pop()
                    stopTime.append(timeList[l])
                    break
        for i in range(firstPoint, finalPoint + 1):
            try:
                if(dateList[i] == endDate and timeList[i] == endTime):
                    dateCheck.append(dateList[i])
                    timeCheck.append(timeList[i])
                    list2.append(list1[i])
                    list4.append(list3[i])
                    calCol.append(calColFull[i])
                    SO2SamorHold.append(SO2CalorHolds[i])
                    TRSSamorHold.append(TRSCalorHolds[i])
                    listCount = listCount + 1
                    listCount2 = listCount2 + 1
                    calculate()
                    list2.clear()
                    list4.clear()
                    list5.clear()
                    list6.clear()
                    calCol.clear()
                    SO2SamorHold.clear()
                    TRSSamorHold.clear()
                    listCount = 0
                    listCount2 = 0
                else:
                    dateCheck.append(dateList[i])
                    timeCheck.append(timeList[i])
                    list2.append(list1[i])
                    list4.append(list3[i])
                    calCol.append(calColFull[i])
                    SO2SamorHold.append(SO2CalorHolds[i])
                    TRSSamorHold.append(TRSCalorHolds[i])
                    listCount = listCount + 1
                    listCount2 = listCount2 + 1
            except IOError:
                stopDate.append(dateList[i])
                stopTime.append(timeList[i])
                calCol.append(calColFull[i])
                SO2SamorHold.append(SO2CalorHolds[i])
                TRSSamorHold.append(TRSCalorHolds[i])
                list2.append(list1[i])
                list4.append(list3[i])
                listCount = listCount + 1
                listCount2 = listCount2 + 1 
                calculate()
                list2.clear()
                list4.clear()
                list5.clear()
                list6.clear()
                calCol.clear()
                SO2SamorHold.clear()
                TRSSamorHold.clear()
                listCount = 0
                listCount2 = 0
        makeCSV(fileName, time)
    elif(time == "Slice" or time == "slice"):
        startFound = 0
        endDay = startDate
        startValue = 0
        endValue = 0
        ##startTime = startTime.replace("'","")
        ##startTime = startTime.replace(":","")
        ##endTime = endTime.replace("'","")
        ##endTime = endTime.replace(":","")
        startTime = int(startTime.replace(':',''))
        endTime = int(endTime.replace(':',''))
        for x in range(len(timeList)):
            if(len(timeList[x]) == 4):
                timeList[x] = timeList[x][:1] + timeList[x][3:]
                timeList[x] = int(timeList[x])
            else:
                timeList[x] = timeList[x][:2] + timeList[x][3:]
                timeList[x] = int(timeList[x])
        for j in range(len(dateList)):
            if(dateList[j] == startDate and timeList[j] == startTime):
                startValue = j
        for k in range(len(dateList)):
            if(dateList[k] == endDate and (timeList[k] == endTime or k == len(list1)) ):
                endValue = k
            elif(dateList[k] == endDate and (timeList[k] < endTime and timeList[k] <= startTime)):
                endValue = k
        for i in range(startValue, endValue+1):
            try:
                if(timeList[i] >= startTime and timeList[i] <= endTime and i != endValue+2): ##append data that is between the start and end time of each day
                    dateCheck.append(dateList[i])
                    timeCheck.append(timeList[i])
                    list2.append(list1[i])
                    list4.append(list3[i])
                    calCol.append(calColFull[i])
                    SO2SamorHold.append(SO2CalorHolds[i])
                    TRSSamorHold.append(TRSCalorHolds[i])
                    listCount = listCount + 1
                    listCount2 = listCount2 + 1
                    if(timeList[i] == startTime or i == len(list1)): ##append the start date and time a day
                        initialDate.append(dateList[i])
                        initialTime.append(timeList[i])
                        startFound = 1
                    elif(timeList[i] > startTime and timeList[i-1] < startTime and startFound == 0):
                        initialDate.append(dateList[i])
                        initialTime.append(timeList[i])
                        startFound = 1
                    if(timeList[i] == endTime): ##append the end date and time for a day
                        stopDate.append(dateList[i])
                        stopTime.append(timeList[i])
                        if(dateList[i] == endDate): ##just to indicate that this is the last day and to break once done
                            calculate()
                            list2.clear()
                            list4.clear()
                            list5.clear()
                            list6.clear()
                            calCol.clear()
                            SO2SamorHold.clear()
                            TRSSamorHold.clear()
                            listCount = 0
                            listCount2 = 0
                            startFound = 0
                            break
                        else: ##calculates results for day and then keeps going on to next one
                            calculate()
                            list2.clear()
                            list4.clear()
                            list5.clear()
                            list6.clear()
                            calCol.clear()
                            SO2SamorHold.clear()
                            TRSSamorHold.clear()
                            listCount = 0
                            listCount2 = 0
                            startFound = 0
                    elif((dateList[i] == endDate or dateList[i] != dateList[i+1]) and (timeList[i] < endTime and timeList[i+1] > endTime)): ##if no end date found at last day, then stop and save what values are there
                        stopDate.append(dateList[i])
                        stopTime.append(timeList[i])
                        calculate()
                        list2.clear()
                        list4.clear()
                        list5.clear()
                        list6.clear()
                        calCol.clear()
                        SO2SamorHold.clear()
                        TRSSamorHold.clear()
                        listCount = 0
                        listCount2 = 0
                        break
            except IndexError:
                break
        makeCSV(fileName, time)
    else:
        print("Please pick a valid option...")
        
def removespaces(event = None):
    global calibrationFile
    global runEverything
    if(runEverything == 0):
        fileName = a1.get()
    else:
        fileName = calibrationFile
    inputFile = open(fileName, 'r')
    noExtension = fileName[:-4]
    outputFile = open(noExtension + "Modified" + '.csv', 'w')
    firstLine = inputFile.readline()
    for line in inputFile:
        if not line.strip():
            continue
        new_line = line.replace('\t', ' ')
        new_line = line.replace('"', '')
        new_line = line.replace(',', ' ')
        outputFile.write(new_line)
    inputFile.close()
    outputFile.close()
    calibrationFile = noExtension + "Modified" + '.csv'
    print("file is now: ", calibrationFile)
    
def columnAvg(event = None):
    global count
    global count1
    global calibrationFile
    global runEverything
    if(runEverything == 0):
        fileName = a1.get()
    fileName = calibrationFile
    LocalDate   = []
    LocalTime   = []
    UTCDate     = []
    UTCTime     = []
    Rcell       = []
    SampleFlow  = []
    Calibration = []
    TRS         = []
    SO2         = []
    HeldValue1  = []
    HeldValue2  = []
    infile = open(fileName, 'r')
    while True:
        line = infile.readline()
        if line == "":
            break
        word = line.split(',')
        LocalDate.append(word[0])
        UTCDate.append(word[1])
        Rcell.append(word[2])
        SampleFlow.append(word[3])
        SO2.append(word[4])
        TRS.append(word[5])
        Calibration.append(word[6])
    infile.close()
    SO2.pop(0)
    TRS.pop(0)
    for m in range(len(TRS)):
        TRS[m] = float(TRS[m])
    for n in range(len(SO2)):
        SO2[n] = float(SO2[n])
    for k in range(len(TRS)):
        if Calibration[k].endswith('\n'):
            Calibration[k] = Calibration[k][:-1]
    for i in range(len(TRS)):
        try:
            if TRS[i] == TRS[i+1] and TRS[i] != TRS[i-1]:
                HeldValue2.append("sample...")
            elif TRS[i] == TRS[i+1] and TRS[i] == TRS[i-1]:
                HeldValue2.append("Holding...")
            elif TRS[i] != TRS[i+1] and TRS[i] == TRS[i-1]:
                HeldValue2.append("Holding...")
            elif TRS[i] != TRS[i+1] and TRS[i] != TRS[i-1]:
                HeldValue2.append("sample...")
            else:
                HeldValue2.append("sample...")
        except IndexError:
            HeldValue2.append("sample...")
            break
    for j in range(len(SO2)):
        try:
            if SO2[j] == SO2[j+1] and SO2[j] != SO2[j-1]:
                HeldValue1.append("sample...")
            elif SO2[j] == SO2[j+1] and SO2[j] == SO2[j-1]:
                HeldValue1.append("Holding...")
            elif SO2[j] != SO2[j+1] and SO2[j] == SO2[j-1]:
                HeldValue1.append("Holding...")
            elif SO2[j] != SO2[j+1] and SO2[j] != SO2[j-1]:
                HeldValue1.append("sample...")
            else:
                HeldValue1.append("sample...")
        except IndexError:
            HeldValue1.append("sample...")
            break
    HeldValue1.insert(0,"SO2 Holds")
    HeldValue2.insert(0,"TRS hold")
    SO2.insert(0, "S02 Concentrations")
    TRS.insert(0, "TRS Concentrations")
    for z in range(len(HeldValue2)):
        if Calibration[z].endswith('\n'):
            Calibration[z] = Calibration[z][:-1]
    with open(fileName, "w") as txt_file:
        simplecsv(txt_file,list(zip(LocalDate,UTCDate,Rcell,SampleFlow,SO2,TRS,Calibration,HeldValue1,HeldValue2)))
    calibrationFile = fileName
    LocalDate.clear()
    UTCDate.clear()
    Rcell.clear()
    SampleFlow.clear()
    SO2.clear()
    TRS.clear()
    Calibration.clear()
    
def grabColumn(event = None):
    if(runEverything == 0):
        fileName = a1.get()
    else:
        fileName = inputEntry.get()
    global firstTen
    global lastTen
    global calibrationFile
    column0     = []
    column1     = []
    column2     = []
    column3     = []
    column4     = []
    column5     = []
    column6     = []
    array       = []
    localtime   = []
    centraltime = []
    infile = open(fileName,'r')
    while True:
        line = infile.readline()
        if line == "":
            break
        word = line.split(', ')
        localtime.append(word[0])
        centraltime.append(word[1])
    infile.close()
    with open(fileName) as infile:
        for line in infile:
            columnSplit0 = (line.split(',')[0]) #local Date, but also has UTC in it for some reason
            column0.append(columnSplit0)
            columnSplit1 = (line.split(',')[1]) #UTC Date, This one causes issues for some reason
            column0.append(columnSplit1)
            columnSplit2 = (line.split(',')[2]) #Disk Space
            column2.append(columnSplit2)
            columnSplit3 = (line.split(',')[3]) #Rcell Temp
            column3.append(columnSplit3)
            columnSplit4 = (line.split(',')[4]) #Sample Flow
            column4.append(columnSplit4)
            columnSplit5 = (line.split(',')[5]) #SO2 Concentration
            column5.append(columnSplit5)
            columnSplit6 = (line.split(',')[6]) #TRS Concentration
            column6.append(columnSplit6)
            zip(localtime,centraltime,column3,column4,column5,column6,array)
    column0 = [x.strip(' ') for x in column0]
    column1 = [x.strip(' ') for x in column1]#does not have anything in it
    column2 = [x.strip(' ') for x in column2]
    column3 = [x.strip(' ') for x in column3]
    column4 = [x.strip(' ') for x in column4]
    column5 = [x.strip(' ') for x in column5]
    column6 = [x.strip(' ') for x in column6]
    column6.pop(0)
    column5.pop(0)
    for i in range(len(column5)):
        if column5[i] == '-----':
            column5[i] = '9999999'
        elif column5[i] == '----':
            column5[i] = '9999999'
        elif column5[i] == '---':
            column5[i] == '9999999'
        column5[i] = float(column5[i])
    for i in range(len(column6)):
            if column6[i].endswith('\n'):#Changed '\r\n' to '\n'
                column6[i] = column6[i][:-1]
            if column6[i] == '-----' or column6[i] == '----': #Added or
                column6[i] = float(9999999)
            elif column6[i] == '---':
                column6[i] = float(9999999)
            if column5[i] == '-----' or column5[i] == '----': #Added or
                column5[i] = float(9999999)
            elif column5[i] == '---':
                column5[i] = float(9999999)
            if column5[i] == "":
                column5[i] = 9999999
            if str(column5[i]).endswith('E-'):
                column5[i] = column5[i][:-2]
                column5[i] = float(column5[i])
            if (float(column6[i]) > float(40) or float(column5[i]) > float(40)):
                array.append("calibration")
            else:
                array.append("sample")
    for i in range(len(column6)-1):
        if (array[i] == "sample" and array[i+1] == "calibration") and array[i] != "calibration":
            while firstTen > -1:
                array[i-firstTen] = "calibration"
                firstTen -= 1
            firstTen = 29
        if (array[i] == "sample" and array[i-1] == "calibration") and (float(column6[i-1]) > 40 or float(column5[i-1] > float(40))):
            while lastTen < 30:
                array[i+lastTen] = "calibration"
                lastTen += 1
            lastTen = 0
            array[i] = "calibration"
    column6.insert(0,"TRS Concentrations")
    array.insert(0,"Calibrations/samples")
    column5.insert(0,"S02 Concentrations")
    tempTXTfile = fileName[:-4]
    calibrationLabelFile = tempTXTfile + '.csv'
    with open(calibrationLabelFile, "w") as txt_file:
        simplecsv(txt_file,list(zip(localtime,centraltime,column3,column4,column5,column6,array)))
    print("Column data saved to " + calibrationLabelFile + " in directory.")
    calibrationFile = calibrationLabelFile
    txt_file.close()
    localtime.clear()
    centraltime.clear()
    column2.clear()
    column3.clear()
    column4.clear()
    column5.clear()
    column6.clear()
    array.clear()
        
def exit_program():
    exit()
    
def open_file():
    filepath = askopenfilename(
        filetypes = [("CSV Files", "*.csv"), ("All Files", "*.*"), ("Text files", "*.txt")]
    )
    if not filepath:
        return
    txt_edit.delete("1.0", tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"Placeholder - {filepath}")

def save_file():
    filepath = asksaveasfilename(
        defaultextension="csv",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*"), ("CSV Files", "*.csv")],
        )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text = txt_edit.get(1.0, tk.END)
        output_file.write(text)
    window.title(f"SO2 Data Manager - {filepath}")
        
def readME_file():
    filepath = "SO2README.txt"
    txt_edit.delete("1.0", tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"placeholder - {filepath}")
def delete_file():
    filepath = askopenfilename(
        filetypes = [("All files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete("1.0", tk.END)
    os.remove(filepath)
    text = (filepath + " deleted.")
    txt_edit.insert(tk.END, text)
   
def functionbutton(event = None):
    val1 = a1.get()
    val2 = b1.get()
    val3 = c1.get()
    val4 = "dupes.txt"
    File_OneFound = 0
    File_TwoFound = 0
    try:
        f = open(val1, "r")
        File_OneFound = 1
        f.close()
        try:
            f = open(val2, "r")
            File_TwoFound = 1
            f.close()     
        except IOError:
            print("part 2 does not exist")
    except IOError:
        print("part 1 does not exist")
    if File_OneFound == 1 and File_TwoFound == 1:
        with open(val4, "wb") as wfd:
                for f in [val1,val2]:
                    with open(f, "rb") as fd:
                        shutil.copyfileobj(fd,wfd,1024*1024*10)
    lines_seen = set() # holds lines already seen
    outfile = open(val3, "w")
    for line in open(val4, "r"):
        if line not in lines_seen: # not a duplicate
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()
    txt_edit.insert(tk.END, val3)
    

def clicked(event = None):
    prompt = tk.Tk()
    prompt.geometry("200x200")
    prompt.config(bg = "#f1dd38")
    btn_yes = tk.Button(prompt, text="yes", command = functionbutton,sticky = "ew")
    btn_yes.grid(row = 1, column = 0)
    btn_no = tk.Button(prompt, text="no", command = prompt.destroy,sticky = "ew")
    btn_no.grid(row = 1, column = 1)

def allSteps(event = None):
    global runEverything
    runEverything = 1
    grabColumn()
    columnAvg()
    removespaces()
    getStats()
    
    
def runAll():
    global inputEntry, statEntry, startDateEntry, startTimeEntry, endDateEntry, endTimeEntry
    newWindow = tk.Tk()
    newWindow.title("Entry parameters")
    newWindow.geometry("400x230")
    newWindow.config(bg = "#f1dd38")
    newWindow.resizable(0,0)
    date_text = "mm/dd/yyyy"
    time_text = "24:00"
    file_text = "Filename.txt"
    inputFile = tk.Label(newWindow, text = "Text file").grid(row = 0, column = 0,sticky = "ew")
    stat_option = tk.Label(newWindow, text = "Calc setting").grid(row = 1, column = 0,sticky = "ew")
    start_date = tk.Label(newWindow, text = "Start date").grid(row = 2, column = 0,sticky = "ew")
    start_time = tk.Label(newWindow, text = "Start time").grid(row = 3, column = 0,sticky = "ew")
    end_date = tk.Label(newWindow, text = "End date").grid(row = 4, column = 0,sticky = "ew")
    end_time = tk.Label(newWindow, text = "End time").grid(row = 5, column = 0,sticky = "ew")
    inputEntry = tk.Entry(newWindow)
    inputEntry.insert(0, file_text)
    inputEntry.grid(row = 0, column = 1)
    statEntry = tk.Entry(newWindow)
    statEntry.grid(row = 1, column = 1)
    startDateEntry = tk.Entry(newWindow)
    startDateEntry.insert(0, date_text)
    startDateEntry.grid(row = 2, column = 1)
    startTimeEntry = tk.Entry(newWindow)
    startTimeEntry.insert(0, time_text)
    startTimeEntry.grid(row = 3, column = 1)
    endDateEntry = tk.Entry(newWindow)
    endDateEntry.insert(0, date_text)
    endDateEntry.grid(row = 4, column = 1)
    endTimeEntry = tk.Entry(newWindow)
    endTimeEntry.insert(0, time_text)
    endTimeEntry.grid(row = 5, column = 1)
    btn = tk.Button(newWindow, text = "Run", command = allSteps, width = 10)
    btn.grid(row = 6, column = 0, sticky = "w")
    btn_daily = tk.Button(newWindow, text = "Daily", command=lambda:statEntry.insert(tk.END,"Daily"), width = 10)
    btn_daily.grid(row = 7, column = 0,sticky = "w")
    btn_hourly = tk.Button(newWindow, text = "Hourly", command=lambda:statEntry.insert(tk.END, "Hourly"), width = 10)
    btn_hourly.grid(row = 7, column = 1,sticky = "e")
    btn_slice = tk.Button(newWindow, text = "Slice", command = lambda:statEntry.insert(tk.END, "Slice"), width = 10)
    btn_slice.grid(row = 8, column = 0, sticky = "w")
    btn_custom = tk.Button(newWindow, text = "Custom", command = lambda:statEntry.insert(tk.END, "Custom"), width = 10)
    btn_custom.grid(row = 8, column = 1,sticky = "e")
    btn_statclear = tk.Button(newWindow, text = "Clear Stat", command=lambda:statEntry.delete(0, tk.END), width = 10)
    btn_statclear.grid(row = 9, column = 0, sticky = "w")
    btn_quit = tk.Button(newWindow, text = "Quit", command = newWindow.destroy, width = 10)
    btn_quit.grid(row = 6, column = 1, sticky = "e")
    newWindow.bind('<Return>', allSteps)
                                                               
    
def calc_stats():
    newWindow = tk.Tk()
    newWindow.title("Stat Calculations")
    newWindow.geometry("300x250")
    newWindow.config(bg = "#f1dd38")
    date_text = "mm/dd/yyyy"
    time_text = "24:00"
    file_text = "Filename.csv"
    global a1, statEntry, endTimeEntry, startTimeEntry, startDateEntry, endDateEntry
    a = tk.Label(newWindow, text = "Filename").grid(row = 0, column = 0, sticky = "ew")
    b = tk.Label(newWindow, text = "Stats option").grid(row = 1, column = 0, sticky = "ew")
    c = tk.Label(newWindow, text = "StartTime").grid(row = 2, column = 0,sticky = "ew")
    d = tk.Label(newWindow, text = "EndTime").grid(row = 3, column = 0,sticky = "ew")
    e = tk.Label(newWindow, text = "StartDate").grid(row = 4, column = 0,sticky = "ew")
    f = tk.Label(newWindow, text = "EndDate").grid(row = 5, column = 0,sticky = "ew")
    a1 = tk.Entry(newWindow)
    a1.insert(0, file_text)
    a1.grid(row = 0, column = 1)
    statEntry = tk.Entry(newWindow)
    statEntry.grid(row = 1, column = 1)
    startTimeEntry = tk.Entry(newWindow)
    startTimeEntry.insert(0, time_text)
    startTimeEntry.grid(row = 2, column = 1)
    endTimeEntry = tk.Entry(newWindow)
    endTimeEntry.insert(0, time_text)
    endTimeEntry.grid(row = 3, column = 1)
    startDateEntry = tk.Entry(newWindow)
    startDateEntry.insert(0, date_text)
    startDateEntry.grid(row = 4, column = 1)
    endDateEntry = tk.Entry(newWindow)
    endDateEntry.insert(0, date_text)
    endDateEntry.grid(row = 5, column = 1)
    btn = tk.Button(newWindow, text="Submit", command = getStats, width = "10")
    btn_daily = tk.Button(newWindow, text = "Daily", command=lambda:statEntry.insert(tk.END,"Daily"), width = 10)
    btn_daily.grid(row = 7, column = 0,sticky = "w")
    btn_hourly = tk.Button(newWindow, text = "Hourly", command=lambda:statEntry.insert(tk.END, "Hourly"), width = 10)
    btn_hourly.grid(row = 7, column = 1,sticky = "e")
    btn_slice = tk.Button(newWindow, text = "Slice", command = lambda:statEntry.insert(tk.END, "Slice"), width = 10)
    btn_slice.grid(row = 8, column = 0, sticky = "w")
    btn_custom = tk.Button(newWindow, text = "Custom", command = lambda:statEntry.insert(tk.END, "Custom"), width = 10)
    btn_custom.grid(row = 8, column = 1,sticky = "e")
    btn_statclear = tk.Button(newWindow, text = "Clear Stat", command=lambda:statEntry.delete(0, tk.END), width = 10)
    btn_statclear.grid(row = 9, column = 0, sticky = "w")
    btn_quit = tk.Button(newWindow, text = "Quit", command = newWindow.destroy, width = "10")
    btn.grid(row=6, column=0, sticky = "w")
    btn_quit.grid(row = 6, column = 1, sticky = "e")
    newWindow.bind('<Return>', getStats)

def merge_files():
    newWindow = tk.Tk()
    newWindow.title("File Merger")
    newWindow.geometry("230x200")
    newWindow.config(bg = "#f1dd38")
    new_text = "Filename.txt"
    global a1, b1, c1
    a = tk.Label(newWindow, text = "First File").grid(row = 0, column = 0,sticky = "ew")
    b = tk.Label(newWindow, text = "Second file").grid(row = 1, column = 0,sticky = "ew")
    c = tk.Label(newWindow, text = "Merged filename").grid(row = 2, column = 0,sticky = "ew")
    a1 = tk.Entry(newWindow)
    a1.insert(0,new_text)
    a1.grid(row = 0, column = 1, sticky = "ew")
    b1 = tk.Entry(newWindow)
    b1.insert(0, new_text)
    b1.grid(row = 1, column = 1, sticky = "ew")
    c1 = tk.Entry(newWindow)
    c1.insert(0,new_text)
    c1.grid(row = 2, column = 1, sticky = "ew")
    btn = tk.Button(newWindow, text="Submit", command = functionbutton, width = 10)
    btn_quit = tk.Button(newWindow, text = "Quit", command = newWindow.destroy, width = 10)
    btn.grid(row=3, column=0, sticky = "w")
    btn_quit.grid(row = 3, column = 1, sticky = "e")
    newWindow.bind('<Return>', functionbutton)

def mark_Holds():
    newWindow = tk.Tk()
    newWindow.title("Mark holds and samples")
    newWindow.geometry("300x100")
    newWindow.config(bg = "#f1dd38")
    file_text = "Filename.csv"
    global a1
    a =tk.Label(newWindow, text = "Input file").grid(row = 0, column = 0,sticky = "ew")
    a1 = tk.Entry(newWindow)
    a1.insert(0, file_text)
    a1.grid(row = 0, column = 1, sticky = "ew")
    btn = tk.Button(newWindow, text="Confirm", command = columnAvg, width = 10)
    btn.grid(row = 3, column = 0, sticky = "w")
    btn_quit = tk.Button(newWindow, text = "Quit", command = newWindow.destroy, width = 10)
    btn_quit.grid(row = 3, column = 1, sticky = "e")
    newWindow.bind('<Return>', columnAvg)
    
def label_cals():
    global a1
    newWindow = tk.Tk()
    newWindow.title("Label Calibrations")
    newWindow.geometry("250x150")
    newWindow.config(bg = "#f1dd38")
    button_frame = tk.Frame(newWindow)
    button_frame.columnconfigure(0, weight = 1)
    button_frame.columnconfigure(1, weight = 2)
    file_text = "Filename.txt"
    a = tk.Label(newWindow, text = "Input File").grid(row = 0, column = 0,sticky = "ew")
    a1 = tk.Entry(newWindow)
    a1.insert(0, file_text)
    a1.grid(row = 0, column = 1, sticky = "ew")
    btn = tk.Button(newWindow, text="Confirm", command = grabColumn, width = 10)
    btn_quit = tk.Button(newWindow, text = "Quit", command = newWindow.destroy, width = 10)
    
    btn.grid(row = 3, column = 0, sticky = "w")
    btn_quit.grid(row = 3, column = 1, sticky = "e")
    newWindow.bind('<Return>', grabColumn)

def format_file():
    newWindow = tk.Tk()
    newWindow.title("Format file for calculations")
    newWindow.geometry("320x100")
    newWindow.config(bg = "#f1dd38")
    file_text = "filename.csv"
    global a1
    a = tk.Label(newWindow, text = "Input File").grid(row = 0, column = 0, sticky = "ew")
    a1 = tk.Entry(newWindow)
    a1.insert(0, file_text)
    a1.grid(row = 0, column = 1, sticky = "ew")
    btn = tk.Button(newWindow, text="Confirm", command = removespaces, width = 10)
    btn_quit = tk.Button(newWindow, text = "Quit", command = newWindow.destroy, width = 10)
    btn.grid(row = 3, column = 0, sticky = "w")
    
    btn_quit.grid(row = 3, column = 1, sticky = "e")
    newWindow.bind('<Return>', removespaces)
    
window = tk.Tk()
window.title("Sulfur Data Manager Ver2.0 WIP")
window.rowconfigure(0, minsize = 500, weight = 1)
window.columnconfigure(1, minsize = 500, weight = 1)
window.config(bg = "#353FE8")

txt_edit = tk.Text(window, highlightthickness = 3, highlightbackground = "#111")
fr_buttons = tk.Frame(window, bg = "#f1dd38", highlightthickness = 3, highlightbackground = "#111")
terminal = tk.Frame(window, bg = "#f1dd38")

btn_open = tk.Button(fr_buttons, text = "Open", command = open_file)
btn_save = tk.Button(fr_buttons, text = "Save", command = save_file)
btn_readme = tk.Button(fr_buttons, text = "Readme", command = readME_file)
btn_runall = tk.Button(fr_buttons, text = "Run All", command = runAll, bg = "#6EEC77")
btn_merge = tk.Button(fr_buttons, text = "Merge", command = merge_files)
btn_labelCals = tk.Button(fr_buttons, text = "Label Calibrations", command = label_cals)
btn_markHolds = tk.Button(fr_buttons, text = "Mark Holds", command = mark_Holds)
btn_format = tk.Button(fr_buttons, text = "Format", command = format_file)
btn_stats = tk.Button(fr_buttons, text = "Calculate", command = calc_stats)
btn_delete = tk.Button(fr_buttons, text = "Delete", command = delete_file)
btn_quit = tk.Button(fr_buttons, text = "Quit", command = exit_program, bg = "#EC6E6E")

btn_open.grid(row = 1, column = 0, sticky="ew", padx=5, pady = (5,0)) #top 0
btn_save.grid(row = 2, column = 0, sticky="ew", padx=5)
btn_readme.grid(row = 3, column = 0, sticky="ew", padx=5) ##1
btn_runall.grid(row = 4, column = 0, sticky="ew", padx=5, pady = 5) ##2
btn_merge.grid(row = 5, column = 0, sticky="ew", padx=5) ##3
btn_labelCals.grid(row = 6, column = 0, sticky="ew", padx=5) ##4
btn_markHolds.grid(row = 7, column = 0, sticky="ew", padx=5) ##5
btn_format.grid(row = 8, column = 0, sticky="ew", padx=5) ##6
btn_stats.grid(row = 9, column = 0, sticky="ew", padx=5) ##7
btn_delete.grid(row = 10, column = 0, sticky="ew", padx=5)##8
btn_quit.grid(row = 11, column = 0, sticky="ew", padx=5, pady = 5) #bottom 9
fr_buttons.grid(row = 0, column = 0, sticky = "ns")
txt_edit.grid(row = 0, column = 1, padx = 10, pady = 5, sticky = "nsew")
terminal.grid(row = 1, column = 0, columnspan = 2,sticky = "nsew")
window.mainloop()
