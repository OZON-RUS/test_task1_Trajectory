import pytest
from slot import Slot
from utils import Time

def test_slot_init_with_time_objects():
    start_time = Time(9, 0)
    end_time = Time(10, 30)
    slot = Slot(start_time, end_time)
    assert slot.start == start_time
    assert slot.end == end_time

def test_slot_init_with_strings():
    slot = Slot("09:00", "10:30")
    assert slot.start == Time(9, 0)
    assert slot.end == Time(10, 30)

def test_slot_init_invalid_type():
    with pytest.raises(Exception):
        Slot(123, "10:00")
    with pytest.raises(Exception):
        Slot("09:00", [1, 2])

def test_slot_issubset():
    parent_slot = Slot("09:00", "12:00")

    # Exact match
    assert Slot("09:00", "12:00").issubset(parent_slot)

    # Subset
    assert Slot("09:30", "11:00").issubset(parent_slot)

    # Starts at same time, ends earlier
    assert Slot("09:00", "10:00").issubset(parent_slot)

    # Starts later, ends at same time
    assert Slot("10:00", "12:00").issubset(parent_slot)

    # Overlaps start
    assert not Slot("08:30", "09:30").issubset(parent_slot)

    # Overlaps end
    assert not Slot("11:30", "12:30").issubset(parent_slot)

    # Completely outside
    assert not Slot("08:00", "08:30").issubset(parent_slot)
    assert not Slot("12:30", "13:00").issubset(parent_slot)

def test_slot_repr():
    slot = Slot("09:00", "10:30")
    assert repr(slot) == "(09:00, 10:30)"