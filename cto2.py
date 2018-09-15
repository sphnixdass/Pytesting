from flask import Flask, redirect, url_for, render_template, request
import win32com.client
from time import sleep
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import threading
import numpy as np
import selenium.webdriver.chrome.service as service
import time
import psutil


db = sqlite3.connect('example.db')


options = webdriver.ChromeOptions()
options.add_experimental_option("useAutomationExtension",False)
options.binary_location = "D:\\Users\\selvgnb\\AppData\\Local\\Microsoft\\AppV\\Client\\Integration\\6F327610-34BD-42B9-8795-5D70F9F4F77D\\Root\\VFS\\ProgramFilesX86\\Google\\Chrome\\Application\\chrome.exe"
chrome_driver_binary = "X:\\Coding\\Python\\Selenium\\chromedriver.exe"
    


#ie = win32com.client.Dispatch("InternetExplorer.Application")


def dbcreate():
    global db
    cursor = db.cursor()
    #cursor.execute('''CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT,
    #                   phone TEXT, email TEXT unique, password TEXT)''')
    cursor.execute('''CREATE TABLE dasstable(id INTEGER PRIMARY KEY, sl TEXT, companyname TEXT,
                       outerhtml TEXT, strurl TEXT, findword TEXT, status TEXT)''')
   
    db.commit()

def dbdrop():
    global db
    cursor = db.cursor()
    cursor.execute('''DROP TABLE dasstable''')
    db.commit()

def dbdelete():
    global db
    cursor = db.cursor()
    cursor.execute('''DELETE FROM dasstable''')
    db.commit()


def dbinsert(sl, companyname, outerhtml, strurl, findword, status):
    global db
    cursor = db.cursor()
    cursor.execute('''INSERT INTO dasstable(sl, companyname, outerhtml, strurl, findword, status) VALUES(?,?,?,?,?,?)''', (sl, companyname, outerhtml, strurl, findword, status))
    db.commit()


def dbselect():
    global db
    cursor = db.cursor()
    cursor.execute('''SELECT sl, companyname, outerhtml, strurl, findword, status FROM dasstable''')
    #user1 = cursor.fetchone() #retrieve the first row
    #print(user1[0]) #Print the first column retrieved(user's name)
    all_rows = cursor.fetchall()
    for row in all_rows:
        # row[0] returns the first column in the query (name), row[1] returns email column.
        print('{0}, {1}, {2}, {3}, {4},{5}'.format(row[0], row[1], row[2], row[3], row[4], row[5]))
    

def dbclose():
    global db
    db.close()






temprc = 1
arrtemp = np.array(range(1000), dtype='a1000').reshape(250,4)

