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

username = config.loginFoscosPmuUsername
password = config.loginFoscosPmuPassword


s=Service('C:/Users/LogicSoftIT/Documents/selenium/chromedriver.exe')

browser = webdriver.Chrome(service=s)

browser.set_window_size(1024, 600)
browser.maximize_window()

url='https://foscos.fssai.gov.in/officer/'
browser.get(url)

browser.implicitly_wait(16)

# store the xpath of the captcha
imgXpath= browser.find_element(By.XPATH,"/html/body/app-root/app-login/main-layout/div/div/div/div[1]/div/div[1]/form/div[2]/p[3]/img")

# send user name to the username field via send keys
browser.find_element(By.XPATH,"/html/body/app-root/app-login/main-layout/div/div/div/div[1]/div/div[1]/form/div[2]/p[1]/input").send_keys(username)

# send password to the username field via send keys
browser.find_element(By.XPATH,"/html/body/app-root/app-login/main-layout/div/div/div/div[1]/div/div[1]/form/div[2]/p[2]/input").send_keys(password)

browser.implicitly_wait(16)

# get the src of the image (captcha)
imgSrcPath = imgXpath.get_attribute("src")

# name of the image in which captcha will be stored
tempImageName = "captchaLoginFoscosPmu.png"

# open an image in the url via src path and store in tempImageName variable
urllib.request.urlretrieve(imgSrcPath, tempImageName)

image_path = r"captchaLoginFoscosPmu.png"
  
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
print(text[:-1])

captchaText =  text[:-1]

# Fill the input field with captcha
browser.find_element(By.XPATH,"/html/body/app-root/app-login/main-layout/div/div/div/div[1]/div/div[1]/form/div[2]/p[4]/input").send_keys(captchaText)

browser.implicitly_wait(16)

# click on signin
browser.find_element(By.XPATH, "/html/body/app-root/app-login/main-layout/div/div/div/div[1]/div/div[1]/form/div[3]/div/button[1]").click()

browser.implicitly_wait(16)

#Click on Reports
browser.find_element(By.XPATH, "//*[@id='Body']/app-root/app-dashboard/loggedin-layout/div[1]/div/b/div[3]").click()

# click on Reports - Registration
browser.find_element(By.XPATH, "//*[@id='Body']/app-root/app-dashboard/loggedin-layout/div[1]/div/b/div[3]/div[2]/div[2]").click()

def launchBrowser():
    chrome_options = Options()
    chrome_options.binary_location="../Google Chrome"
    chrome_options.add_argument("disable-infobars");
    chrome_options.add_argument("--start-maximized")
    while(True):
       pass
   
launchBrowser()
