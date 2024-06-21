import datetime
import icalendar

class Reservation():
    def __init__(self, from_date, to_date, note, status=5):
        self.from_date = from_date
        self.to_date = to_date
        self.note = note
        self.status = status

    @staticmethod
    def from_ical(event):
        return Reservation(
            event.get("DTSTART"),
            event.get("DTEND"),
            event.get("SUMMARY")
        )

    def to_ical(self):
        event = icalendar.Event()
        event.add('SUMMARY', self.note)
        event.add('DTSTART', self.from_date)
        event.add('DTEND', self.to_date)
        return event

        

