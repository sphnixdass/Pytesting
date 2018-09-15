#!/usr/bin/env python
import os, os.path
import win32com.client
import sqlite3
import threading
import numpy as np
import selenium.webdriver.chrome.service as service
import time
import psutil
import numpy as np
import argparse
import imutils
import cv2
import sys
import csv
import subprocess
import getpass
from PIL import Image
from numpy import genfromtxt
from sklearn import datasets, svm, metrics
from subprocess import Popen
from threading import Lock
from flask import Flask, render_template, session, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from threading import Thread


resultimg = ""
Customer_ID = ""
Surname = ""
First_Name = ""
Other_Names = ""
Title = ""
suffix = ""
Salutation = ""
Gender = ""
Deceased_Date = ""
Date_of_Birth = ""
Country_of_birth = ""
Place_of_Birth = ""
Tax_Residence1 = ""
Tax_Residence2 = ""
Tax_Residence3 = ""
Tax_Residence4 = ""
Tax_Residence5 = ""
Tax_Residence6 = ""
Tax_Residence7 = ""
Tax_Residence8 = ""
Tax_Residence9 = ""
Tax_Residence10 = ""
Tax_Reference_no_1 = ""
Tax_Reference_no_2 = ""
Tax_Reference_no_3 = ""
Tax_Reference_no_4 = ""
Tax_Reference_no_5 = ""
Tax_Reference_no_6 = ""
Tax_Reference_no_7 = ""
Tax_Reference_no_8 = ""
Tax_Reference_no_9 = ""
Tax_Reference_no_10 = ""
permanet_add_1 = ""
permanet_add_2 = ""
permanet_add_3 = ""
permanet_add_4 = ""
permanet_add_5 = ""
PostCode = ""
Country_of_Residence = ""
Home_No = ""
Business_No = ""
Mobile_No = ""
Email_Add = ""
Nanpa_Country_Home = ""
Nanpa_Code_Home = ""
Nanpa_Country_Bus = ""
Nanpa_Code_Bus = ""
Nanpa_Country_Mob = ""
Nanpa_Code_Mob = ""
Tax_Reference_no_1 = ""
Tax_Reference_no_2 = ""
Tax_Reference_no_3 = ""
Tax_Reference_no_4 = ""
Tax_Reference_no_5 = ""
Tax_Reference_no_6 = ""
Tax_Reference_no_7 = ""
Tax_Reference_no_8 = ""
Tax_Reference_no_9 = ""
Tax_Reference_no_10 = ""
threadflag = 0
caseref = ""
globalfilename = ""
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

tempsplit = ""

@app.route('/')
def index():
    return render_template('indextesting.html', async_mode=socketio.async_mode)


@socketio.on('my_event', namespace='/test')
def test_message(message):
    global tempsplit
    print("my-event trigger")
    tempsplit = message['data']
    runmacro()
    #print("dasssssss " + message['data'])
    #session['receive_count'] = session.get('receive_count', 0) + 1
    #emit('my_response_dass',
    #     {'data': message['data'], 'count': session['receive_count']})
    emit('my_bo',
         {'CIN': Customer_ID, 'Name': Salutation, 'Country_of_birth': Country_of_birth, 'Tax_Residence1': Tax_Residence1, 'Tax_Residence2': Tax_Residence2, 'Tax_Residence3': Tax_Residence3, 'Tax_Residence4': Tax_Residence4, 'Tax_Residence5': Tax_Residence5, 'Tax_Residence6': Tax_Residence6, 'Tax_Residence7': Tax_Residence7, 'Tax_Residence8': Tax_Residence8, 'Tax_Residence9': Tax_Residence9})
    emit('img_result',
         {'img_resultss': resultimg})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


@socketio.on('my_eventtesting', namespace='/test')
def bo_data(message):
    global Customer_ID
    emit('my_bo',
         {'CIN': Customer_ID, 'Name': Salutation})
    

#from subprocess import Popen
#p = Popen("batch.bat", cwd=r"C:\Path\to\batchfolder")
#stdout, stderr = p.communicate()



    


