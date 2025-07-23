from scheduler import Scheduler
import json

if __name__ == "__main__":
    json_ = """{    "days": [
        {"id": 1, "date": "2024-10-10", "start": "09:00", "end": "18:00"},
        {"id": 2, "date": "2024-10-11", "start": "08:00", "end": "17:00"}
    ],
    "timeslots": [
        {"id": 1, "day_id": 1, "start": "11:00", "end": "12:00"},
        {"id": 3, "day_id": 2, "start": "09:30", "end": "16:00"}
    ]}"""
    dd = json.loads(json_)
    scheduler = Scheduler(json=dd)#"https://ofc-test-01.tspb.su/test-task/")
    print(scheduler.get_busy_slots("2024-10-10"))
    print(scheduler.get_free_slots("2024-10-10"))
    print(scheduler.is_available("2024-10-10", "10:00", "10:30"))
    print(scheduler.is_available("2024-10-10", "11:30", "12:30"))
    print(scheduler.find_slot_for_duration(duration_minutes=60))
    print(scheduler.find_slot_for_duration(duration_minutes=90))
    print(scheduler.find_slot_for_duration(360))

