import pytest
from day import Day
from slot import Slot
from utils import Time

def test_day_init():
    day = Day("2024-10-10", "09:00", "18:00")
    assert day.date == "2024-10-10"
    assert day.start == Time(9, 0)
    assert day.end == Time(18, 0)
    assert len(day.free_timeslots) == 1
    assert day.free_timeslots[0] == Slot(Time(9, 0), Time(18, 0))
    assert day.busy_timeslots == []

    day_with_time_objects = Day("2024-10-11", Time(8, 0), Time(17, 0))
    assert day_with_time_objects.date == "2024-10-11"
    assert day_with_time_objects.start == Time(8, 0)
    assert day_with_time_objects.end == Time(17, 0)

def test_day_init_invalid_type():
    with pytest.raises(Exception):
        Day("2024-10-10", 900, "18:00")
    with pytest.raises(Exception):
        Day("2024-10-10", "09:00", [1, 2])

def test_day_append_full_slot():
    day = Day("2024-10-10", "09:00", "18:00")
    new_slot = Slot("09:00", "18:00")
    day.append(new_slot)
    assert day.busy_timeslots == [new_slot]
    assert day.free_timeslots == []

def test_day_append_middle_slot():
    day = Day("2024-10-10", "09:00", "18:00")
    new_slot = Slot("11:00", "12:00")
    day.append(new_slot)
    assert day.busy_timeslots == [new_slot]
    expected_free = [Slot("09:00", "11:00"), Slot("12:00", "18:00")]
    assert len(day.free_timeslots) == len(expected_free)
    for i, free_slot in enumerate(day.free_timeslots):
        assert free_slot.start == expected_free[i].start
        assert free_slot.end == expected_free[i].end

def test_day_append_start_slot():
    day = Day("2024-10-10", "09:00", "18:00")
    new_slot = Slot("09:00", "10:00")
    day.append(new_slot)
    assert day.busy_timeslots == [new_slot]
    expected_free = [Slot("10:00", "18:00")]
    assert len(day.free_timeslots) == len(expected_free)
    for i, free_slot in enumerate(day.free_timeslots):
        assert free_slot.start == expected_free[i].start
        assert free_slot.end == expected_free[i].end

def test_day_append_end_slot():
    day = Day("2024-10-10", "09:00", "18:00")
    new_slot = Slot("17:00", "18:00")
    day.append(new_slot)
    assert day.busy_timeslots == [new_slot]
    expected_free = [Slot("09:00", "17:00")]
    assert len(day.free_timeslots) == len(expected_free)
    for i, free_slot in enumerate(day.free_timeslots):
        assert free_slot.start == expected_free[i].start
        assert free_slot.end == expected_free[i].end

def test_day_append_multiple_slots():
    day = Day("2024-10-10", "09:00", "18:00")
    slot1 = Slot("10:00", "11:00")
    slot2 = Slot("14:00", "15:00")
    day.append(slot1)
    day.append(slot2)
    assert day.busy_timeslots == [slot1, slot2]
    expected_free = [Slot("09:00", "10:00"), Slot("11:00", "14:00"), Slot("15:00", "18:00")]
    assert len(day.free_timeslots) == len(expected_free)
    for i, free_slot in enumerate(day.free_timeslots):
        assert free_slot.start == expected_free[i].start
        assert free_slot.end == expected_free[i].end

def test_day_append_overlapping_slot():
    day = Day("2024-10-10", "09:00", "18:00")
    day.append(Slot("10:00", "12:00"))
    # Trying to append a slot that partially overlaps or is outside a free slot,
    # or would cause an exception based on current _update_free_timeslot logic for non-subset
    # The current implementation of _update_free_timeslot assumes the new slot is a subset.
    # If it's not, `is_available` returns -1 and `_update_free_timeslot` returns False.
    # This test ensures that behavior.
    assert not day.append(Slot("11:30", "13:00"))
    assert not day.append(Slot("08:00", "09:30"))
    assert not day.append(Slot("08:00", "19:00"))

def test_day_get_free_slots():
    day = Day("2024-10-10", "09:00", "18:00")
    day.append(Slot("11:00", "12:00"))
    free_slots = day.get_free_slots()
    expected_free = [Slot("09:00", "11:00"), Slot("12:00", "18:00")]
    assert len(free_slots) == len(expected_free)
    for i, free_slot in enumerate(free_slots):
        assert free_slot.start == expected_free[i].start
        assert free_slot.end == expected_free[i].end

def test_day_get_busy_slots():
    day = Day("2024-10-10", "09:00", "18:00")
    slot1 = Slot("10:00", "11:00")
    slot2 = Slot("14:00", "15:00")
    day.append(slot1)
    day.append(slot2)
    busy_slots = day.get_busy_slots()
    assert busy_slots == [slot1, slot2]

def test_day_find_slot_for_duration():
    day = Day("2024-10-10", "09:00", "18:00")
    day.append(Slot("11:00", "12:00")) # Creates free slots: 09:00-11:00, 12:00-18:00

    # Find 60 minutes
    found_slot = day.find_slot_for_duration(60)
    assert found_slot.start == Time(9, 0)
    assert found_slot.end == Time(10, 0)

    # Find 90 minutes
    found_slot_90 = day.find_slot_for_duration(90)
    assert found_slot_90.start == Time(9, 0)
    assert found_slot_90.end == Time(10, 30)

    # Find a duration that only fits in the second free slot
    found_slot_long = day.find_slot_for_duration(300) # 5 hours
    assert found_slot_long.start == Time(12, 0)
    assert found_slot_long.end == Time(17, 0)

    # No slot for very long duration
    assert day.find_slot_for_duration(700) is False # More than available max free slot (6 hours)

    # Empty day
    day_empty = Day("2024-10-12", "09:00", "09:30")
    assert day_empty.find_slot_for_duration(60) is False


def test_day_is_available_for_duration():
    day = Day("2024-10-10", "09:00", "18:00")
    day.append(Slot("11:00", "12:00")) # Free: 09:00-11:00, 12:00-18:00

    # Fits in first slot
    assert day.is_available_for_duration(60) != -1

    # Fits in second slot
    assert day.is_available_for_duration(200) != -1

    # Does not fit anywhere
    assert day.is_available_for_duration(400) == -1 # 400 minutes = 6h 40m. Max free slot is 6h.

def test_day_is_available():
    day = Day("2024-10-10", "09:00", "18:00")
    day.append(Slot("11:00", "12:00")) # Free: 09:00-11:00, 12:00-18:00

    # Available in first slot
    assert day.is_available(Slot("09:30", "10:30")) != -1

    # Available in second slot
    assert day.is_available(Slot("13:00", "14:00")) != -1

    # Not available (overlaps busy)
    assert day.is_available(Slot("11:30", "12:30")) == -1

    # Not available (outside of day bounds)
    assert day.is_available(Slot("08:00", "09:30")) == -1

    # Not available (overlaps beginning of busy)
    assert day.is_available(Slot("10:30", "11:30")) == -1

    # Not available (overlaps end of busy)
    assert day.is_available(Slot("11:30", "12:30")) == -1