def roteimage(fname):
    image = cv2.imread(fname)
    
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh>0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h,w)=image.shape[:2]
    center = (w//2,h//2)
    M = cv2.getRotationMatrix2D(center,angle,1.0)
    image2 = cv2.imread(fname)
    rotated = cv2.warpAffine(image2,M,(w,h),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
    #cv2.putText(rotated,"Angle: {:.2f} degrees".format(angle),(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
    print("[INFO] angel: {:3f}".format(angle))
    #cv2.imshow("Rotated",rotated)
    gray = cv2.cvtColor(rotated,cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    blur3 = cv2.GaussianBlur(thresh,(5,5),0)
    gray3 = cv2.bitwise_not(blur3)
    cv2.imwrite(str(fname).replace(".png","r.png"),gray3)
    #cv2.imwrite(str(fname).replace(".png","r.png"),rotated)
    #cv2.waitKey(0)

def templatematchtax(fname,tname):
    img = cv2.imread(fname,0)
    img2 = img.copy()
    template = cv2.imread(tname,0)
    w, h = template.shape[::-1]

    img = img2.copy()
    method = 'cv.TM_CCOEFF_NORMED'
    # Apply template Matching
    #cv2.TM_CCORR_NORMED
    
    res = cv2.matchTemplate(img,template,cv2.TM_CCORR_NORMED)
    print(cv2.minMaxLoc(res))
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    threshold = 0.98
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        print("dass", pt,res)
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (150,150,0), 3)
        height, width = img.shape
        #new_img3=img[pt[1]:pt[1] + h +20,pt[0]:pt[0] + w+80]
        new_img3=img[pt[1]-20:pt[1] + h +40,1:width]
        temptname = str(tname).replace(".png","")
        print(temptname)
        cv2.imwrite("static/" + str(getpass.getuser() + '_' + temptname + '_result_' + fname).replace("r.png",".png"),new_img3)
        cv2.imwrite("static/" +str(getpass.getuser() + '_' + temptname + fname).replace(".png","m.png"),img)


def removefile():
    for item in os.listdir():
        if item.startswith(getpass.getuser()) and item != 'selvgnb_123456_Input.pdf' and item != 'selvgnb_123457_Input.pdf':
            os.remove(item)

    for item2 in os.listdir("static/"):
        file_path = os.path.join("static/", item2)
        if item2.startswith(getpass.getuser()) and item2 != 'selvgnb_123456_Input.pdf' and item2 != 'selvgnb_123457_Input.pdf':
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    #os.remove(item2)
            except:
                print("unable to delete " + item2)
                



def createbat(fname):
    global globalfilename
    global caseref
    getpagecount(fname)
    file = open(getpass.getuser() + "pagecount.txt", "r")
    pagecount = int(file.read())
    f = open(getpass.getuser() + 'GS2.bat','w')
    for x in range(pagecount):
        #f.write('"C:\Program Files\gs\gs9.19\\bin\gswin64c.exe" -dNOPAUSE -dBATCH -dFirstPage=' + str(x + 1) + ' -dLastPage=' + str(x+1) + ' -sDEVICE=png16m -r200x200 -sOutputFile="' + getpass.getuser() + 'DInputPage' + str(x+1) + '.png" ' + fname + '\n')
        f.write('"C:\Temp\Dass\Software\gs9.19\\bin\gswin64c.exe" -dNOPAUSE -dBATCH -dFirstPage=' + str(x + 1) + ' -dLastPage=' + str(x+1) + ' -sDEVICE=png16m -r200x200 -sOutputFile="' + getpass.getuser() + '_'  + caseref + '_' + 'DInputPage' + str(x+1) + '.png" ' + globalfilename + '\n')
    f.close()

def mainprocess():
    global caseref
    global globalfilename
    filepath = getpass.getuser() + "_caseref.txt"  
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            globalfilename = str(line.strip())
            print("Line {}: {}".format(cnt, globalfilename))
            a,b,c = globalfilename.split("_")
            caseref = b
            print("case ref" + caseref)
            line = fp.readline()
            cnt += 1
            print("image spring is running")
            createbat(globalfilename)
            #createbat('DassInput.pdf')

            p = Popen(getpass.getuser() + "GS2.bat")
            stdout, stderr = p.communicate()
            print(stdout,stderr)
            for item in os.listdir():
                if (getpass.getuser() in item) and (caseref in item) and ('DInputPage' in item) and item.endswith('r.png') == False:
                    roteimage(item)

            for item in os.listdir():
                if (getpass.getuser() in item) and (caseref in item) and ('DInputPage' in item) and item.endswith('r.png'):
                    templatematchtax(item,'TaxResidency.png')
                    templatematchtax(item,'statementfrequency.png')

            get_result_image()


def getpagecount(fname):
    global globalfilename
    if os.path.exists(getpass.getuser() + "pagecount.txt"):
        os.remove(getpass.getuser() + "pagecount.txt")
    else:
        pass
        #print("The file does not exist")
  
    
    f = open(getpass.getuser() + 'pagecount.bat','w')
    #f.write('"C:\Program Files\gs\gs9.19\\bin\gswin64c.exe" -q -dNODISPLAY -c "(' + filename + ') (r) file runpdfbegin pdfpagecount = quit" > ' + getpass.getuser() +  'pagecount.txt')
    f.write('"C:\Temp\Dass\Software\gs9.19\\bin\gswin64c.exe" -q -dNODISPLAY -c "(' + globalfilename+ ') (r) file runpdfbegin pdfpagecount = quit" > ' + getpass.getuser() +  'pagecount.txt')
    f.close()
    p = Popen(getpass.getuser() + "pagecount.bat")
    stdout, stderr = p.communicate()
    
    #print(stdout,stderr)
    #file = open("pagecount.txt", "r") 
    #print(file.read())

def get_result_image():
    global resultimg
    resultimg= ""
    for item in os.listdir("static/"):
        if ('_result_' in item) and (getpass.getuser() in item):
            a,b,c,d,e,f = str(item).split("_")
            d1, d2 = f.split("Page")
            d3 = int(d2.replace(".png",""))
            resultimg = resultimg + (getpass.getuser() + " : " + str(b) + " : " + str(d3) + " : " + str(e)) + ","
            print((getpass.getuser() + " : " + str(b) + " : " + str(d3) + " : " + str(e))) 



def runmacro():
    print("running macro")
    removefile()
    global Customer_ID
    global Surname
    global First_Name
    global Other_Names
    global Title
    global suffix
    global Salutation
    global Gender
    global Deceased_Date
    global Date_of_Birth
    global Country_of_birth
    global Place_of_Birth
    global Tax_Residence1
    global Tax_Residence2
    global Tax_Residence3
    global Tax_Residence4
    global Tax_Residence5
    global Tax_Residence6
    global Tax_Residence7
    global Tax_Residence8
    global Tax_Residence9
    global Tax_Residence10
    global Tax_Reference_no_1
    global Tax_Reference_no_2
    global Tax_Reference_no_3
    global Tax_Reference_no_4
    global Tax_Reference_no_5
    global Tax_Reference_no_6
    global Tax_Reference_no_7
    global Tax_Reference_no_8
    global Tax_Reference_no_9
    global Tax_Reference_no_10
    global permanet_add_1
    global permanet_add_2
    global permanet_add_3
    global permanet_add_4
    global permanet_add_5
    global PostCode
    global Country_of_Residence
    global Home_No
    global Business_No
    global Mobile_No
    global Email_Add
    global Nanpa_Country_Home
    global Nanpa_Code_Home
    global Nanpa_Country_Bus
    global Nanpa_Code_Bus
    global Nanpa_Country_Mob
    global Nanpa_Code_Mob
    global Tax_Reference_no_1
    global Tax_Reference_no_2
    global Tax_Reference_no_3
    global Tax_Reference_no_4
    global Tax_Reference_no_5
    global Tax_Reference_no_6
    global Tax_Reference_no_7
    global Tax_Reference_no_8
    global Tax_Reference_no_9
    global Tax_Reference_no_10
    
    global tempsplit
    global xl
    global threadflag
    #if os.path.exists("AI_CTO.xlsm"):
    #xl=win32com.client.Dispatch("Excel.Application")
    #xl.Workbooks.Open(os.path.abspath("AI_CTO.xlsm"), ReadOnly=1)
    if os.path.exists("AI_CTO.xlsm"):
        print("xl object")
        xl=win32com.client.Dispatch("Excel.Application")
        xl.Workbooks.Open(os.path.abspath("AI_CTO.xlsm"), ReadOnly=0)
        wsref = xl.Worksheets("Ref")
    else:
        print("Unable to open the excel")
        
    ws = xl.Worksheets("Ref")
    wsbo = xl.Worksheets("BOData")
    #ws.Cells(1,1).Value = "Cell A1"
    #ws.Cells(1,1).Offset(2,4).Value = "Cell D2"
    a,s,c = tempsplit.split(":")
    ws.Range("B1").Value = a
    ws.Range("B2").Value = s
    ws.Range("B3").Value = c
    xl.Application.Run("AI_CTO.xlsm!ModProcess.testing")
    
    #xl.Application.Run("AI_CTO.xlsm!ModProcess.BOExtract")
    xl.DisplayAlerts = False 
    xl.Application.Save() # if you want to save then uncomment this line and change delete the ", ReadOnly=1" part from the open function.
    xl.DisplayAlerts = True

    Customer_ID = wsbo.Range("G2").Value
    Surname = wsbo.Range("H2").Value
    First_Name = wsbo.Range("I2").Value
    Other_Names = wsbo.Range("J2").Value
    Title = wsbo.Range("K2").Value
    suffix = wsbo.Range("L2").Value
    Salutation = wsbo.Range("M2").Value
    Gender = wsbo.Range("N2").Value
    Deceased_Date = wsbo.Range("O2").Value
    Date_of_Birth = wsbo.Range("P2").Value
    Country_of_birth = wsbo.Range("Q2").Value
    Place_of_Birth = wsbo.Range("R2").Value
    Tax_Residence1 = wsbo.Range("AA2").Value
    Tax_Residence2 = wsbo.Range("AB2").Value
    Tax_Residence3 = wsbo.Range("AC2").Value
    Tax_Residence4 = wsbo.Range("AD2").Value
    Tax_Residence5 = wsbo.Range("AE2").Value
    Tax_Residence6 = wsbo.Range("AF2").Value
    Tax_Residence7 = wsbo.Range("AG2").Value
    Tax_Residence8 = wsbo.Range("AH2").Value
    Tax_Residence9 = wsbo.Range("AI2").Value
    Tax_Residence10 = wsbo.Range("AJ2").Value
    Tax_Reference_no_1 = wsbo.Range("AK2").Value
    Tax_Reference_no_2 = wsbo.Range("AL2").Value
    Tax_Reference_no_3 = wsbo.Range("AM2").Value
    Tax_Reference_no_4 = wsbo.Range("AN2").Value
    Tax_Reference_no_5 = wsbo.Range("AO2").Value
    Tax_Reference_no_6 = wsbo.Range("AP2").Value
    Tax_Reference_no_7 = wsbo.Range("AQ2").Value
    Tax_Reference_no_8 = wsbo.Range("AR2").Value
    Tax_Reference_no_9 = wsbo.Range("AS2").Value
    Tax_Reference_no_10 = wsbo.Range("AT2").Value
    permanet_add_1 = wsbo.Range("AV2").Value
    permanet_add_2 = wsbo.Range("AW2").Value
    permanet_add_3 = wsbo.Range("AX2").Value
    permanet_add_4 = wsbo.Range("AY2").Value
    permanet_add_5 = wsbo.Range("AZ2").Value
    PostCode = wsbo.Range("BA2").Value
    Country_of_Residence = wsbo.Range("BB2").Value
    Home_No = wsbo.Range("BC2").Value
    Business_No = wsbo.Range("BD2").Value
    Mobile_No = wsbo.Range("BE2").Value
    Email_Add = wsbo.Range("BF2").Value
    Nanpa_Country_Home = wsbo.Range("BJ2").Value
    Nanpa_Code_Home = wsbo.Range("BK2").Value
    Nanpa_Country_Bus = wsbo.Range("BL2").Value
    Nanpa_Code_Bus = wsbo.Range("BM2").Value
    Nanpa_Country_Mob = wsbo.Range("BN2").Value
    Nanpa_Code_Mob = wsbo.Range("BO2").Value
    Tax_Reference_no_1 = wsbo.Range("BP2").Value
    Tax_Reference_no_2 = wsbo.Range("BQ2").Value
    Tax_Reference_no_3 = wsbo.Range("BR2").Value
    Tax_Reference_no_4 = wsbo.Range("BS2").Value
    Tax_Reference_no_5 = wsbo.Range("BT2").Value
    Tax_Reference_no_6 = wsbo.Range("BU2").Value
    Tax_Reference_no_7 = wsbo.Range("BV2").Value
    Tax_Reference_no_8 = wsbo.Range("BW2").Value
    Tax_Reference_no_9 = wsbo.Range("BX2").Value
    Tax_Reference_no_10 = wsbo.Range("BY2").Value


    print("Customer_ID : " + str(Customer_ID))
    xl.Application.Quit() # Comment this out if your excel script closes
    #if threadflag == 0:
        
    #    threadflag = 1
    #    threading.Thread(target=mainprocess).start()
        
    mainprocess()
    #del xl

 
def clarevar():
    global Customer_ID
    global Surname
    global First_Name
    global Other_Names
    global Title
    global suffix
    global Salutation
    global Gender
    global Deceased_Date
    global Date_of_Birth
    global Country_of_birth
    global Place_of_Birth
    global Tax_Residence1
    global Tax_Residence2
    global Tax_Residence3
    global Tax_Residence4
    global Tax_Residence5
    global Tax_Residence6
    global Tax_Residence7
    global Tax_Residence8
    global Tax_Residence9
    global Tax_Residence10
    global Tax_Reference_no_1
    global Tax_Reference_no_2
    global Tax_Reference_no_3
    global Tax_Reference_no_4
    global Tax_Reference_no_5
    global Tax_Reference_no_6
    global Tax_Reference_no_7
    global Tax_Reference_no_8
    global Tax_Reference_no_9
    global Tax_Reference_no_10
    global permanet_add_1
    global permanet_add_2
    global permanet_add_3
    global permanet_add_4
    global permanet_add_5
    global PostCode
    global Country_of_Residence
    global Home_No
    global Business_No
    global Mobile_No
    global Email_Add
    global Nanpa_Country_Home
    global Nanpa_Code_Home
    global Nanpa_Country_Bus
    global Nanpa_Code_Bus
    global Nanpa_Country_Mob
    global Nanpa_Code_Mob
    global Tax_Reference_no_1
    global Tax_Reference_no_2
    global Tax_Reference_no_3
    global Tax_Reference_no_4
    global Tax_Reference_no_5
    global Tax_Reference_no_6
    global Tax_Reference_no_7
    global Tax_Reference_no_8
    global Tax_Reference_no_9
    global Tax_Reference_no_10

    Customer_ID = ""
    Surname = ""
    First_Name = ""
    Other_Names = ""
    Title = ""
    suffix = ""
    Salutation = ""
    Gender = ""
    Deceased_Date = ""
    Date_of_Birth = ""
    Country_of_birth = ""
    Place_of_Birth = ""
    Tax_Residence1 = ""
    Tax_Residence2 = ""
    Tax_Residence3 = ""
    Tax_Residence4 = ""
    Tax_Residence5 = ""
    Tax_Residence6 = ""
    Tax_Residence7 = ""
    Tax_Residence8 = ""
    Tax_Residence9 = ""
    Tax_Residence10 = ""
    Tax_Reference_no_1 = ""
    Tax_Reference_no_2 = ""
    Tax_Reference_no_3 = ""
    Tax_Reference_no_4 = ""
    Tax_Reference_no_5 = ""
    Tax_Reference_no_6 = ""
    Tax_Reference_no_7 = ""
    Tax_Reference_no_8 = ""
    Tax_Reference_no_9 = ""
    Tax_Reference_no_10 = ""
    permanet_add_1 = ""
    permanet_add_2 = ""
    permanet_add_3 = ""
    permanet_add_4 = ""
    permanet_add_5 = ""
    PostCode = ""
    Country_of_Residence = ""
    Home_No = ""
    Business_No = ""
    Mobile_No = ""
    Email_Add = ""
    Nanpa_Country_Home = ""
    Nanpa_Code_Home = ""
    Nanpa_Country_Bus = ""
    Nanpa_Code_Bus = ""
    Nanpa_Country_Mob = ""
    Nanpa_Code_Mob = ""
    Tax_Reference_no_1 = ""
    Tax_Reference_no_2 = ""
    Tax_Reference_no_3 = ""
    Tax_Reference_no_4 = ""
    Tax_Reference_no_5 = ""
    Tax_Reference_no_6 = ""
    Tax_Reference_no_7 = ""
    Tax_Reference_no_8 = ""
    Tax_Reference_no_9 = ""
    Tax_Reference_no_10 = ""



if __name__ == '__main__':
    socketio.run(app, debug=True)
