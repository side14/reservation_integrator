import datetime
import icalendar

class Reservation():
    def __init__(self, from_date, to_date, name, number=None, note=None):
        self.from_date = from_date
        self.to_date = to_date
        self.name = name
        self.number = number
        self.note = note

    @staticmethod
    def from_ical(event):
        return Reservation(
            event.get("DTSTART").dt,
            event.get("DTEND").dt,
            event.get("SUMMARY")
        )

    def to_ical(self):
        event = icalendar.Event()
        event.add('SUMMARY', self.name)
        event.add('DTSTART', self.from_date)
        event.add('DTEND', self.to_date)
        return event

        

