
from json import *
import os
data = []
# load json file as a dictionary

with open(r"C:\icloud_resources" + "\\record.json", "r") as fp:
    recoded = load(fp)

with open(r"C:\icloud_resources" + "\\attendance.json", "r") as fp:
    attendRecords = load(fp)

temp = ""
