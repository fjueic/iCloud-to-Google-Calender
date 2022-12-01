import pickle
import re

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
days_map = {day: index for index, day in enumerate(days)}


def storeData(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def getData(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


def add_holidays(time_table, holidays):
    for i in range(len(time_table.body_array)):
        for holiday in holidays:
            time_table.body_array[i].insert(days_map[holiday] + 1, " ")
    return time_table


def abc(time_table):
    for row in range(len(time_table.body_array)):
        print((time_table.body_array[row]))
    for _ in range(5):
        print()
    for row in range(len(time_table.body_array)):
        print(len((time_table.body_array[row])))
    for _ in range(5):
        print()

    for row in range(len(time_table.heading_array)):
        print((time_table.heading_array[row]))
    for _ in range(5):
        print()
    for row in range(len(time_table.heading_array)):
        print(len((time_table.heading_array[row])))
    for _ in range(5):
        print()


def getElement(time_table, day, start, end):
    timePeriod = f"{start} - {end}"
    temp = 0
    for j in range(len(time_table.body_array)):
        if timePeriod == time_table.body_array[j][0]:
            temp = j
            break
    return time_table.body_array[temp][day + 1]


def remove_white_from_string(string):
    return re.sub(r'\s+', '', string)


def findHolidays(lectures):
    temp = diagonalFlip(lectures.body_array)[0]
    days = [" Mon", " Tue", " Wed", " Thu", " Fri", " Sat", " Sun"]
    result = list()
    for i in range(len(days)):
        if days[i] not in temp:
            result.append(remove_white_from_string(days[i]))
    for i in range(len(result)):
        remove_white_from_string(result[i])
    return result


def diagonalFlip(arr):
    return list(list(e) for e in zip(*arr))


# def transpose_array(arr):
#     return

def check_column(arr):
    for e in arr:
        if len(e) > 5:
            return False
    return True


def clean(arr):
    def check(a):
        for e in a:
            if e != ' ':
                return True
        return False

    for rows in arr:
        while ("" in rows):
            rows.remove("")
    temp = list()
    arr = diagonalFlip(arr)
    for rows in arr:
        if check(rows):
            temp.append(rows)
    arr = diagonalFlip(temp)
    return arr


def CleanSoup(content):
    for tags in content.findAll(True):
        tags.attrs = {}
    return content


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
        self.body_array = clean(self.body_array)
        try:
            self.heading_array = list(
                list(re.sub(' +', ' ', th.text.replace('\n', ' ')) for th in tr) for tr in
                self.table_heading.findAll("th"))
        except:
            pass
        try:
            self.heading_array = clean(self.heading_array[:])
        except:
            pass


class Lecture:
    def __init__(self, arr, time_table):
        if len(arr[2]) > 5 or len(arr[3]) > 5:
            self.name = re.findall(".*[\s][(][P][PR][)]", arr[3])[0][:-5]
            self.start = re.findall("\d\d[:]\d\d", arr[1])[0]
            self.end = re.findall("\d\d[:]\d\d", arr[1])[1]
            self.day = days_map[re.findall("(Mon|Tue|Wed|Thu|Fri|Sat|Sun)", arr[0])[0]]
            try:
                self.location = re.findall("(Online)", arr[3])[0]
            except:
                self.location = re.findall("[A-D][-:]\d\d\d", arr[3])[0]
            self.teacher = arr[2]
            try:
                self.code = re.findall("[)]\s.*-S", arr[3])[0][2:-2]
            except:
                try:
                    self.code = re.findall("Se.*P[PR]", getElement(time_table, self.day, self.start, self.end))[0][
                                10:-4]
                except:
                    self.code = re.findall("SEM.*P[PR].*-", getElement(time_table, self.day, self.start, self.end))[0][
                                9:-7]
            self.type = re.findall("[(][P][PR][)]", arr[3])[0][1:-1]
            if self.type == "PR":
                self.type = "Practical"
                try:
                    self.division = re.findall("P[12]", arr[3])[0]
                except:
                    try:
                        self.division = re.findall("PR[12]", arr[3])[0]
                    except:
                        self.division = "N/A"
                try:
                    self.section = re.findall("CSE-\d", arr[3])[0][-1]
                except:
                    self.section = "N/A"
            else:
                self.type = "Theory"
                self.division = "N/A"
                self.section = re.findall("\d\s", arr[3])[0][0]
            if self.type == "Theory":
                self.color = "4"
            else:
                self.color = "7"
            self.description = f"{self.name} {self.type} {self.division} {self.section} {self.code} {self.teacher} {self.location} {self.start} - {self.end} {self.day}"
        else:
            self.name = "N/A"
            self.start = re.findall("\d\d[:]\d\d", arr[1])[0]
            self.end = re.findall("\d\d[:]\d\d", arr[1])[1]
            self.day = days_map[re.findall("(Mon|Tue|Wed|Thu|Fri|Sat|Sun)", arr[0])[0]]
            self.location = "N/A"
            self.teacher = "N/A"
            self.code = "N/A"
            self.type = "N/A"
            self.division = "N/A"
            self.section = "N/A"
            self.color = "N/A"
            self.description = f"{self.name} {self.type} {self.division} {self.section} {self.code} {self.teacher} {self.location} {self.start} - {self.end} {self.day}"


class AttendanceTable():
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
            list(re.sub(' +', ' ', td.text.replace('\n', ' ')) for td in tr) for tr in arr[1:])
        self.body_array = clean(self.body_array)
        try:
            self.heading_array = list(
                list(re.sub(' +', ' ', th.text.replace('\n', ' ')) for th in tr) for tr in
                self.table_heading.findAll("th"))
        except:
            pass
        try:
            self.heading_array = clean(self.heading_array[:])
        except:
            pass
