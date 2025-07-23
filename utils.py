from datetime import datetime
import operator

class Time:
    def __init__(self, hours: int, minutes: int):
        hours = int(hours)
        minutes = int(minutes)
        hours_add = minutes // 60
        
        self.hours = hours + hours_add
        self.minutes = minutes - hours_add * 60
    def __eq__(self, value):
            if self.hours == value.hours and self.minutes == value.minutes:
                return True
            else:
                return False
    def __ne__(self, value):
        return not self.__eq__(value)
    
    def __gt__(self, value):
        if self.hours > value.hours:
            return True
        elif self.hours < value.hours:
            return False
        elif self.minutes > value.minutes:
            return True
        else:
            False

    def __lt__(self, value):
        if self.hours < value.hours:
            return True
        elif self.hours > value.hours:
            return False
        elif self.minutes < value.minutes:
            return True
        else:
            False

    def __ge__(self, value):
        return self.__gt__(value) or self.__eq__(value)
    
    def __le__(self, value):
        return self.__lt__(value) or self.__eq__(value)

    def __sub__(self, other):
        min_sub = self.minutes - other.minutes
        if min_sub < 0:
            return Time(self.hours - other.hours - 1, 60 + min_sub)
        else:
            return Time(self.hours - other.hours, min_sub)
    
    def __add__(self, other):
        min_add = self.minutes + other.minutes
        if min_add >= 60:
            return Time(self.hours + other.hours + 1, min_add - 60)
        else:
            return Time(self.hours + other.hours, min_add)
    
    def __str__(self):
        return "{:02}".format(self.hours) + ":" + "{:02}".format(self.minutes)
    
    def __repr__(self):
        return self.__str__()
    
def get_timestamp(timeslot):
            start_ = timeslot[0].split(":")
            end_ = timeslot[1].split(":")
            start_ts = Time(int(start_[0]), int(start_[1]))
            end_ts = Time(int(end_[0]), int(end_[1]))
            return start_ts, end_ts