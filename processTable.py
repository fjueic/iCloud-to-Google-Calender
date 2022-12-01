from json import dump

from bs4 import BeautifulSoup

from functionsForTableAndLectures import *

from data import recoded, data
from seleniumFunctions import sendClassData


def processTable(raw_data):
    # clean data
    soup = CleanSoup(BeautifulSoup(raw_data, features="html.parser"))
    # get all tables from html
    table = soup.findAll("table")
    # first i s week wise table
    # second is alternate faculty table
    # lecture wise table is 3rd table
    lectures = Table(table[2])
    time_table = Table(table[0])

    # get all week's dates from timetable
    dates = list(date[0][-9:-1] for date in time_table.heading_array[-7:])
    # change dates format from "dd.mm.yy" to "mm.dd.yyyy"
    dates = list(f"{date.split('/')[1]}/{date.split('/')[0]}/20{date.split('/')[2]}" for date in dates)
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    days_map = {day: index for index, day in enumerate(days)}
    # find all holidays
    holidays = findHolidays(lectures)
    # enter all holidays again to avoid any error happened while cleaning data
    time_table = add_holidays(time_table, holidays)

    # check for empty slots in time_table.body_array
    # add empty slots to lectures table(3rd table) to keep track of holidays
    for i in range(len(time_table.body_array)):
        for j in range(len(time_table.body_array[i])):
            if j == 0:
                continue
            if len(time_table.body_array[i][j]) < 5 and len(time_table.body_array[i][0]) > 6:
                lectures.body_array.append([days[j - 1], f" {time_table.body_array[i][0]} ", "", ""])



    # get all lectures from lectures table
    # store all Lecture objects in lectures_list
    arr = []
    for lecture in lectures.body_array:
        # lecture is a list of 4 elements
        # Lecture is a class which get lecture data and store them in variable
        arr.append(Lecture(lecture, time_table))


    # all lectures data is recoded in recoded variable with is a dictionary
    # recoded variable is loaded from a json file named record.json
    for lecture in arr:
        # check if lecture is already recoded
        if f"{dates[lecture.day]} {lecture.start} {lecture.end}" in recoded.keys():
            # if lecture is recoded and code is same as recoded code there is nothing to do
            if recoded[f"{dates[lecture.day]} {lecture.start} {lecture.end}"] == lecture.code:
                continue
            # if lecture is recoded but code is different
            # class is changed and we need to update data and send email to users
            elif recoded[f"{dates[lecture.day]} {lecture.start} {lecture.end}"] != lecture.code:
                # if lecture was deleted
                if lecture.code == "N/A":
                    recoded[f"{dates[lecture.day]} {lecture.start} {lecture.end}"] = lecture.code
                    data.append(
                        [f"{lecture.name} {lecture.teacher} {lecture.code}", dates[lecture.day], lecture.start,
                         lecture.end,
                         lecture.location, lecture.description, lecture.color, "Mail", "Delete"])
                # if lecture is added
                else:
                    recoded[f"{dates[lecture.day]} {lecture.start} {lecture.end}"] = lecture.code
                    data.append(
                        [f"{lecture.name} {lecture.teacher} {lecture.code}", dates[lecture.day], lecture.start, lecture.end,
                         lecture.location, lecture.description, lecture.color, "Mail", "Create"])


            # if lecture is not recoded
            # lecture is new and we need to add it to recoded and there is no need to send email to users

            else:
                recoded[f"{dates[lecture.day]} {lecture.start} {lecture.end}"] = f"{lecture.code}"
                data.append(
                    [f"{lecture.name} {lecture.teacher} {lecture.code}", dates[lecture.day], lecture.start, lecture.end,
                     lecture.location, lecture.description, lecture.color, "Don't Mail", "Create"])
        else:
            if (lecture.code != "N/A"):
                recoded[f"{dates[lecture.day]} {lecture.start} {lecture.end}"] = f"{lecture.code}"
                data.append(
                    [f"{lecture.name} {lecture.teacher} {lecture.code}", dates[lecture.day], lecture.start, lecture.end,
                     lecture.location, lecture.description, lecture.color, "Don't Mail", "Create"])
            else:
                recoded[f"{dates[lecture.day]} {lecture.start} {lecture.end}"] = f"{lecture.name}"


    # again save data to record.json
    with open("record.json", "w") as fp:
        dump(recoded, fp)