import requests
import json
class SupersaasAPI():
    def __init__(self, key, url="https://supersaas.com/api"):
        self.key = key
        self.url = url
        self.shedule_id = 728075 

    "2024-01-18T13:00:00"
    def add_reservation(self, reservation, status="R"):

        f =  reservation.from_date.strftime("%Y-%m-%d 13:00:00")
        d = reservation.to_date.strftime("%Y-%m-%d 10:00:00")
        #try all seven slots, if it doesnt work we are fucked
        for i in range(7):
            url = f"{self.url}/bookings.json?schedule_id={self.shedule_id}&api_key={self.key}&booking[start]={f}&booking[finish]={d}&booking[full_name]={reservation.note}&booking[resource_id]=slot{i+1}&booking[field_1_r]={status}"
            if(reservation.name is not None):
                url+=f"&booking[full_name]={reservation.name}"
            if(reservation.number is not None):
                url+=f"&booking[mobile]={reservation.number}"
            if(reservation.note is not None):
                url+=f"&booking[field_2_r]={reservation.note}"

            x = requests.post(url)
            print(x.status_code)
            print(x.text)
            if x.status_code == 422:
                continue
            else:
                break
        else:
            print("fuck") #TODO: email notification


    def test_reservation(self, reservation):
        f =  reservation.from_date.strftime("%Y-%m-%d 10:00:00")
        d = reservation.to_date.strftime("%Y-%m-%d 13:00:00")

        x = requests.get(f"{self.url}/range/{self.shedule_id}.json?api_key={self.key}&from={f}&to={d}")

        reservations = json.loads(x.text)["bookings"]
        #compare dates and name for equality
        for r in reservations:
            if (
                reservation.from_date.strftime("%Y-%m-%d") == r["start"].split("T")[0] or 
                reservation.to_date.strftime("%Y-%m-%d") == r["finish"].split("T")[0] or 
                reservation.note == r["full_name"]
            ):
                return True

        return False
