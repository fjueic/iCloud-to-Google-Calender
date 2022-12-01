from projectImports import *
from data import temp


def sumbitData():
    DATA = ""
    for row in data:
        for element in row:
            DATA += f"{element},"
        DATA = DATA[:-1] + "\n"
    DATA = DATA[:-1]
    if len(DATA) > 0:
        sendClassData(DATA)
    sleep(120)

    DATA = ""
    for row in attendanceArray:
        for element in row:
            DATA += f"{element},"
        DATA = DATA[:-1] + "\n"
    DATA = DATA[:-1]
    if (len(DATA) > 0):
        sendAttendanceData(DATA)




def main():


    driver = openiCloud()


    clickOnTimeTable(driver)
    raw_html = driver.page_source
    processTable(raw_data=raw_html)



    clickOnNext(driver)
    raw_html = driver.page_source
    processTable(raw_data=raw_html)

    clickOnAttendence(driver)

    openAttendence(driver)
    raw_html = driver.page_source
    processAttendance(raw_html)
    driver.close()
    sumbitData()
def custom(s):
    processTable(raw_data=s)
    sumbitData()
if __name__ == '__main__':
    main()



