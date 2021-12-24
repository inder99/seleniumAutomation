#!/usr/bin/python
import sys
import config
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

username = config.email
password = config.password + sys.argv[1]

s=Service('C:/Users/LogicSoftIT/Documents/selenium/chromedriver.exe')
browser = webdriver.Chrome(service=s)
url='https://email.gov.in/'
browser.get(url)
browser.implicitly_wait(8)
browser.find_element_by_name("username").send_keys(username)
browser.find_element_by_name("password").send_keys(password)

browser.implicitly_wait(4)

browser.find_element_by_xpath("//*[@id='formSubmitButton']").click()
