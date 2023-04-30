import re
from iCloudToGCal.processdata.processTable import remove_comments_css, remove_all_classes, get_all_tables, Table, to_csv
import datetime
from datetime import date
import os
from json import load, dump

temp = """
paste here raw html from icloud for debugging and testing
"""


def processAttendance(raw_html=temp):
    with open(r"C:\icloud_resources" + "\\attendance.json", "r") as f:
        attendRecords = load(f)
    data = []
    soup = remove_comments_css(raw_html)
    soup = remove_all_classes(soup)
    tables = get_all_tables(soup)

    t = Table(tables[0])
    arr = t.body_array[1:]

    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j] == "": continue
            if arr[i][j][0] in ["P", "p", "A", "a"]:
                dat = datetime_obj = datetime.datetime.strptime(f"{arr[0][j]}/{date.today().year}",
                                                                '%d/%m/%Y')
                # index 0 == date
                # index 1 == start time
                # index 2 == end time
                # index 3 == status(present or absent)
                Date = f"{dat.month}/{dat.day}/{dat.year}"
                startEnd = re.findall("\d\d[:]\d\d", arr[i][0])
                start = startEnd[0]
                end = startEnd[1]
                if arr[i][j][0] == "P" or arr[i][j][0] == "p":
                    status = "P"
                else:
                    status = "A"
                key = f" {Date} {start} {end} "
                value = f"{status}"
                if key in attendRecords.keys():
                    if attendRecords[key] == value:
                        continue
                    else:
                        attendRecords[key] = value
                        data.append([f"D", start, end, status])
                else:
                    attendRecords[key] = value
                    data.append([Date, start, end, status])
    with open(r"C:\icloud_resources" + "\\attendance.json", "w") as f:
        dump(attendRecords, f)
    return to_csv(data)
