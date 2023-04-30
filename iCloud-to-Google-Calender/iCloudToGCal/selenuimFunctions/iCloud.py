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


def openiCloud(username="",password=""):
    # cerdentials
    import os
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    if username == "" and password == "":
        with open(r"C:\icloud_resources" +"\\cerdential.txt", "r") as f:
            username = f.readline()
            password = f.readline()+"\n"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    actions = ActionChains(driver)

    # login url
    driver.get("https://gu.icloudems.com/corecampus/index.php")
    driver.implicitly_wait(120)
    # enter username
    driver.find_element(By.ID, "useriid").send_keys(username)
    sleep(2)
    # enter password
    WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.ID, "actlpass"))).send_keys(password)
    # press enter
    # driver.find_element(By.ID, "actlpass").send_keys(Keys.ENTER)
    # login button
    sleep(5)

    # if not "schedulerand/tt_report_view.php" in driver.current_url:
    # try:
    #     driver.find_element(By.ID, "psslogin").click()
    # except:
    #     pass



    return driver


def clickOnTimeTable(driver):
    driver.find_element(By.XPATH,"//a[@href='schedulerand/tt_report_view.php']").click()
    sleep(5)
    # wait for timetable ot load
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    sleep(5)


def clickOnNext(driver):
    try:
        driver.find_element(By.XPATH, "//a[contains(text(),'Next ')]").click()
    except:
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
    driver.execute_script("""
    var sidebar = document.querySelector('.sidebar-menu');
    sidebar.innerHTML = '<a href="/corecampus/student/attendance/myattendance.php">Attendance</a>';
    """)
    # click on attendance
    driver.find_element(By.XPATH, "//a[contains(text(),'Attendance')]").click()
    sleep(5)
    try:
        driver.find_element(By.ID, "getattendance").click()
    except:pass
    sleep(5)
def openAttendence(driver):
    sleep(5)
    Select(driver.find_element(By.ID, "acadyear")).select_by_index(1)

    card_body = driver.find_element(By.CLASS_NAME, "card-body")
    sleep(5)
    Select(driver.find_element(By.NAME, "users")).select_by_index(date.today().month)
    sleep(5)

