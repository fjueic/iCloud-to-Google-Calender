
from json import *
data = []
# load json file as a dictionary
with open("record.json", "r") as fp:
    recoded = load(fp)

with open("attendance.json", "r") as fp:
    attendRecords = load(fp)

temp = ""