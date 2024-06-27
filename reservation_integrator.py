from fastapi import FastAPI
from reservation import Reservation
from supersaas_api import SupersaasAPI
import imaplib
import email
from email.header import decode_header
import webbrowser
import os
from datetime import datetime
from icalendar import Calendar, Event, vCalAddress, vText
import requests
from util import get_echalupy_ical, parse_echalupy_date, parse_echalupy_mail
import json
from mail import Mail




# init
app = FastAPI()
key = ""
with open("key", "r") as f:
    key = f.readlines()[0]
    if key[-1]=="\n":
        key = key[:-1]


supersaas_api = SupersaasAPI(key)
credentials = {}
with open("mail_credentials", "r") as f:
    credentials = json.load(f)

mail = Mail(credentials["username"], credentials["password"], credentials["server"])







#@app.get("/sync")
#async 
def sync():
    global mail
    calendar = get_echalupy_ical()
    for event in calendar.walk('VEVENT'):
        reservation = Reservation.from_ical(event)
        if not supersaas_api.test_reservation(reservation):
            supersaas_api.add_reservation(reservation)
        break #TODO: delete

    mails = mail.get_mails()
    for mail in mails:
        mail = parse_echalupy_mail(mail)
        from_date, to_date = parse_echalupy_date(mail["date"])
        reservation = Reservation(from_date, to_date, mail["name"], mail["phone"], mail["count"])
        if not supersaas_api.test_reservation(reservation):
            supersaas_api.add_reservation(reservation, "Z")
        
    return {"message": "OKAY"}


print(sync())
