import os, os.path
import json
import win32com.client
import sqlite3
import threading
import numpy as np
import selenium.webdriver.chrome.service as service
import time
import psutil
import numpy as np
import argparse
import re
import imutils
import cv2
import sys
import csv
import subprocess
import getpass
import ctypes
from shutil import copyfile
#from PIL import Image
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
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pythoncom
from bs4 import BeautifulSoup

Lb1 = ""
pythoncom.CoInitialize()
ShellWindowsCLSID = '{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

@app.route('/result')
def result():
   dict = {'phy':50,'che':60,'maths':70}
   return render_template('Ni', result = dict)

@app.route('/')
def index():
    return render_template('NickName.html', async_mode=socketio.async_mode)


@socketio.on('extract_button', namespace='/test')
def test_message(message):
    #ctypes.windll.user32.MessageBoxW(0, "Process has been completed. please click Show Result button.", "Agile Automation", 0)
    print("Click submit event trigger")
    nickname = str(message['nickname'])
    PostalCode = str(message['PostalCode'])
    full_name(nickname)
   #googlesearchpage = str(message['googlesearchpage'])

    print(message)
    #ctypes.windll.user32.MessageBoxW(0, "Process has been completed. please click Show Result button.", "Agile Automation", 0)

@socketio.on('GenerateReport', namespace='/test')
def fun_generate_report(message):
   global filepathtemp
   conn = sqlite3.connect(filepathtemp + str(getpass.getuser()).lower() + '.db')
   c = conn.cursor()
   c.execute('select * from Master where id = "' + message + '"')
   rows = c.fetchall()
   conn.close()
   print(str(message))
   #print(rows)
   #row = rows[int(message) -1]
   row = rows[0]
   print("Timmer called : " + str(row))
   print("Timmer called : " + str(row[0]))
   emit('my_response_rowclick',
        {'resultdata': str(row[14]).replace('\n', r'<p></p>'), 'AInews': str(row[13]).replace('\n', r'<p></p>'), 'otherwebvar': str(otherwebresult).replace('\n', r'<p></p>') })


def mainprogram():
   if os.path.exists(filepathtemp + str(getpass.getuser()).lower() + ".xlsm"):
      print("Main Program")
      xl=win32com.client.Dispatch("Excel.Application")
      workbook = xl.Workbooks.Open(os.path.abspath(filepathtemp + str(getpass.getuser()).lower() + ".xlsm"), ReadOnly=0)
      ws = workbook.Worksheets("SystemRef")
      ws.Range("C7").Value = str(companyname)


      ws.Range("B20").Value = str(ProfileSearchCheckBox)
      ws.Range("B21").Value = str(WorldCheckBox)
    #ws.Range("B1").Value = str(googlesearchpage)
      xl.DisplayAlerts = False
      xl.Application.Save() # if you want to save then uncomment this line and change delete the ", ReadOnly=1" part from the open function.
      xl.DisplayAlerts = True
      xl.Application.Run(filepathtemp + str(getpass.getuser()).lower() + ".xlsm!ModGoogleSearch.Google_search")
      xl.DisplayAlerts = False
      xl.Application.Save() # if you want to save then uncomment this line and change delete the ", ReadOnly=1" part from the open function.
      xl.DisplayAlerts = True
      workbook.Close(True)

def full_name(nickname):
    global Lb1
    Lb1 = ""
    with open("nicknames.db", 'r') as fin:
        lines = fin.readlines()
        # remove '\n' characters
        clean_lines = [l.strip('\n') for l in lines]
        # split on tab so that we get lists from strings
        A = [cl.split('\t') for cl in clean_lines]
        Lb1 = nickname


        for item in A:
            if item[0].lower().strip() == nickname.lower().strip():
                print(item[1])
                #data_check(item[1], v3.get())
                Lb1 = Lb1 + '<!>' + item[1].lower()

    emit('NickName_responce', {'resultdata': Lb1})


if __name__ == '__main__':
    socketio.run(app, debug=True)
