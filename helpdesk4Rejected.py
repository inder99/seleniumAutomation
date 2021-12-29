from re import sub
import sys
import urllib.request

from PIL import Image
from pytesseract import pytesseract

import config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from selenium.common.exceptions import TimeoutException
from PIL import UnidentifiedImageError

# write the console statements to the mentioned fileName
sys.stdout = open('./logHelpdesk4', 'a')

path_to_tesseract = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

# credientials for the helpdesk4 modification
username = config.loginHelpdesk4Username
password = config.loginHelpdesk4Password

# credentials for the PMU login
pmuUsername = config.loginFoscosPmuUsername
pmuPassword = config.loginFoscosPmuPassword

s=Service('C:/Users/LogicSoftIT/Documents/selenium/chromedriver.exe')

# open the chrome browser
browser = webdriver.Chrome(service=s)

# maximize the chrome window to full screen
browser.set_window_size(1024, 600)
browser.maximize_window()

# Answer to the ticket
messageToWrite = ''
applicationStatus = ''
lastRowReferenceNo = ''
typeOfApplication = ''
flagLicenseApplication = 1
numberOfRows = 1
# PMU url
link = config.urlFoscosOfficer

SHORT_TIMEOUT  = 5   # give enough time for the loading element to appear
LONG_TIMEOUT = 30  # give enough time for loading to finish

BUTTON_CLOSE_TICKET_XPATH = "//*[@id='Body']/app-root/app-ticket-action/loggedin-layout/div[3]/div/div[5]/div[2]/button[1]"

def setMessageToWrite(s):
    global messageToWrite
    messageToWrite = s

def setTypeOfApplication(s):
    global typeOfApplication
    typeOfApplication = s

def setApplicationStatus(s):
    global applicationStatus
    applicationStatus = s

def setflagLicenseApplication(flg):
    global flagLicenseApplication
    flagLicenseApplication = flg
    
def setlastRowReferenceNo(s):
    global lastRowReferenceNo
    lastRowReferenceNo = ''
    lastRowReferenceNo = s  
# function to define whether substring exist in String or not
def checkSubstring(string, sub_str):
    string= string.lower()
    sub_str = sub_str.lower()
    if (string.find(sub_str) == -1):
        return False
    else:
        return True

def clearTheVariablesToDefault() :
    setMessageToWrite('')
    setApplicationStatus('')
    setflagLicenseApplication(1)
    
# Extract captcha Text from an captch Xpath image
def getCaptchaText(captchaImageXpath):
    
    # var to store captcha text
    captchaString = ''
    
    browser.implicitly_wait(8)

    # Fetch the captcha xpath
    imgCaptchXpath= browser.find_element(By.XPATH,captchaImageXpath)

    browser.implicitly_wait(16)

    # Fetch the src from the Image Xpath
    imgCaptchSrc=imgCaptchXpath.get_attribute("src")

    # Store the image in temporary from the src path
    urllib.request.urlretrieve(imgCaptchSrc, "C:/Users/LogicSoftIT/Documents/selenium/captchHelpdesk4.png")

    image_path = r"C:/Users/LogicSoftIT/Documents/selenium/captchHelpdesk4.png"
    
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

# Function to Login into the Helpdesk4 Modificaiton
def loginForHelpdesk4() :
    
    # store the url to navigate
    url= config.urlFoscosOfficer
    
    # navigate to the url
    browser.get(url)

    browser.implicitly_wait(16)

    # Fetch the xpath of the userid field
    # Clear the field
    # Write the username in the input field
    usernameXpath = browser.find_element(By.XPATH,"/html/body/app-root/app-login/main-layout/div/div/div/div[1]/div/div[1]/form/div[2]/p[1]/input")
    usernameXpath.clear()
    usernameXpath.send_keys(username)

    # Fetch the xpath of the password field
    # Clear the field
    # Write the username in the input field
    passwordXpath = browser.find_element(By.XPATH,"/html/body/app-root/app-login/main-layout/div/div/div/div[1]/div/div[1]/form/div[2]/p[2]/input")
    passwordXpath.clear()
    passwordXpath.send_keys(password)

    browser.implicitly_wait(16)
    
    try:
        # Get captcha text from an image
        captchaText = getCaptchaText("/html/body/app-root/app-login/main-layout/div/div/div/div[1]/div/div[1]/form/div[2]/p[3]/img")

        browser.implicitly_wait(16)
        
        # Fetch Xpath of Captcha Input field and send captcha
        browser.find_element(By.XPATH,"/html/body/app-root/app-login/main-layout/div/div/div/div[1]/div/div[1]/form/div[2]/p[4]/input").send_keys(captchaText)

        browser.implicitly_wait(16)
        
    except UnidentifiedImageError:
        WebDriverWait(browser, 10)
        # Fetch Xpath of SignIn and Click on it
    finally:
        browser.find_element(By.XPATH, "/html/body/app-root/app-login/main-layout/div/div/div/div[1]/div/div[1]/form/div[3]/div/button[1]").click()


