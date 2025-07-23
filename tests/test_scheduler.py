import pytest
from scheduler import Scheduler
from slot import Slot
from utils import Time
import json

@pytest.fixture
def sample_scheduler_json():
    return {
        "days": [
            {"id": 1, "date": "2024-10-10", "start": "09:00", "end": "18:00"},
            {"id": 2, "date": "2024-10-11", "start": "08:00", "end": "17:00"}
        ],
        "timeslots": [
            {"id": 1, "day_id": 1, "start": "11:00", "end": "12:00"},
            {"id": 3, "day_id": 2, "start": "09:30", "end": "16:00"}
        ]
    }

def test_scheduler_init(sample_scheduler_json):
    scheduler = Scheduler(json=sample_scheduler_json)
    assert "2024-10-10" in scheduler.days
    assert "2024-10-11" in scheduler.days

    day1 = scheduler.days["2024-10-10"]
    assert day1.start == Time(9, 0)
    assert day1.end == Time(18, 0)
    assert Slot("11:00", "12:00") in day1.busy_timeslots

    day2 = scheduler.days["2024-10-11"]
    assert day2.start == Time(8, 0)
    assert day2.end == Time(17, 0)
    assert Slot("09:30", "16:00") in day2.busy_timeslots

def test_get_busy_slots(sample_scheduler_json):
    scheduler = Scheduler(json=sample_scheduler_json)
    busy_slots_day1 = scheduler.get_busy_slots("2024-10-10")
    assert len(busy_slots_day1) == 1
    assert busy_slots_day1[0] == Slot("11:00", "12:00")

    busy_slots_day2 = scheduler.get_busy_slots("2024-10-11")
    assert len(busy_slots_day2) == 1
    assert busy_slots_day2[0] == Slot("09:30", "16:00")

def test_get_free_slots(sample_scheduler_json):
    scheduler = Scheduler(json=sample_scheduler_json)
    free_slots_day1 = scheduler.get_free_slots("2024-10-10")
    expected_free_day1 = [Slot("09:00", "11:00"), Slot("12:00", "18:00")]
    assert len(free_slots_day1) == len(expected_free_day1)
    for i, slot in enumerate(free_slots_day1):
        assert slot.start == expected_free_day1[i].start
        assert slot.end == expected_free_day1[i].end

    free_slots_day2 = scheduler.get_free_slots("2024-10-11")
    expected_free_day2 = [Slot("08:00", "09:30"), Slot("16:00", "17:00")]
    assert len(free_slots_day2) == len(expected_free_day2)
    for i, slot in enumerate(free_slots_day2):
        assert slot.start == expected_free_day2[i].start
        assert slot.end == expected_free_day2[i].end

def test_is_available(sample_scheduler_json):
    scheduler = Scheduler(json=sample_scheduler_json)

    # Available slot
    assert scheduler.is_available("2024-10-10", "10:00", "10:30") is True
    assert scheduler.is_available("2024-10-10", "12:00", "13:00") is True
    assert scheduler.is_available("2024-10-11", "08:00", "09:00") is True

    # Unavailable (within busy slot)
    assert scheduler.is_available("2024-10-10", "11:30", "12:30") is False
    assert scheduler.is_available("2024-10-11", "10:00", "11:00") is False

    # Unavailable (outside day bounds)
    assert scheduler.is_available("2024-10-10", "08:00", "08:30") is False
    assert scheduler.is_available("2024-10-10", "18:00", "19:00") is False

def test_find_slot_for_duration(sample_scheduler_json):
    scheduler = Scheduler(json=sample_scheduler_json)

    # Find 60 minutes on 2024-10-10
    slot_found_60 = scheduler.find_slot_for_duration(60)
    assert slot_found_60 == ("2024-10-10", Time(9, 0), Time(10, 0))

    # Find 90 minutes on 2024-10-10
    slot_found_90 = scheduler.find_slot_for_duration(90)
    assert slot_found_90 == ("2024-10-10", Time(9, 0), Time(10, 30))

    # Find a slot on 2024-10-11 (smaller initial free slots)
    scheduler_with_less_free_time = Scheduler(json={
        "days": [{"id": 1, "date": "2024-10-10", "start": "09:00", "end": "10:00"}],
        "timeslots": []
    })
    # First day has only 1 hour free. If we need more, it should move to the next day.
    # In the original fixture, 2024-10-10 has max 2 hours free (09:00-11:00)
    # 2024-10-11 has (08:00-09:30) (16:00-17:00) - max 1.5 hours free (90 mins)
    slot_found_2hours = scheduler.find_slot_for_duration(120) # 2 hours
    assert slot_found_2hours == ("2024-10-10", Time(9, 0), Time(11, 0))

    # Test when no slot is found
    assert scheduler.find_slot_for_duration(360) is not False
    assert scheduler.find_slot_for_duration(361) is False