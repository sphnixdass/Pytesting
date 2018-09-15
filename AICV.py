# import the necessary packages
import numpy as np
import argparse
import imutils
import cv2
import sys
import os
import csv
import subprocess
import getpass
from PIL import Image
from numpy import genfromtxt
from sklearn import datasets, svm, metrics
from subprocess import Popen


def imagetest():

    im = cv2.imread(getpass.getuser() + 'DInputPage1r.png')
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    blur3 = cv2.GaussianBlur(thresh,(5,5),0)
    cv2.imwrite(getpass.getuser() + 'DInputPage1t.png',blur3)
    
    
def createcsv():
    im = cv2.imread(getpass.getuser() + 'DInputPage1r.png')
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    blur3 = cv2.GaussianBlur(thresh,(5,5),0)
    cv2.imwrite(getpass.getuser() + 'DInputPage1t.png',blur3)
    im3, contours3,hierarchy3 = cv2.findContours(blur3,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    print(len(contours3))
    for c3 in contours3:
        x3,y3,w3,h3 = cv2.boundingRect(c3)
        with open(getpass.getuser() + "Split2.csv", 'a') as f:
            writer = csv.writer(f)
            writer.writerow(cv2.boundingRect(c3))
              #writer.writerow(cv2.boundingRect(c))


def createchimg():
    im = cv2.imread(getpass.getuser() + 'DInputPage1r.png')
    with open(getpass.getuser() + "Split3.csv") as fh:
        csv_reader = csv.reader (fh)
        for row in csv_reader:
            #print(row)
            new_img=im[int(row[1]):int(row[1])+int(row[3]),int(row[0]):int(row[0])+int(row[2])]
            cv2.imwrite('temp/' + str(row[4]) + 'Dval' + 'x' + str(row[0]) + 'y' + str(row[1])  + 'w' + str(row[2])  + 'h' + str(row[3]) + '.png',new_img)


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
        cv2.imwrite(str(fname).replace(".png","mt.png"),new_img3)
        #further check
##        templateu = cv2.imread('TemplateUnited.png',0)
##        res2 = cv2.matchTemplate(new_img3,templateu,cv2.TM_CCORR_NORMED)
##        print(cv2.minMaxLoc(res2))
##        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res2)
##        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
##            top_left = min_loc
##        else:
##            top_left = max_loc
##        #threshold = 0.9
##        loc = np.where( res2 >= threshold)
##        for pt2 in zip(*loc[::-1]):
##            print("united match", pt)
##            new_img4=img[pt[1]-20:pt[1] + h +300,1:width]
##            cv2.imwrite(str(fname).replace(".png","mt1.png"),new_img4)
##            imagecontours(new_img4)
    #bottom_right = (top_left[0] + w, top_left[1] + h)
    #cv2.rectangle(img,top_left, bottom_right, 150, 2)
        cv2.imwrite(str(fname).replace(".png","m.png"),img)

def imagecontours(imgth):
    im2, contours,hierarchy = cv2.findContours(imgth,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    y2= 1
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        
        if w>20 and h>60 and h<130 and (y2-y) > 3:
            print(str((y2-y)))
            new_img3=im2[y:y+h,x:x+w]
            cv2.imwrite(getpass.getuser() + "test" + str(x) + " " +str(y) + ".png",new_img3)
        y2 = y

def templatematch(fname,tname):
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
        cv2.imwrite(str(fname).replace(".png","mt.png"),new_img3)
    #bottom_right = (top_left[0] + w, top_left[1] + h)
    #cv2.rectangle(img,top_left, bottom_right, 150, 2)
        cv2.imwrite(str(fname).replace(".png","m.png"),img)
        
def removefile():
    for item in os.listdir():
        if item.startswith(getpass.getuser() + 'DInputPage'):
            os.remove(item)

def createbat(fname):
    getpagecount(fname)
    file = open(getpass.getuser() + "pagecount.txt", "r")
    pagecount = int(file.read())
    f = open(getpass.getuser() + 'GS2.bat','w')
    for x in range(pagecount):
        f.write('"C:\Temp\Dass\Software\gs9.19\\bin\gswin64c.exe" -dNOPAUSE -dBATCH -dFirstPage=' + str(x + 1) + ' -dLastPage=' + str(x+1) + ' -sDEVICE=png16m -r200x200 -sOutputFile="' + getpass.getuser() + 'DInputPage' + str(x+1) + '.png" ' + fname + '\n')
    f.close()

def mainprocess():
    #print(
    createbat(getpass.getuser() + 'Input.pdf')
    removefile()
    p = Popen(getpass.getuser() + "GS2.bat")
    stdout, stderr = p.communicate()
    print(stdout,stderr)
    for item in os.listdir():
        if item.startswith(getpass.getuser() + 'DInputPage'):
            roteimage(item)

    for item in os.listdir():
        if item.endswith('r.png'):
            templatematchtax(item,'TaxResidency.png')


def getpagecount(fname):
    if os.path.exists(getpass.getuser() + "pagecount.txt"):
        os.remove(getpass.getuser() + "pagecount.txt")
    else:
        pass
        #print("The file does not exist")
  
    filename = fname
    f = open(getpass.getuser() + 'pagecount.bat','w')
    f.write('"C:\Temp\Dass\Software\gs9.19\\bin\gswin64c.exe" -q -dNODISPLAY -c "(' + filename + ') (r) file runpdfbegin pdfpagecount = quit" > ' + getpass.getuser() +  'pagecount.txt')
    f.close()
    p = Popen(getpass.getuser() + "pagecount.bat")
    stdout, stderr = p.communicate()
    
    #print(stdout,stderr)
    #file = open("pagecount.txt", "r") 
    #print(file.read())

    
def testing():
    
    resultimg= ""
    for item in os.listdir("static/"):
        if ('_result_' in item) and (getpass.getuser() in item):
            a,b,c,d,e,f = str(item).split("_")
            d1, d2 = f.split("Page")
            d3 = int(d2.replace(".png",""))
            resultimg = resultimg + (getpass.getuser() + " : " + str(b) + " : " + str(d3) + " : " + str(e)) + ","
            print((getpass.getuser() + " : " + str(b) + " : " + str(d3) + " : " + str(e))) 

testing()           
#mainprocess()            
#imagetest()
#roteimage()
#createcsv()
#createchimg()
#templatematch()

##def createcsv():
##    im = cv2.imread('DInputPage1r.png')
##    gray3 = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
##    blur3 = cv2.GaussianBlur(gray3,(5,5),0)
##    thresh3 = cv2.adaptiveThreshold(blur3,255,1,1,11,2)
##    #cv2.imwrite('DInputPage1t.png',blur3)
##    im3, contours3,hierarchy3 = cv2.findContours(thresh3,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
##    print(len(contours3))
##    for c3 in contours3:
##        x3,y3,w3,h3 = cv2.boundingRect(c3)
##        with open("Split2.csv", 'a') as f:
##            writer = csv.writer(f)
##            writer.writerow(cv2.boundingRect(c3))
##              #writer.writerow(cv2.boundingRect(c))
##            
