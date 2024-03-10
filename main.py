import base64
import json
from time import sleep, time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver
from seleniumwire.utils import decode


class Lecture:
    def __init__(self, obj):
        self.division = obj["division"]
        self.date = obj["fromDate"]
        self.lectType = obj["lectType"]
        self.fromTime = obj["fromTime"]
        self.toTime = obj["toTime"]
        self.day = obj["day"]
        self.roomno = obj["roomno"]
        self.course_code = obj["sub_shortname"]
        self.course_name = obj["subject_full"]
        self.teacher = obj["empFName"]
        self.batch_name = obj["batch_name"]
        self.action = None
        self.alternate = False

    def __str__(self):
        return f"{self.course_code}, {self.course_name}, {self.teacher}, {self.division}, {self.date}, {self.lectType}, {self.fromTime}, {self.toTime}, {self.day}, {self.roomno}, {self.batch_name}, {self.action}, {self.alternate}"


class AlternateLecture:
    def __init__(self, obj):
        self.division = obj["division"]
        self.date = obj["date"]
        self.lectType = obj["lectType"]
        self.fromTime = obj["fromtime"]
        self.toTime = obj["totime"]
        self.day = obj["day"]
        self.roomno = obj["roomno"]
        self.course_code = obj["sub_Code"]
        self.course_name = obj["sub_Fulltname"]
        self.teacher = (
            obj["EmpFirstName_alt"]
            + " "
            + obj["EmpMiddleName_alt"]
            + " "
            + obj["EmpLastName_alt"]
        )
        self.batch_name = obj["batch_name"]
        self.action = None
        self.alternate = True

    def __str__(self):
        return f"{self.course_code}, {self.course_name}, {self.teacher}, {self.division}, {self.date}, {self.lectType}, {self.fromTime}, {self.toTime}, {self.day}, {self.roomno}, {self.batch_name}, {self.action}, {self.alternate}"


def openInstance():
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(options=firefox_options)
    return driver


def waitTillElement(driver, element):
    try:
        element_present = EC.presence_of_element_located((By.ID, element))
        WebDriverWait(driver, 5).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")


def login(driver, username, password):
    driver.get("https://gu.icloudems.com/corecampus/index.php")
    waitTillElement(driver, "useriid")
    driver.find_element(By.ID, "useriid").send_keys(username)
    sleep(1)
    driver.find_element(By.ID, "actlpass").send_keys(password)
    sleep(1)
    driver.find_element(By.ID, "psslogin").click()
    waitTillElement(driver, "sidebar-toggler")


def openAttendancePage(driver):
    sleep(2)
    element = driver.find_element(
        By.XPATH, "//a[@href='/corecampus/student/schedulerand/tt_report_view.php']"
    ).click()
    current_time = time()
    while time() - current_time < 10:
        sleep(1)
        if "Monday" in driver.page_source:
            break
    sleep(2)
    try:
        driver.find_element(By.XPATH, "//a[contains(text(),'Next ')]").click()
    except:
        driver.find_element(By.XPATH, "//a[contains(text(),'Next')]").click()
    sleep(3)


def getTimeTableFromRequest(driver):
    lectures = []
    for request in driver.requests:
        if (
            request.response
            and request.url
            == "https://gu.icloudems.com/corecampus/student/schedulerand/ctrl_tt_report.php"
        ):
            body = decode(
                request.response.body,
                request.response.headers.get("Content-Encoding", "identity"),
            )
            data = json.loads(body)

            for day in data["NEWTT"].keys():
                for lecture_start in data["NEWTT"][day].keys():
                    for lecture_end in data["NEWTT"][day][lecture_start].keys():
                        for lecture in data["NEWTT"][day][lecture_start][lecture_end]:
                            lectures.append(Lecture(lecture))

            for lecture in data["MyAlternate"]:
                lectures.append(AlternateLecture(lecture))
    return lectures


def openGoogleForm(driver, id):
    driver.get(f"https://docs.google.com/forms/d/e/{id}/viewform")
    waitTillElement(driver, "wSDd7b")


def fillGoogleForm(driver, data):
    driver.find_element(By.TAG_NAME, "textarea").send_keys(data)
    driver.find_element(By.XPATH, "//span[contains(text(),'Submit')]").click()


def sendData(driver, data, id):
    if data:
        openGoogleForm(driver, id)
        fillGoogleForm(driver, data)
        sleep(5)
    driver.quit()


def filterByOldDate(data):
    import os

    if os.path.exists("store.json"):
        with open("store.json", "r") as file:
            old_data = json.load(file)
    else:
        os.system("touch store.json")
        old_data = {}
    new_data = {}
    return_data = []

    for lecture in data:
        t = (
            lecture.date
            + ","
            + lecture.fromTime
            + ","
            + lecture.toTime
            + ","
            + str(lecture.alternate)
            + ","
            + lecture.roomno
        )
        if t not in old_data:
            new_data[t] = lecture.course_code
            lecture.action = "Added"
            return_data.append(lecture)
        elif lecture.course_code != old_data[t]:
            lecture.action = "Changed"
            new_data[t] = lecture.course_code
            return_data.append(lecture)
    temp = [
        lecture.date
        + ","
        + lecture.fromTime
        + ","
        + lecture.toTime
        + ","
        + str(lecture.alternate)
        + ","
        + lecture.roomno
        for lecture in data
    ]
    for i in range(len(old_data)):
        if list(old_data.keys())[i] not in temp:
            return_data.append(
                Lecture(
                    {
                        "division": "NA",
                        "fromDate": list(old_data.keys())[i].split(",")[0],
                        "lectType": "NA",
                        "fromTime": list(old_data.keys())[i].split(",")[1],
                        "toTime": list(old_data.keys())[i].split(",")[2],
                        "day": "NA",
                        "roomno": "NA",
                        "sub_shortname": old_data[list(old_data.keys())[i]],
                        "subject_full": "NA",
                        "empFName": "NA",
                        "batch_name": "NA",
                    }
                )
            )
            return_data[-1].action = "Removed"
        else:
            new_data[list(old_data.keys())[i]] = old_data[list(old_data.keys())[i]]
    return return_data, new_data


def main():
    id = "GOOGLE FORM ID"
    guid = "GUID"
    gupass = "GUPASS"
    driver = openInstance()
    driver.get("https://gu.icloudems.com/corecampus/index.php")
    login(driver, guid, gupass)
    openAttendancePage(driver)
    data = getTimeTableFromRequest(driver)
    data, new_data = filterByOldDate(data)
    data = [str(i).strip() for i in data]
    data = data[::-1]
    data = "\n".join(data)
    sendData(driver, data, id)
    with open("store.json", "w") as file:
        json.dump(new_data, file)


if __name__ == "__main__":
    main()
