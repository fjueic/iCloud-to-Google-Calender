from datetime import date
from time import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options





def openiCloud():
    # cerdentials
    with open("cerdential.txt", "r") as f:
        username = f.readline()
        password = f.readline()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    actions = ActionChains(driver)

    # login url
    driver.get("https://gu.icloudems.com/corecampus/index.php")
    driver.implicitly_wait(120)
    # enter username
    driver.find_element(By.ID, "useriid").send_keys(username)
    sleep(2)
    # enter password
    WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.ID, "actlpass"))).send_keys(password)
    # login button
    sleep(5)

    if not "schedulerand/tt_report_view.php" in driver.current_url:
        try:
            driver.find_element(By.ID, "psslogin").click()
        except:
            pass

    sleep(5)


    return driver


def clickOnTimeTable(driver):
    driver.find_element(By.XPATH,"//a[@href='schedulerand/tt_report_view.php']").click()
    sleep(5)
    # wait for timetable ot load
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    sleep(5)


def clickOnNext(driver):
    driver.find_element(By.XPATH, "//a[contains(text(),'Next')]").click()
    sleep(5)
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    sleep(5)

def get_academic_year(driver):

    #click on Menu
    driver.find_element(By.XPATH, "//a[contains(text(),'Menu')]").click()
    sleep(5)


def clickOnAttendence(driver):
    sleep(5)
    driver.find_element(By.XPATH, "//a[@href='/corecampus/student/attendance/myattendance.php']").click()

    sleep(5)

def openAttendence(driver):
    sleep(5)
    Select(driver.find_element(By.ID, "acadyear")).select_by_index(1)

    card_body = driver.find_element(By.CLASS_NAME, "card-body")
    sleep(5)
    Select(driver.find_element(By.NAME, "users")).select_by_index(date.today().month)
    sleep(5)


def sendClassData(data):
    # open google form link in headless chrome to send data


    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    actions = ActionChains(driver)
    # link is 3rd line in cerdential file
    driver.implicitly_wait(120)
    with open("cerdential.txt", "r") as f:
        f.readline()
        f.readline()
        link = f.readline().strip()
    driver.get(link)
    sleep(5)
    # all labels
    element = driver.find_elements (By.TAG_NAME, "label")
    # cilck on first label
    element[0].click()
    sleep(1)
    textInput = driver.find_element(By.TAG_NAME, "textarea")
    textInput.send_keys(data)
    sleep(2)
    # click on submit button
    sleep(10)
    driver.find_element(By.XPATH, "//span[contains(text(),'Submit')]").click()
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.CLASS_NAME, "vHW8K")))
    driver.close()

def sendAttendanceData(data):
    # headless chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    actions = ActionChains(driver)
    # link is 3rd line in cerdential file
    driver.implicitly_wait(120)
    with open("cerdential.txt", "r") as f:
        f.readline()
        f.readline()
        link = f.readline().strip()
    driver.get(link)
    sleep(5)
    # all labels
    element = driver.find_elements (By.TAG_NAME, "label")
    # cilck on first label
    element[1].click()
    sleep(1)
    textInput = driver.find_element(By.TAG_NAME, "textarea")
    textInput.send_keys(data)
    sleep(2)
    # click on submit button
    sleep(10)
    driver.find_element(By.XPATH, "//span[contains(text(),'Submit')]").click()
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.CLASS_NAME, "vHW8K")))
    driver.close()