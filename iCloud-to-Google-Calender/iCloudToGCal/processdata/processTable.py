import re
from json import dump
from bs4 import BeautifulSoup, Comment
from iCloudToGCal.processdata.data import recoded
from iCloudToGCal.selenuimFunctions.Gform import sendClassData

temp = """
paste here raw html from icloud for debugging and testing

"""


def remove_comments_css(html):
    """
    removes all comments and css from html
    """
    soup = BeautifulSoup(html, 'html.parser')
    # remove all comments
    comments = soup.findAll(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()
    # remove all style tags and properties
    for tag in soup.find_all(['style', 'script']):
        tag.decompose()
    for tag in soup.find_all(True):
        del tag['style']
    return soup


def remove_all_classes(soup):
    """
    removes all classes from html
    """
    for tag in soup.find_all(True):
        del tag['class']
    return soup


def get_all_tables(soup):
    """
    returns array of all tables in soup
    """
    return soup.find_all('table')


def diagonalflip(arr):
    return list(list(e) for e in zip(*arr))


def clean(arr):
    def check(a):
        for e in a:
            if e != ' ':
                return True
        return False

    for rows in arr:
        while "" in rows:
            rows.remove("")
    t = list()
    arr = diagonalflip(arr)
    for rows in arr:
        if check(rows):
            t.append(rows)
    arr = diagonalflip(t)
    return arr


class Table:
    def __init__(self, table):
        # full table
        self.time_table = table.extract()
        # heading
        self.table_heading = self.time_table.findChild("thead")
        # body
        self.table_body = self.time_table.findAll("tbody")
        arr = []
        for tbody in self.table_body:
            for tr in tbody.findAll("tr"):
                arr.append(tr)
        # to 2d array
        self.body_array = list(
            list(re.sub(' +', ' ', td.text.replace('\n', ' ')) for td in tr) for tr in arr)
        try:
            self.heading_array = list(
                list(re.sub(' +', ' ', th.text.replace('\n', ' ')) for th in tr) for tr in
                self.table_heading.findAll("th"))
        except:
            pass


class Lecture:
    def __init__(self, arr):
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        days_map = {day: index for index, day in enumerate(days)}
        if len(arr[2]) > 5 or len(arr[3]) > 5:
            self.start = re.findall("\d\d[:]\d\d", arr[1])[0]
            self.end = re.findall("\d\d[:]\d\d", arr[1])[1]
            self.day = days_map[re.findall("(Mon|Tue|Wed|Thu|Fri|Sat|Sun)", arr[0])[0]]
            self.teacher = arr[2]
            self.description = arr[3]
            self.type = re.findall("[(][P][PR][)]", arr[3])[0][1:-1]
            self.color = "4"
            if self.type == "PR": self.color = "7"
            try:
                self.location = re.findall("(Online)", arr[3])[0]
            except:
                self.location = re.findall("[A-D][-:]\d\d\d", arr[3])[0]
            try:
                self.name = re.findall("^.*?(?=\((?:PP|PR)\))", arr[3])[0]
            except:
                self.name = self.description
        else:
            self.name = "N/A"
            self.start = re.findall("\d\d[:]\d\d", arr[1])[0]
            self.end = re.findall("\d\d[:]\d\d", arr[1])[1]
            self.day = days_map[re.findall("(Mon|Tue|Wed|Thu|Fri|Sat|Sun)", arr[0])[0]]
            self.teacher = "N/A"
            self.description = "N/A"
            self.type = "N/A"
            self.color = "N/A"
            self.location = "N/A"


def to_csv(arr):
    """
    converts 2d array to csv
    """
    result = ""
    for row in arr:
        for cell in row:
            result += f"{cell},"
        result += "\n"
    return result


def add_free_lectures(lectures, dates):
    """
    adds free lectures to lectures array
    it is used to fill the gaps between lectures
    """
    times = [("08:45", "09:35"), ("09:35", "10:25"), ("10:30", "11:20"), ("11:20", "12:10"), ("12:15", "13:05"),
             ("13:05", "13:55"), ("14:00", "14:50"), ("14:50", "15:40"), ("15:45", "16:35")]
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    def check(lectures, date, start, end):
        for lecture in lectures:
            if days[dates.index(date)] in lecture[0] and f"{start} - {end}" in lecture[1]:
                return True
        return False

    for date in dates:
        for time in times:
            if check(lectures, date, time[0], time[1]): continue
            lectures.append([
                days[dates.index(date)], f"{time[0]} - {time[1]}", "", ""
            ])
    return lectures


def processTable(raw_data=temp):
    # print(raw_data)
    data = []
    soup = remove_comments_css(raw_data)
    soup = remove_all_classes(soup)
    tables = get_all_tables(soup)

    t1 = Table(tables[0])
    t2 = Table(tables[1])
    t3 = Table(tables[2])
    dates = list(date[0][-9:-1] for date in t1.heading_array[-7:])
    dates = list(f"{date.split('/')[1]}/{date.split('/')[0]}/20{date.split('/')[2]}" for date in dates)

    """
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
    """
    lectures = clean(t3.body_array)
    lectures = add_free_lectures(lectures, dates)

    for row in lectures:
        l = Lecture(row)
        date = dates[l.day]
        key = f"{date} {l.start} {l.end}"
        value = l.description
        if key in recoded.keys():
            if recoded[key] == value:
                continue
            else:
                if value == "N/A":
                    recoded[key] = value
                    data.append(
                        [f"{l.name} {l.teacher}", date, l.start, l.end, l.location, l.description, l.color, "Mail",
                         "Delete"])
                else:
                    recoded[key] = value
                    data.append(
                        [f"{l.name} {l.teacher}", date, l.start, l.end, l.location, l.description, l.color, "Mail",
                         "Create"])
        else:
            if value != "N/A":
                recoded[key] = value
                data.append([f"{l.name} {l.teacher}", date, l.start, l.end, l.location, l.description, l.color, "Don"
                                                                                                                "'t "
                                                                                                                "Mail",
                             "Create"])
            recoded[key] = value
    # save data to record.json
    import os
    with open(r"C:\icloud_resources" + "\\record.json", "w") as fp:
        dump(recoded, fp)

    return to_csv(data)