def openTicketsInHelpdesk():
    
    browser.implicitly_wait(8)

    # Click on sideNavBar - HelpDesk 
    browser.find_element(By.XPATH, "/html/body/app-root/app-dashboard/loggedin-layout/div[1]/div/b/div[2]/div").click()

    browser.implicitly_wait(8)

    # Click on sideNavBar - Helpdesk - Open Tickets
    browser.find_element(By.XPATH, "/html/body/app-root/app-dashboard/loggedin-layout/div[1]/div/b/div[2]/div[2]/div[1]/a").click();

    # last row of the table
    # lastRow = browser.find_element(By.XPATH, "(//table[2]/tbody/tr)[last()]")

# Fetch the Application/License number of the last row of the table
def fetchLastRowApplicationRef():

    browser.implicitly_wait(16)
    
    setlastRowReferenceNo(browser.find_element(By.XPATH, "(//table[2]/tbody/tr)[last()]/td[3]").text)
    
    print("Ticket No - " + browser.find_element(By.XPATH, "(//table[2]/tbody/tr)[last()]/td[4]").text)
    print("Application No - " + lastRowReferenceNo)
    # Flag to identify the type License or Registration
    # By default we assume it is License category
    flagLicenseApplication = 1

    if len(lastRowReferenceNo) == 14 and lastRowReferenceNo[0] == '2':
        flagLicenseApplication = 0
    elif len(lastRowReferenceNo) == 17 and lastRowReferenceNo[0] == '3':
        flagLicenseApplication = 0

    setflagLicenseApplication(flagLicenseApplication)

# Login to PMU Login  
def pmuLogin():
    print('navigating to PMU Link: ' + link)
    
    browser.get(link)
    
    # Credentials for the PMU Login    
    browser.find_element(By.XPATH,"/html/body/app-root/app-login/main-layout/div/div/div/div[1]/div/div[1]/form/div[2]/p[1]/input").send_keys(pmuUsername)

    # send password to the username field via send keys
    browser.find_element(By.XPATH,"/html/body/app-root/app-login/main-layout/div/div/div/div[1]/div/div[1]/form/div[2]/p[2]/input").send_keys(pmuPassword)

    browser.implicitly_wait(16)
    
    browser.implicitly_wait(8)
    
    try:
        
        c = getCaptchaText("//*[@id='signin']/form/div[2]/p[3]/img")
        
        browser.implicitly_wait(16)
        
        # Fill the input field with captcha
        browser.find_element(By.XPATH,"//*[@id='signin']/form/div[2]/p[4]/input").send_keys(c)

        browser.implicitly_wait(16)
        
    except UnidentifiedImageError:
        
        print("Kindly fill the captcha as captcha image not Loaded")
        
        WebDriverWait(browser, 10)
        
    finally:
        # click on signin
        browser.find_element(By.XPATH, "//*[@id='signin']/form/div[3]/div/button[1]").click()

