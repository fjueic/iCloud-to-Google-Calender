from .chromedriver.installDriver import *

check_for_resources()
from .GUI.GUI import *

check_for_data()
from .processdata.processAttendence import *
from .processdata.processTable import *

from .selenuimFunctions.Gform import *
from .selenuimFunctions.iCloud import *


def run_script():
    """Run the script."""
    # Get the iCloud calendar data
    install_driver()
    driver = openiCloud()
    clickOnTimeTable(driver)
    t = processTable(driver.page_source)
    if len(t) != 0: sendClassData(t)
    clickOnNext(driver)
    t = processTable(driver.page_source)
    if len(t) != 0: sendClassData(t)

    clickOnAttendence(driver)
    t = processAttendance(driver.page_source)
    if len(t) != 0: sendAttendanceData(t)


def config():
    with open(r"C:\icloud_resources\cerdential.txt", "r+") as f:
        d = f.read().split("\n")
        try:
            data = GUI()
            for i in range(len(data)):
                if data[i]:
                    d[i] = data[i]
        except:
            pass
        f.seek(0)
        f.write("\n".join(d))
        f.truncate()

