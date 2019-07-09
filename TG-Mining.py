import os
import requests
from DSBMobile import DSBMobile

# Settings
username = "<user>"
password = "<pass>"
dataFolder   = "data/"

# Pull timetable from server
print("Pull timetable from server...")
dsb = DSBMobile(username, password)
timeTable = dsb.getTimeTables()[0]

# Check if data folder exists
if not os.path.isdir(dataFolder):
    print("Data folder does not exist! Creating one...")
    os.mkdir(dataFolder)

# Check if we are up-to-date
timeTableFile = dataFolder + timeTable.date.replace(" ", "_").replace(":", "-") + ".htm"
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