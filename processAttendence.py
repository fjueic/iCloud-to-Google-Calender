import re
from datetime import datetime
from datetime import date
from json import dump
import datetime
from functionsForTableAndLectures import AttendanceTable, CleanSoup
from bs4 import BeautifulSoup
from data import attendRecords
from seleniumFunctions import sendAttendanceData

attendanceArray =[] # list of all attendance data
def processAttendance(raw_html):
    # clean raw HTML data
    soup = CleanSoup(BeautifulSoup(raw_html, features="html.parser"))
    # get all tables from html
    table = soup.findAll("table")
    # attendance table is first and only table on whole page
    attendance = AttendanceTable(table[0])
    result = 0
    # get all lectures attendance status
    for i in range(len(attendance.body_array)):
        for j in range(len(attendance.body_array[i])):
            if attendance.body_array[i][j][0] in ["P","p","A","a"]:
                dat = datetime_obj = datetime.datetime.strptime(f"{attendance.body_array[0][j]}/{date.today().year}", '%d/%m/%Y')
                # index 0 == date
                # index 1 == start time
                # index 2 == end time
                # index 3 == status(present or absent)
                Date = f"{dat.month}/{dat.day}/{dat.year}"
                startEnd = re.findall("\d\d[:]\d\d",attendance.body_array[i][0])
                start = startEnd[0]
                end = startEnd[1]
                if attendance.body_array[i][j][0] == "P" or attendance.body_array[i][j][0] =="p":
                    status = "P"
                else:
                    status = "A"
                key = f" {Date} {start} {end} "
                value = f"{status}"
                if key in attendRecords.keys():
                    if attendRecords[key] == value:
                        continue
                    else:
                        attendRecords[key]=value
                        attendanceArray.append([f"D", start, end, status])
                else:
                    attendRecords[key]=value
                    attendanceArray.append([Date, start, end, status])
    # save the recoded data to attendance.json file
    with open("attendance.json", "w") as fp:
        dump(attendRecords,fp)