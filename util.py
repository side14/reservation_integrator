from icalendar import Calendar
import requests
from datetime import datetime

def get_echalupy_ical():
    url = "https://www.e-chalupy.cz/api/iCal.php?id=12350&klic=F32167c2db80103"
    # init the calendar
    cal = Calendar()
    # Some properties are required to be compliant
    cal.add('prodid', '-//My calendar product//example.com//')
    cal.add('version', '2.0')

     

    f = requests.get(url)
    if f.status_code == 200:

        # fix the incorrect formatting of the file, e-chalupy ftw
        # there is very little point in explaining what exactly it does, just compare the files before and after to see the difference

        ics = f.text.replace("\\r", "").replace("\\n", "\n")
        new_ics = ""
        # consume the old ics while building the new one
        while(ics!=""):
            for i, c in enumerate(ics):
                if c == ":":
                    #string manipulation, what fun
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

        return Calendar.from_ical(ics)


def parse_echalupy_date(d):
    # the date is inputed as a string
    # meaning that finite automata is the only option really
    from_date = { # also serves as a state variable
        "day": None,
        "month": None,
        "year": None,
    }
    to_date = { # also serves as a state variable
        "day": None,
        "month": None,
        "year": None,
    }

    mode_from = True # keep an information whether I am reading from or to
    number_str = ""
    for c in d+"-": 
        if c == " ":
            continue
        
        if c in "0123456789":
            number_str+=c
        
        
        # python doesnt have switch statements so we get this
        if (c == "." or c=="-")  and len(number_str) != 0:
            if mode_from:
                if from_date["day"] is None:
                    from_date["day"] = int(number_str)
                elif from_date["month"] is None:
                    from_date["month"] = int(number_str)
                elif from_date["year"] is None:
                    from_date["year"] = int(number_str)
            else:
               if to_date["day"] is None:
                    to_date["day"] = int(number_str)
               elif to_date["month"] is None:
                    to_date["month"] = int(number_str)
                    if from_date["month"] is None:
                        from_date["month"] = int(number_str)

               elif to_date["year"] is None:
                    to_date["year"] = int(number_str)
                    if from_date["year"] is None:
                        from_date["year"] = int(number_str)


            number_str = ""
        if c == "-":
            mode_from = False


    return datetime(from_date["year"], from_date["month"], from_date["day"]), datetime(to_date["year"], to_date["month"], to_date["day"])


def parse_echalupy_mail(mail):
    strings = [
    ("date", "Požadovaný termín:"),
    ("count", "Počet osob:"),
    ("name", "Odeslal:"),
    ("phone", "Telefon:")
    ]
    
    collected = {}
    for str_tuple in strings:
        string = str_tuple[1]
        position = mail.find(string)
        count = 0
        for c in mail[position + len(string):]:
            if c == "\n":
                break
            count+=1

        collected[str_tuple[0]] = mail[position+len(string)+1:position+len(string)+count]


    return collected
    
