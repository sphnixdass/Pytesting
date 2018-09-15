from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import threading
import numpy as np
import selenium.webdriver.chrome.service as service
import time
import psutil

#https://selenium-python.readthedocs.io/locating-elements.html

temprc = 1
arrtemp = np.array(range(1000), dtype='a1000').reshape(250,4)


def chromeloop(strtemp):
    global temprc
    global arrtemp
    options = webdriver.ChromeOptions()
    #options.add_argument("--disable-extensions")
    #options.add_argument('--disable-useAutomationExtension')
    options.add_experimental_option("useAutomationExtension",False)
    options.binary_location = "D:\\Users\\selvgnb\\AppData\\Local\\Microsoft\\AppV\\Client\\Integration\\6F327610-34BD-42B9-8795-5D70F9F4F77D\\Root\\VFS\\ProgramFilesX86\\Google\\Chrome\\Application\\chrome.exe"
    #capabilities = {'browserName': 'chrome','chromeOptions':  { 'useAutomationExtension': False, 'forceDevToolsScreenshot': True, 'args': ['--start-maximized', '--disable-infobars'] }}
    
    chrome_driver_binary = "X:\\Coding\\Python\\Selenium\\chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
    driver.get("http://www.google.com")
    element = driver.find_element_by_name("q")
    element.send_keys(strtemp)
    element.submit()
    

    for pa in range(2,4):
        content = driver.find_elements_by_class_name('rc')
        for x in content:
            inner_text= driver.execute_script("return arguments[0].innerHTML;", x)
            try:
                urlsp = inner_text.split('<h3')
                urlsp2 = urlsp[1].split('</h3>')
                urlsp3 = urlsp2[0].split('<a href=')
                urlsp4 = urlsp3[1].split('"')
                arrtemp[temprc,0] = urlsp4[1]
            except:
                print("Unable to extract href")
            #print(urlsp4[1])
            
            arrtemp[temprc,1] = strtemp
            arrtemp[temprc,2] = temprc
            arrtemp[temprc,3] = "Yet to Start"
            temprc = temprc + 1

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


t1 = threading.Thread(target=chromeloop, args=("tcs + fraud",))
t2 = threading.Thread(target=chromeloop, args=("Infosys + fraud",))


t1.start()
t2.start()

t1.join()
t2.join()



def chromeremaing():
    global temprc
    global arrtemp
    options = webdriver.ChromeOptions()
    options.add_experimental_option("useAutomationExtension",False)
    options.binary_location = "D:\\Users\\selvgnb\\AppData\\Local\\Microsoft\\AppV\\Client\\Integration\\6F327610-34BD-42B9-8795-5D70F9F4F77D\\Root\\VFS\\ProgramFilesX86\\Google\\Chrome\\Application\\chrome.exe"
    chrome_driver_binary = "X:\\Coding\\Python\\Selenium\\chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
    procs = psutil.Process(driver.service.process.pid).children(recursive=True)
    for x in range(temprc):
        if arrtemp[x,3].decode('ascii') == 'Yet to Start' or arrtemp[x,3].decode('ascii') == 'started':
            arrtemp[x,3] = 'started'.encode('ascii')
            
            try:
                
                driver.implicitly_wait(10)
                time.sleep(3)
                driver.get(arrtemp[x,0].decode('ascii'))
                driver.implicitly_wait(10)
                time.sleep(3)
                content = driver.find_elements_by_tag_name("html")
                driver.implicitly_wait(10)
                f = open("Doutput" + str(arrtemp[x,2].decode('ascii')).zfill(4) + ".txt", "w",encoding="utf-8")
                for e in content:
                    f.write(e.text)
                f.close()
                arrtemp[x,3] = 'Completed'.encode('ascii')
            except:
                print("Error occured on", x, arrtemp[x,3].decode('ascii'), arrtemp[x,0])
                
                time.sleep(3)
                for p in procs:
                    p.terminate()
                    gone, alive = psutil.wait_procs(procs, timeout=3)
                for p in alive:
                    p.kill()
   
    driver.close()
    driver.quit()



