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

username = config.loginHelpdesk8Username
password = config.loginHelpdesk8Password


s=Service('C:/Users/LogicSoftIT/Documents/selenium/chromedriver.exe')

browser = webdriver.Chrome(service=s)

browser.set_window_size(1024, 600)
browser.maximize_window()

url='https://foscos.fssai.gov.in/officer/'
browser.get(url)

browser.implicitly_wait(16)

imgsrc= browser.find_element(By.XPATH,"/html/body/app-root/app-login/main-layout/div/div/div/div[1]/div/div[1]/form/div[2]/p[3]/img")

browser.find_element(By.XPATH,"/html/body/app-root/app-login/main-layout/div/div/div/div[1]/div/div[1]/form/div[2]/p[1]/input").send_keys(username)

browser.find_element(By.XPATH,"/html/body/app-root/app-login/main-layout/div/div/div/div[1]/div/div[1]/form/div[2]/p[2]/input").send_keys(password)

browser.implicitly_wait(8)

browser.implicitly_wait(16)

x=imgsrc.get_attribute("src")

tempImageName = "captchHelpdesk4.png"
urllib.request.urlretrieve(x, tempImageName)

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

captchaText =  text[:-1]

browser.find_element(By.XPATH,"/html/body/app-root/app-login/main-layout/div/div/div/div[1]/div/div[1]/form/div[2]/p[4]/input").send_keys(captchaText)

browser.implicitly_wait(16)

browser.find_element(By.XPATH, "/html/body/app-root/app-login/main-layout/div/div/div/div[1]/div/div[1]/form/div[3]/div/button[1]").click()

browser.implicitly_wait(16)

# browser.find_element(By.ID, "//*[@id='Body']/app-root/app-open-ticket/loggedin-layout/div[1]/div/b/div[2]").click()

#browser.find_element(By.XPATH, "/html/body/app-root/app-open-ticket/loggedin-layout/div[1]/div/b/div[2]/div[2]/div[1]").click()

#browser.find_element(By.XPATH, "/html/body/app-root/app-open-ticket/loggedin-layout/div[3]/div/table[2]/tbody/tr[2]/td[7]/a").click()

def launchBrowser():
    while(True):
       pass
   
launchBrowser()