def fetchApplicationStatus():
    browser.implicitly_wait(16)

    # Click on left nav - Reports
    browser.find_element(By.XPATH, "//*[@id='Body']/app-root/app-dashboard/loggedin-layout/div[1]/div/b/div[3]").click()
   
    browser.implicitly_wait(16)
   
    if flagLicenseApplication == 0 :
        # click on Reports - Registration
        browser.find_element(By.XPATH, "//*[@id='Body']/app-root/app-dashboard/loggedin-layout/div[1]/div/b/div[3]/div[2]/div[2]").click()
    else :
      # click on Reports - License
        browser.find_element(By.XPATH, "//*[@id='Body']/app-root/app-dashboard/loggedin-layout/div[1]/div/b/div[3]/div[2]/div[1]").click()

    browser.implicitly_wait(8)
    
    # Get the information corresponding to the license number/ application number
    browser.find_element(By.XPATH, "//*[@id='container']/form/div[1]/div[2]/input").send_keys(lastRowReferenceNo)

    browser.implicitly_wait(8)
    # Click on submit button
    browser.find_element(By.XPATH, "//*[@id='container']/form/div[2]/button").click()
    
    browser.implicitly_wait(16)
    
    # Fetch the application status of the application
    applicationStatus = browser.find_element(By.XPATH, "//*[@id='container']/div[3]/div[4]").text
    typeOfApplication = browser.find_element(By.XPATH, "//*[@id='container']/div[1]/div[4]/label").text
    setTypeOfApplication(typeOfApplication)
    print("Application status " + applicationStatus)
    messageToWrite = lastRowReferenceNo + ' type is ' + typeOfApplication + ' and status is "' + applicationStatus + '". '

    print("message - ", messageToWrite)
    
    if checkSubstring(applicationStatus, "Reverted"):    
        # Please search by application ref no. because modification history is dependent on application reference no.
        if(len(lastRowReferenceNo) == 14 ):
            getApplicationNo = browser.find_element("//*[@id='container'']/div[1]/div[2]/label/span[1]/span").text
            
            browser.find_element(By.XPATH, "//*[@id='container']/form/div[1]/div[2]/input").send_keys(getApplicationNo)

            browser.implicitly_wait(8)
            # Click on submit button
            browser.find_element(By.XPATH, "//*[@id='container']/form/div[2]/button").click()
            
            browser.implicitly_wait(16)
            
        browser.find_element(By.XPATH, "//*[@id='container']/div[9]/a[1]/label").click()
        fboRemark = browser.find_element(By.XPATH, "//*[@id='container']/div[9]/div[1]/div/div/table/tbody/tr[2]/td[3]").text
        messageToWrite = messageToWrite + ' FBO remarks is - ' + fboRemark + '. '
        
    setMessageToWrite(messageToWrite)
    setApplicationStatus(applicationStatus)
    # do stuff within that page here...
    # browser.back()
def moveTicketToDelayIssuance() : 
    browser.find_element(By.XPATH, "//*[@id='Body']/app-root/app-ticket-action/loggedin-layout/div[3]/div/div[5]/div[1]/input[2]").click()
    ddelement= Select(browser.find_element(By.XPATH, "//*[@id='Body']/app-root/app-ticket-action/loggedin-layout/div[3]/div/div[5]/table/tbody/tr[1]/td/select"))
    ddelement.select_by_visible_text('Delay in issuance of License/Registration')

def moveTicketToHelpdesk() : 
    browser.find_element(By.XPATH, "//*[@id='Body']/app-root/app-ticket-action/loggedin-layout/div[3]/div/div[5]/div[1]/input[2]").click()
    ddelement= Select(browser.find_element(By.XPATH, "//*[@id='Body']/app-root/app-ticket-action/loggedin-layout/div[3]/div/div[5]/table/tbody/tr[1]/td/select"))
    ddelement.select_by_visible_text('Helpdesk')
       
