from typing import Union
from utils import Time

class Slot:
    pass

class Slot:
    def __init__(self, start: Union[Time, str], end: Union[Time, str]):
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
        
        self.start = start
        self.end = end

    def issubset(self, set_slot: Slot):
        return set_slot.start <= self.start and set_slot.end >= self.end
    
    def __repr__(self):
        return f"({self.start}, {self.end})"
    
    def __eq__(self, value: Slot):
        return value.start == self.start and value.end == self.end