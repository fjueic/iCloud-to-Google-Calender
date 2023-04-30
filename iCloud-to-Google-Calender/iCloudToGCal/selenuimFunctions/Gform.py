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
import os

def sendClassData(data):
    # open google form link in headless chrome to send data


    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    actions = ActionChains(driver)
    # link is 3rd line in cerdential file
    driver.implicitly_wait(120)
    with open(r"C:\icloud_resources" + "\\cerdential.txt", "r") as f:
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
    sleep(.1)
    driver.close()

def sendAttendanceData(data):
    # headless chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    actions = ActionChains(driver)
    # link is 3rd line in cerdential file
    driver.implicitly_wait(120)
    with open(r"C:\icloud_resources" + "\\cerdential.txt", "r") as f:
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
    driver.close()