def chrome2():
    
    driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
    driver.implicitly_wait(20)
    time.sleep(3)
    
    for x in range(3):
        db = sqlite3.connect('example.db')
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM dasstable WHERE status = "Yet to Start" LIMIT 1''')
        all_rows = cursor.fetchall()
        tempurl = ""
        tempsl = ""
        #print(all_rows)
        for row in all_rows:
            tempurl = row[4]
            tempsl = row[1]
            print("sssss" + tempurl)

        print("tempsl  : " + str(tempsl))
        #db.close()
        #db = sqlite3.connect('example.db')
        db.execute("UPDATE dasstable SET status='Started' WHERE sl='" + str(tempsl) + "'")
        db.commit()
        #db.close()
        
        

        driver.implicitly_wait(20)
        time.sleep(3)
        driver.get(tempurl)
        driver.implicitly_wait(10)
        time.sleep(3)
        content = driver.find_elements_by_tag_name("html")
        driver.implicitly_wait(20)

        tempcon = ""
        tempcon = content
        for e in content:
            tempcon = e.text

        
        #tempcon = tempcon.decode('utf-8', 'ignore')
        tempcon=tempcon.replace("'","");
        tempcon=tempcon.replace('"','');
        print(tempcon)
        #db = sqlite3.connect('example.db')
        db.execute("UPDATE dasstable SET outerhtml = '" + str(tempcon) + "', status='Completed' WHERE sl='" + str(tempsl) + "'")
        db.commit()
        db.close()
    #db.close()
    #driver.get(tempurl)
    driver.close()
    driver.quit()
    
    
def chromeloop(strtemp):
    global temprc
    global arrtemp
##    options = webdriver.ChromeOptions()
##    #options.add_argument("--disable-extensions")
##    #options.add_argument('--disable-useAutomationExtension')
##    options.add_experimental_option("useAutomationExtension",False)
##    options.binary_location = "D:\\Users\\selvgnb\\AppData\\Local\\Microsoft\\AppV\\Client\\Integration\\6F327610-34BD-42B9-8795-5D70F9F4F77D\\Root\\VFS\\ProgramFilesX86\\Google\\Chrome\\Application\\chrome.exe"
##    #capabilities = {'browserName': 'chrome','chromeOptions':  { 'useAutomationExtension': False, 'forceDevToolsScreenshot': True, 'args': ['--start-maximized', '--disable-infobars'] }}
##    
##    chrome_driver_binary = "X:\\Coding\\Python\\Selenium\\chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
    driver.get("http://www.google.com")
    element = driver.find_element_by_name("q")
    element.send_keys(strtemp)
    element.submit()
    

    for pa in range(2,4):
        content = driver.find_elements_by_class_name('rc')
        tempurl = ""
        for x in content:
            inner_text= driver.execute_script("return arguments[0].innerHTML;", x)
            try:
                urlsp = inner_text.split('<h3')
                urlsp2 = urlsp[1].split('</h3>')
                urlsp3 = urlsp2[0].split('<a href=')
                urlsp4 = urlsp3[1].split('"')
                arrtemp[temprc,0] = urlsp4[1]
                tempurl = urlsp4[1]
            except:
                print("Unable to extract href")
            #print(urlsp4[1])
            
            arrtemp[temprc,1] = strtemp
            arrtemp[temprc,2] = temprc
            arrtemp[temprc,3] = "Yet to Start"
            temprc = temprc + 1
            dbinsert(temprc, strtemp,"",tempurl,"dssd", "Yet to Start")
            
        aele = driver.find_elements_by_tag_name("a")
        aeflag = False
        for ae in aele:
            if aeflag == False:
                if ae.text == str(pa):
                    ae.click()
                    time.sleep(3)
                    aeflag = True
                
            #print(urlsp4[0])
    #print(content)
    #inner_text= driver.execute_script("return arguments[0].innerText;", content)
    #print(inner_text)
    driver.close()
    driver.quit()



#dbcreate()
chromeloop("Infosys + fraud")
t1 = threading.Thread(target=chrome2)  
t2 = threading.Thread(target=chrome2)

t1.start()
t2.start()

t1.join()
t2.join()

#dbinsert("dass","121212","dass@gmail.com","dssd")
#dbinsert("dass2","1212122","dass@gmail.com2","dssd2")
dbselect()
dbdelete()
dbclose()


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))


@app.route('/success/<name>')
def success(name):
    print("success")
    google_extract("www.google.com")
    return 'Hello %s as Guest' % name
    
@app.route('/guest/<guest>')
def hello_guest(guest):
    
    print("hi dass")
    return 'Hello %s as Guest' % guest

@app.route('/hello/<name>')
def hello_name(name):
    if name == 'dass':
        return redirect(url_for('login_screen'))
    else:
        return redirect(url_for('hello_guest', guest = name))
    return 'hello %s!' % name



def google_extract(comp_name):
    global ie
    #ie = win32com.client.Dispatch("InternetExplorer.Application")
    ie.Visible = True
    ie.Navigate(comp_name)
    if ie.Busy:
        sleep(5)
    text = ie.Document.body.innerHTML
    
    text = text.encode('ascii','ignore')
    ie.Quit()
    print(text)
    

#google_extract("www.google.com")
if __name__ =='__main__':
    pass
    #app.run(debug = True)
    
