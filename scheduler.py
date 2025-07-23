import requests
from requests.exceptions import HTTPError
from day import Day
from slot import Slot
from utils import get_timestamp, Time

class Scheduler:
    __slots__ = ["days"]
    days: dict

    def __init__(self, url=None, json=None):
        if json is not None:
            days = json.get("days")
            timeslots = json.get("timeslots")
        else:
            response = requests.get(url)
            if response.status_code != 200:
                raise HTTPError(response=response)
            response: dict = response.json()
            days: list[dict] = response.get("days")
            timeslots: list[dict] = response.get("timeslots")
            if days is None or timeslots is None:
                raise Exception(days, timeslots)

        

        days_by_id: dict[Day] = {}
        for day in days:
            day_id = day.pop("id")
            days_by_id[day_id] = Day(**day)
        
        for timeslot in timeslots:
            day_id = timeslot.pop("day_id")
            day: Day = days_by_id[day_id]
            timeslot.pop("id")
            timeslot = Slot(**timeslot)
            day.append(timeslot)

        self.days = {}
        for day_id in days_by_id.keys():
            day = days_by_id[day_id]
            self.days[day.date] = day

    def get_busy_slots(self, date):
        day: Day = self._get_day_by_date(date)
        busy_slots = day.get_busy_slots()
        return busy_slots

    def get_free_slots(self, date):
        day: Day = self._get_day_by_date(date)
        free_slots = day.get_free_slots()
        return free_slots

    def is_available(self, date, start, end):
        day: Day = self._get_day_by_date(date)
        slot: Slot = Slot(start, end)
        is_available = day.is_available(slot)
        if is_available == -1:
            return False
        return True

    def find_slot_for_duration(self, duration_minutes):
        for date in self.days.keys():
            day: Day = self._get_day_by_date(date)
            slot = day.find_slot_for_duration(duration_minutes)
            if slot is False:
                continue
            return (day.date, slot.start, slot.end)
        return False

    def _get_day_by_date(self, date):
        return self.days[date]