def chromeextract():
    global temprc
    global arrtemp
    options = webdriver.ChromeOptions()
    #options.add_argument("--disable-extensions")
    #options.add_argument('--disable-useAutomationExtension')
    options.add_experimental_option("useAutomationExtension",False)
    options.binary_location = "D:\\Users\\selvgnb\\AppData\\Local\\Microsoft\\AppV\\Client\\Integration\\6F327610-34BD-42B9-8795-5D70F9F4F77D\\Root\\VFS\\ProgramFilesX86\\Google\\Chrome\\Application\\chrome.exe"
    #capabilities = {'browserName': 'chrome','chromeOptions':  { 'useAutomationExtension': False, 'forceDevToolsScreenshot': True, 'args': ['--start-maximized', '--disable-infobars'] }}
    
    chrome_driver_binary = "X:\\Coding\\Python\\Selenium\\chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
    procs = psutil.Process(driver.service.process.pid).children(recursive=True)
    print(procs)

    for x in range(temprc):
        #print(x, arrtemp[x,3].decode('ascii'), arrtemp[x,3])
        if arrtemp[x,3].decode('ascii') == 'Yet to Start':
            arrtemp[x,3] = 'started'.encode('ascii')
            
            try:
                
                driver.implicitly_wait(20)
                time.sleep(3)
                driver.get(arrtemp[x,0].decode('ascii'))
                driver.implicitly_wait(10)
                time.sleep(3)
                content = driver.find_elements_by_tag_name("html")
                driver.implicitly_wait(20)
                f = open("Doutput" + str(arrtemp[x,2].decode('ascii')).zfill(4) + ".txt", "w",encoding="utf-8")
                for e in content:
                    f.write(e.text)
                f.close()
                arrtemp[x,3] = 'Completed'.encode('ascii')
            except:
                print("Error occured on", x, arrtemp[x,3].decode('ascii'), arrtemp[x,0])
                time.sleep(20)
                try:
                    for p in procs:
                        p.terminate()
                        gone, alive = psutil.wait_procs(procs, timeout=3)
                    for p in alive:
                        p.kill()
                except:
                    print("error on killing")
##                options = webdriver.ChromeOptions()
##                options.add_experimental_option("useAutomationExtension",False)
##                options.binary_location = "D:\\Users\\selvgnb\\AppData\\Local\\Microsoft\\AppV\\Client\\Integration\\6F327610-34BD-42B9-8795-5D70F9F4F77D\\Root\\VFS\\ProgramFilesX86\\Google\\Chrome\\Application\\chrome.exe"
##                chrome_driver_binary = "X:\\Coding\\Python\\Selenium\\chromedriver.exe"
##                driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
##                time.sleep(100)
                #return
    driver.close()
    driver.quit()


t1 = threading.Thread(target=chromeextract)  
t2 = threading.Thread(target=chromeextract)
t3 = threading.Thread(target=chromeextract)
t4 = threading.Thread(target=chromeextract)
t5 = threading.Thread(target=chromeextract)

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()




for x in range(temprc):
    if arrtemp[x,3].decode('ascii') == 'Yet to Start' or arrtemp[x,3].decode('ascii') == 'started':
        t1 = threading.Thread(target=chromeextract)  
        t2 = threading.Thread(target=chromeextract)
        t3 = threading.Thread(target=chromeextract)
        t4 = threading.Thread(target=chromeextract)
        t5 = threading.Thread(target=chromeextract)

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        
        t1.exit()
        t2.exit()
        t3.exit()
        t4.exit()
        t5.exit()

        break


print("second loop exe")
for x in range(temprc):
    if arrtemp[x,3].decode('ascii') == 'Yet to Start' or arrtemp[x,3].decode('ascii') == 'started':
        chromeremaing()
        
print("second indi ")
for x in range(temprc):
    if arrtemp[x,3].decode('ascii') == 'Yet to Start' or arrtemp[x,3].decode('ascii') == 'started':
        chromeremaing()


print(arrtemp)
##t2 = threading.Thread(target=chromeloop, args=("caleb",))
##t3 = threading.Thread(target=chromeloop, args=("caleb",))
##t4 = threading.Thread(target=chromeloop, args=("caleb",))
##t5 = threading.Thread(target=chromeloop, args=("caleb",))

##driver2.get("http://www.google.com");
##element = driver2.find_element_by_name("q")
##element.send_keys("pycon")
##element.submit();
##
##driver3.get("http://www.google.com");
##element = driver3.find_element_by_name("q")
##element.send_keys("pycon")
##element.submit();


##t2.start()
##t3.start()
##t4.start()
##t5.start()



##t2.join()
##t3.join()
##t4.join()
##t5.join()


##element = driver.find_element_by_css_selector('rc')
##inner_text= driver.execute_script("return arguments[0].innerText;", element)