def responseToTicket():
    space = " "
    textToAppendWithMessage = messageToWrite
    textIncompleteMessageToAppend = "Login to Foscso portal and Kindly check in 'Incomplete Application' Home Dashboard foscos portal. "
    textHowToApplyLicense = """After license/registration is issued, for any modification, you need to apply at the portal of Foscos, under 
    'Modification' Tab 'Apply for Modification in License/Registration' alongWith supported document after that your application will move
    to the concerned Local Authority , For Registration it will go to 'RA'(Registration Authority) , for License it will go to 
    'DO'(Designated Officer). Click on the application number which is hyperlink to your modification of your application.
    https://foscos.fssai.gov.in/assets/docs/Howtoapplyformodificationoflicense.pdf . User Manutal 'https://foscos.fssai.gov.in/user-manual'
    """
    textApplicationRevertedToFBO = "Respond to Reverted Application https://foscos.fssai.gov.in/assets/docs/Howtorespondtoarevertedapplication.pdf ."
    textAttachScreenshot = space + " Kindly attach the screenshot of the technical error that you are facing."
    textToSurrender = """To surrender license/registration application needs to be in active state.
If the license/registration certificate is expired then you need to renew it first and then need to apply for the surrender.
To surrender follow this
https://foscos.fssai.gov.in/assets/docs/Howtosurrenderalicense.pdf
https://foscos.fssai.gov.in/user-manual
Order mentioned about renew after expiry
https://fssai.gov.in/upload/advisories/2021/10/617bd59fbcaedOrder_License_Expiry_date_29_10_2021.pdf"
"""
    textToHelpdesk = 'Please advise.'
    textToExpedite = 'Application is pending for approval. Please expedite the process.'
        
    # Click on the Proceed of the last row
    browser.find_element(By.XPATH, "(//table[2]/tbody/tr/td)[last()]").click()
    
    problem_description = ''
    
    try:
        problem_description = browser.find_element(By.XPATH, "//*[@id='Body']/app-root/app-ticket-action/loggedin-layout/div[3]/div/div[4]/div[2]/textarea").text
        print('Problem Description' + problem_description)
    except UnicodeEncodeError as str:
        print('unicode issue in parsing the Problem_description', str)
        pass
    
    print('response to ticket - ' + messageToWrite)
    
    if(checkSubstring(applicationStatus, "Incomplete Application")) :
        textToAppendWithMessage = textToAppendWithMessage + textIncompleteMessageToAppend
    elif(checkSubstring(applicationStatus, "issued")) : 
        textToAppendWithMessage = messageToWrite + textHowToApplyLicense
    elif checkSubstring(applicationStatus, "Reverted"):
        textToAppendWithMessage = textToAppendWithMessage + textApplicationRevertedToFBO
    elif checkSubstring(typeOfApplication, "Renewal") or checkSubstring(applicationStatus, "Non-Form C") or checkSubstring(applicationStatus, "Stage"):
        textToAppendWithMessage = textToAppendWithMessage + textToExpedite
    elif checkSubstring(applicationStatus, "Rejected"):
        textToAppendWithMessage = textToAppendWithMessage + textToHelpdesk
        
    if checkSubstring(problem_description, "surrender"):
        textToAppendWithMessage = textToAppendWithMessage + textToSurrender
            
    checkScreenshot = browser.find_element(By.XPATH, "//*[@id='Body']/app-root/app-ticket-action/loggedin-layout/div[3]/div/table/tbody/tr[2]/td[7]/span").text
    
    print('checkScreenshot - ', checkScreenshot)
    
    if checkSubstring(checkScreenshot, "N/A"):
        textToAppendWithMessage = textToAppendWithMessage + textAttachScreenshot
    
    if len(textToAppendWithMessage) != len(messageToWrite):
        setMessageToWrite(textToAppendWithMessage)
    
    # Fetch Xpath of textarea and write message on the text area - an answer to the ticket    
    browser.find_element(By.XPATH, "//*[@id='Body']/app-root/app-ticket-action/loggedin-layout/div[3]/div/div[5]/table/tbody/tr[1]/td/textarea").send_keys(messageToWrite)
    
    if (typeOfApplication == 'Renewal' and checkSubstring(applicationStatus, "Stage")) or (checkSubstring(applicationStatus, "Non-Form C") or checkSubstring(applicationStatus, "Stage")):
        moveTicketToDelayIssuance()
    elif checkSubstring(applicationStatus, "Rejected"):
        moveTicketToHelpdesk()
        browser.find_element(By.XPATH, BUTTON_CLOSE_TICKET_XPATH).click()
        print("Rejected appliation moved to the Heldpdesk")

loginForHelpdesk4()
openTicketsInHelpdesk()
fetchLastRowApplicationRef()

pmuLogin()
fetchApplicationStatus()

loginForHelpdesk4()
openTicketsInHelpdesk()

responseToTicket()

clearTheVariablesToDefault()

i = 0
while i <=10:
    pattern='https://foscos.fssai.gov.in/officer/helpdesk/open-ticket'
    
    try:
        wait = WebDriverWait(browser,90)
        wait.until(EC.url_matches(pattern))
    except TimeoutException as ex:
        print("Exception has been thrown. Timeout more than 90 seconds" + str(ex))
        break
        
    fetchLastRowApplicationRef()

    pmuLogin()
    fetchApplicationStatus()

    loginForHelpdesk4()
    openTicketsInHelpdesk()
    responseToTicket()
    
    clearTheVariablesToDefault()
    i = i+1


def launchBrowser():
    while(True):
       pass

# close write to the log file
sys.stdout.close()
  
launchBrowser()
