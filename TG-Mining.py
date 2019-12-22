import os
import time
import requests
from DSBMobile import DSBMobile

# Settings
username = "<user>"
password = "<pass>"
dataFolder   = "data/"

# Pull timetable from server
print("Pulling timetable from server...")
dsb = DSBMobile(username, password)
timeTable = dsb.getTimeTables()[0]

# Check if data folder exists
if not os.path.isdir(dataFolder):
    print("Data folder does not exist! Creating one...")
    os.mkdir(dataFolder)

# Generate file name
timeTableDate = time.strptime(timeTable.date, "%d.%m.%Y %H:%M")
timeTableFile = dataFolder + time.strftime("%Y-%m-%d_%H-%M", timeTableDate) + ".htm"

# Check if we are up-to-date
if not os.path.isfile(timeTableFile):
    print("We are NOT up-to-date!")
    print("Downloading timetable...")
    response = requests.get(timeTable.url, stream=True)
    if response.status_code == 200:
        with open(timeTableFile, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print("done!")
    else:
        print("Error: Status code is " + response.status_code + "!")
else:
    print("We are up-to-date!")