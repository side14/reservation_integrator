from fastapi import FastAPI
from reservation import Reservation

app = FastAPI()
from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime
from pathlib import Path
import os
import pytz
 
# init the calendar
cal = Calendar()
# Some properties are required to be compliant
cal.add('prodid', '-//My calendar product//example.com//')
cal.add('version', '2.0')

 


path_to_ics_file = "export.ics"
with open(path_to_ics_file) as f:

    # fix the incorrect formatting of the file, e-chalupy ftw
    # there is very little point in explaining what exactly it does, just compare the files before and after to see the difference

    ics = f.read().replace("\\r", "").replace("\\n", "\n")
    new_ics = ""
    while(ics!=""):
        for i, c in enumerate(ics):
            if c == ":":
                #string manipulation what fun
                temp = ics[:i+1]
                ics = ics[i+1:]
                while temp[i-1] != " " and temp[i-1] != ":" and temp[i-1] != "\n":
                    i-=1
                    if i < 1:
                        break
                
                new_ics+=temp[:i-(temp[i-1] == " ")] + "\r\n" + temp[i:]


                break
        else:
            break
    ics = new_ics + "VCALENDAR"

    print(ics)
    calendar = Calendar.from_ical(ics)
events = []
for event in calendar.walk('VEVENT'):
    events.append(Reservation.from_ical(event))
for reservation in events:
    cal.add_component(reservation.to_ical())

print(cal.to_ical())
@app.get("/sync")
async def root():
    return {"message": "Hello World"}
