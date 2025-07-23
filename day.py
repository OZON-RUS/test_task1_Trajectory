from typing import Literal, Union
from utils import get_timestamp, Time
from slot import Slot

class Day:
    __slots__ = ["date", "start", "end", "busy_timeslots", "free_timeslots"]

    def __init__(self, date: str, start: Union[str, Time], end: Union[str, Time]):
        start_cls = start.__class__.__name__
        if start_cls != "Time" and start_cls != "str":
            raise Exception
        elif start_cls == "str":
            start = Time(*start.split(":"))
        
        end_cls = end.__class__.__name__
        if end_cls != "Time" and end_cls != "str":
            raise Exception
        elif end_cls == "str":
            end = Time(*end.split(":"))

        self.date = date
        self.start = start
        self.end = end
        self.free_timeslots = [Slot(start, end)]
        self.busy_timeslots = []
    
    def append(self, slot: Slot):
        if not self._update_free_timeslot(slot):
            return False
        if not self._update_busy_timeslot(slot):
            return False
        return True
        
    def get_free_slots(self):
        return self.free_timeslots
        
    def get_busy_slots(self):
        return self.busy_timeslots

    def find_slot_for_duration(self, duration: Union[int, Time]):
        if duration.__class__.__name__ == "int":
            duration = Time(0, duration)
        i = self.is_available_for_duration(duration)
        if i == -1:
            return False
        start = self.free_timeslots[i].start
        end = start + duration
        return Slot(start, end)

    def is_available_for_duration(self, duration: Union[int, Time]):
        if duration.__class__.__name__ == "int":
            duration = Time(0, duration)
        free_timeslots = self.free_timeslots
        for i, free_timeslot in enumerate(free_timeslots):
            free_timeslot_duration = free_timeslot.end - free_timeslot.start
            if free_timeslot_duration >= duration:
                return i
        return -1

    def is_available(self, slot: Slot):
        free_timeslots = self.free_timeslots
        for i, free_timeslot in enumerate(free_timeslots):
            if slot.issubset(free_timeslot):
                return i
        return -1

    def _update_busy_timeslot(self, slot):
        self.busy_timeslots.append(slot)
        return True

    def _update_free_timeslot(self, slot):
        free_timeslots = self.free_timeslots
        i = self.is_available(slot)
        if i == -1:
            return False
        
        free_timeslot = free_timeslots[i]
        # s.....e
        # +-----+
        if slot.start == free_timeslot.start and slot.end == free_timeslot.end:
            free_timeslots = [*free_timeslots[:i], *free_timeslots[i+1:]]

        #  s..e
        # +-----+
        elif slot.start > free_timeslot.start and slot.end < free_timeslot.end:
            free_timeslots = [*free_timeslots[:i], 
                                Slot(free_timeslot.start, slot.start), Slot(slot.end, free_timeslot.end),
                                *free_timeslots[i+1:]]

        # s..e
        # +......+
        elif slot.start == free_timeslot.start and slot.end < free_timeslot.end:
            free_timeslots = [*free_timeslots[:i], Slot(slot.end, free_timeslot.end), *free_timeslots[i+1:]]

        #     s...e
        # +.......+
        elif slot.start > free_timeslot.start and slot.end == free_timeslot.end:
            free_timeslots = [*free_timeslots[:i], Slot(free_timeslot.start, slot.start), *free_timeslots[i+1:]]

        else:
            raise Exception()
            
        self.free_timeslots = free_timeslots
        return True
        
