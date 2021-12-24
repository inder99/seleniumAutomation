import sys
import urllib.request

import config
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from PIL import Image
from pytesseract import pytesseract

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

    
path_to_tesseract = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

username = config.loginHelpdesk4Username
password = config.loginHelpdesk4Password


s=Service('C:/Users/LogicSoftIT/Documents/selenium/chromedriver.exe')

browser = webdriver.Chrome(service=s)

browser.set_window_size(1024, 600)
browser.maximize_window()

url='https://foscos.fssai.gov.in/officer/'
browser.get(url)

browser.implicitly_wait(16)

usernameXpath = browser.find_element(By.XPATH,"/html/body/app-root/app-login/main-layout/div/div/div/div[1]/div/div[1]/form/div[2]/p[1]/input")
usernameXpath.clear()
usernameXpath.send_keys(username)

passwordXpath = browser.find_element(By.XPATH,"/html/body/app-root/app-login/main-layout/div/div/div/div[1]/div/div[1]/form/div[2]/p[2]/input")
passwordXpath.clear()
passwordXpath.send_keys(password)

def getCaptchaText(captchaImageXpath):
    captchaString = ''
    browser.implicitly_wait(8)

    imgCaptchXpath= browser.find_element(By.XPATH,captchaImageXpath)

    browser.implicitly_wait(16)

    imgCaptchSrc=imgCaptchXpath.get_attribute("src")

    urllib.request.urlretrieve(imgCaptchSrc, "captchHelpdesk4.png")

    image_path = r"captchHelpdesk4.png"
    
    # Opening the image & storing it in an image object
    img = Image.open(image_path)
    
    # Providing the tesseract 
    # executable location to pytesseract library
    pytesseract.tesseract_cmd = path_to_tesseract
    
    # Passing the image object to 
    # image_to_string() function
    # This function will
    # extract the text from the image
    text = pytesseract.image_to_string(img)
    
    # Displaying the extracted text
    #print(text[:-1])

    captchaString =  text[:-1]

    return captchaString

captchaText = getCaptchaText("/html/body/app-root/app-login/main-layout/div/div/div/div[1]/div/div[1]/form/div[2]/p[3]/img")

# Fetch Xpath of Captcha Input field and send captcha
browser.find_element(By.XPATH,"/html/body/app-root/app-login/main-layout/div/div/div/div[1]/div/div[1]/form/div[2]/p[4]/input").send_keys(captchaText)

browser.implicitly_wait(16)

# Fetch Xpath of SignIn and Click on it
browser.find_element(By.XPATH, "/html/body/app-root/app-login/main-layout/div/div/div/div[1]/div/div[1]/form/div[3]/div/button[1]").click()

browser.implicitly_wait(8)

# Click on HelpDesk
browser.find_element(By.XPATH, "/html/body/app-root/app-dashboard/loggedin-layout/div[1]/div/b/div[2]/div").click()
 
# Click on Open Tickets
browser.find_element(By.XPATH, "/html/body/app-root/app-dashboard/loggedin-layout/div[1]/div/b/div[2]/div[2]/div[1]/a").click();

# last row of the table
lastRow = browser.find_element(By.XPATH, "(//table[2]/tbody/tr)[last()]")

# Fetch the licencse no of the last row
lastRowReferenceNo = browser.find_element(By.XPATH, "(//table[2]/tbody/tr)[last()]/td[3]").text

applicationFlag = 1

if len(lastRowReferenceNo) == 14:
    applicationFlag = 0
    
print(lastRowReferenceNo)

# Click on the Proceed of the last row
browser.find_element(By.XPATH, "(//table[2]/tbody/tr/td)[last()]").click()

links = ["https://foscos.fssai.gov.in/"]

for link in links:
    print('navigating to: ' + link)
    
    browser.get(link)
    
    browser.implicitly_wait(16)
    
    if applicationFlag == 1:
        applicationInput = browser.find_element(By.XPATH, "//*[@id='govAgenciesSearch']").send_keys(lastRowReferenceNo)
        
        browser.implicitly_wait(16)
        
        c = getCaptchaText("//*[@id='keywordsDiv']/div/div/form/div/div/div[3]/p[2]/img")
        
        browser.implicitly_wait(16)
        
        print(c)
        
        # Fetch Xpath of Captcha Input field and send captcha
        captchInput  = browser.find_element(By.XPATH, "/html/body/app-root/app-index/main-layout/div/div[2]/div/div[1]/div/div[1]/div[1]/div/div/div/div/div/div[2]/div[1]/div/div[1]/div/div/form/div/div/div[3]/div/input").send_keys(c)
        browser.implicitly_wait(16)
        browser.find_element(By.XPATH, "//button[text()='Submit']").click()
        browser.implicitly_wait(16)
        #applicationStatus = browser.find_element(By.XPATH, "//*[@id='keywordsDiv']/div/div/div[2]/table/tbody/tr[4]/td[4]/label").text    
        browser.implicitly_wait(16)
    else :
        browser.find_element(By.XPATH, "//*[@id='p_p_id_eAdvisor_WAR_foblsportlet_']/div/div/div[2]/ul/li[3]").click()

        applicationInput = browser.find_element(By.XPATH, "/html/body/app-root/app-index/main-layout/div/div[2]/div/div[1]/div/div[1]/div[1]/div/div/div/div/div/div[2]/div[1]/div/div[4]/div[1]/div/div/div/form/div/div/div[3]/div/input").send_keys(lastRowReferenceNo)
        
        browser.implicitly_wait(16)
        
        c = getCaptchaText("//*[@id='governmentAgenciesDiv1']/div[1]/div/div/div/form/div/div/div[4]/p[2]/img")
        
        browser.implicitly_wait(16)
        
        print(c)
        
        # Fetch Xpath of Captcha Input field and send captcha
        captchInput  = browser.find_element(By.XPATH, "/html/body/app-root/app-index/main-layout/div/div[2]/div/div[1]/div/div[1]/div[1]/div/div/div/div/div/div[2]/div[1]/div/div[4]/div[1]/div/div/div/form/div/div/div[4]/div/input").send_keys(c)
        browser.implicitly_wait(16)
        browser.find_element(By.XPATH, "//button[text()='Search']").click()
        browser.implicitly_wait(16)
        #applicationStatus = browser.find_element(By.XPATH, "//*[@id='keywordsDiv']/div/div/div[2]/table/tbody/tr[4]/td[4]/label").text    
        browser.implicitly_wait(16)
        
        #print(applicationStatus)
    # do stuff within that page here...
    
    #browser.back()
    
def launchBrowser():
    while(True):
       pass
   
launchBrowser()
