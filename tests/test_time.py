from utils import Time



def test_time_init():
    t = Time(10, 30)
    assert t.hours == 10
    assert t.minutes == 30

    t_overflow = Time(9, 90)
    assert t_overflow.hours == 10
    assert t_overflow.minutes == 30

    t_large_overflow = Time(5, 125)
    assert t_large_overflow.hours == 7
    assert t_large_overflow.minutes == 5

def test_time_eq():
    assert Time(10, 30) == Time(10, 30)
    assert Time(9, 90) == Time(10, 30)
    assert not (Time(10, 30) == Time(10, 31))
    assert not (Time(11, 30) == Time(10, 30))

def test_time_ne():
    assert Time(10, 30) != Time(10, 31)
    assert not (Time(10, 30) != Time(10, 30))

def test_time_gt():
    assert Time(11, 0) > Time(10, 30)
    assert Time(10, 45) > Time(10, 30)
    assert not (Time(10, 30) > Time(10, 30))
    assert not (Time(9, 30) > Time(10, 30))

def test_time_lt():
    assert Time(9, 0) < Time(10, 30)
    assert Time(10, 15) < Time(10, 30)
    assert not (Time(10, 30) < Time(10, 30))
    assert not (Time(11, 30) < Time(10, 30))

def test_time_ge():
    assert Time(11, 0) >= Time(10, 30)
    assert Time(10, 45) >= Time(10, 30)
    assert Time(10, 30) >= Time(10, 30)
    assert not (Time(9, 30) >= Time(10, 30))

def test_time_le():
    assert Time(9, 0) <= Time(10, 30)
    assert Time(10, 15) <= Time(10, 30)
    assert Time(10, 30) <= Time(10, 30)
    assert not (Time(11, 30) <= Time(10, 30))

def test_time_sub():
    t1 = Time(12, 0)
    t2 = Time(10, 30)
    result = t1 - t2
    assert result.hours == 1
    assert result.minutes == 30

    t3 = Time(10, 15)
    t4 = Time(9, 30)
    result2 = t3 - t4
    assert result2.hours == 0
    assert result2.minutes == 45

    t5 = Time(10, 30)
    t6 = Time(10, 0)
    result3 = t5 - t6
    assert result3.hours == 0
    assert result3.minutes == 30

def test_time_add():
    t1 = Time(10, 30)
    t2 = Time(1, 45)
    result = t1 + t2
    assert result.hours == 12
    assert result.minutes == 15

    t3 = Time(9, 0)
    t4 = Time(0, 30)
    result2 = t3 + t4
    assert result2.hours == 9
    assert result2.minutes == 30

    t5 = Time(23, 30)
    t6 = Time(1, 0)
    result3 = t5 + t6
    assert result3.hours == 24 # Should handle hours > 23 for internal calculations if needed, or define bounds
    assert result3.minutes == 30

def test_time_str_repr():
    t = Time(9, 5)
    assert str(t) == "09:05"
    assert repr(t) == "09:05"

    t2 = Time(14, 30)
    assert str(t2) == "14:30"
    assert repr(t2) == "14:30"