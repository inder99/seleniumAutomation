import sys
import config
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

username = config.email
password = config.password

s=Service('./chromedriver.exe')
browser = webdriver.Chrome(service=s)
url='https://fssai.eoffice.gov.in'
browser.get(url)
browser.implicitly_wait(8)
browser.find_element_by_name("userName").send_keys(username)
browser.find_element_by_name("password").send_keys(password)

browser.implicitly_wait(4)

browser.find_element_by_xpath("//*[@id='userNameNextButton']").click()

browser.implicitly_wait(8)

browser.find_element_by_xpath("//*[@id='mobileradio']").click()

browser.find_element_by_xpath("//*[@id='btnApplySecurity']").click()
