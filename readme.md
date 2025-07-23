To provide the documentation and unit tests in English, here they are:

-----

# Schedule Management System

This system is a simple schedule planner that allows you to manage free and busy time slots throughout the day. It can load schedule data from a JSON source and provides functionality to check availability and find free slots.

## Table of Contents

  - [Schedule Management System](#schedule-management-system)
      - [Table of Contents](#table-of-contents)
      - [Overview](#overview)
      - [Project Structure](#project-structure)
      - [Installation](#installation)
      - [Usage](#usage)
          - [Example Usage](#example-usage)
      - [Running Tests](#running-tests)
      - [Classes and Their Functionality](#classes-and-their-functionality)
          - [`Time`](#time)
          - [`Slot`](#slot)
          - [`Day`](#day)
          - [`Scheduler`](#scheduler)

## Overview

The project provides basic functionality for working with schedules:

  - **`Time`**: Manages time (hours and minutes) with support for arithmetic operations and comparisons.
  - **`Slot`**: Represents a time interval with a start and an end, and checks for inclusion within another interval.
  - **`Day`**: Manages the schedule for a specific day, tracking free and busy time slots.
  - **`Scheduler`**: The main class for loading and managing schedules across multiple days, allowing you to check availability and find free slots for a given duration.

## Project Structure

```
your_project/
├── main.py             # Main executable file for demonstration
├── day.py              # Day class definition
├── scheduler.py        # Scheduler class definition
├── slot.py             # Slot class definition
├── utils.py            # Utilities, including the Time class
└── tests/
    ├── __init__.py
    ├── test_time.py    # Tests for the Time class
    ├── test_slot.py    # Tests for the Slot class
    ├── test_day.py     # Tests for the Day class
    └── test_scheduler.py # Tests for the Scheduler class
```

## Installation

To run this project, you will need Python 3.x.
Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Install the necessary dependencies (if any; in this case, `requests` for potential URL usage, but it's commented out in the current `main.py`):

```bash
pip install -r requirements.txts
```

## Usage

The project can be used to manage schedules. You can initialize the `Scheduler` with JSON data.

### Example Usage

You can run `main.py` for a demonstration of the core functionality:

```bash
python main.py
```

`main.py` contains an example of initializing the `Scheduler` from a JSON string and prints various results, such as busy slots, free slots, availability checks, and finding a slot by duration.

#### With JSON

```python
# Example from main.py
from scheduler import Scheduler
import json

if __name__ == "__main__":
    json_data = """{
        "days": [
            {"id": 1, "date": "2024-10-10", "start": "09:00", "end": "18:00"},
            {"id": 2, "date": "2024-10-11", "start": "08:00", "end": "17:00"}
        ],
        "timeslots": [
            {"id": 1, "day_id": 1, "start": "11:00", "end": "12:00"},
            {"id": 3, "day_id": 2, "start": "09:30", "end": "16:00"}
        ]
    }"""
    
    data = json.loads(json_data)
    scheduler = Scheduler(json=data)

    print("Busy slots on 2024-10-10:", scheduler.get_busy_slots("2024-10-10"))
    print("Free slots on 2024-10-10:", scheduler.get_free_slots("2024-10-10"))
    print("Is 2024-10-10 from 10:00 to 10:30 available?", scheduler.is_available("2024-10-10", "10:00", "10:30"))
    print("Is 2024-10-10 from 11:30 to 12:30 available?", scheduler.is_available("2024-10-10", "11:30", "12:30"))
    print("Find a slot for 60 minutes:", scheduler.find_slot_for_duration(duration_minutes=60))
```

#### With URL

```python
# Example from main.py
from scheduler import Scheduler
import json

if __name__ == "__main__":
    url = "https://ofc-test-01.tspb.su/test-task/"
    scheduler = Scheduler(url=url)

    print("Busy slots on 2025-02-15:", scheduler.get_busy_slots("2025-02-15"))
    print("Free slots on 2025-02-15:", scheduler.get_free_slots("2025-02-15"))
    print("Is 2025-02-15 from 10:00 to 10:30 available?", scheduler.is_available("2025-02-15", "10:00", "10:30"))
    print("Is 2025-02-15 from 11:30 to 12:30 available?", scheduler.is_available("2025-02-15", "11:30", "12:30"))
    print("Find a slot for 60 minutes:", scheduler.find_slot_for_duration(duration_minutes=60))
```

## Running Tests

Unit tests are written using the `pytest` framework. To run them, navigate to the root directory of your project and execute:

```bash
pytest
```

This will discover and run all tests in the `tests/` directory.

## Classes and Their Functionality

### `Time`

Represents time in hours and minutes.

  - **`__init__(self, hours: int, minutes: int)`**: Constructor. Automatically corrects minutes exceeding 60 (e.g., 90 minutes becomes 1 hour 30 minutes).
  - **`__eq__(self, value)`**: Checks for equality between two `Time` objects.
  - **`__ne__(self, value)`**: Checks for inequality.
  - **`__gt__(self, value)`**: Checks "greater than".
  - **`__lt__(self, value)`**: Checks "less than".
  - **`__ge__(self, value)`**: Checks "greater than or equal to".
  - **`__le__(self, value)`**: Checks "less than or equal to".
  - **`__sub__(self, other)`**: Subtracts one `Time` object from another, returning the difference as a new `Time` object.
  - **`__add__(self, other)`**: Adds two `Time` objects, returning a new `Time` object.
  - **`__str__(self)` / `__repr__(self)`**: Returns a string representation of the time in `HH:MM` format.

### `Slot`

Represents a time interval.

  - **`__init__(self, start: Union[Time, str], end: Union[Time, str])`**: Constructor. Accepts `Time` objects or strings in "HH:MM" format.
  - **`issubset(self, set_slot: Slot)`**: Checks if the current `Slot` is a subset of `set_slot`.
  - **`__repr__(self)`**: Returns a string representation of the slot in `(HH:MM, HH:MM)` format.

### `Day`

Manages the schedule for a single specific day.

  - **`__init__(self, date: str, start: Union[str, Time], end: Union[str, Time])`**: Constructor. `date` is a date string (e.g., "2024-10-10"), `start` and `end` are the start and end times of the workday. Initially, the entire day is considered free.
  - **`append(self, slot: Slot)`**: Adds a busy `slot` to the day's schedule, updating the list of free slots accordingly. Returns `True` on successful addition, `False` otherwise.
  - **`get_free_slots(self)`**: Returns a list of free slots.
  - **`get_busy_slots(self)`**: Returns a list of busy slots.
  - **`find_slot_for_duration(self, duration: Union[int, Time])`**: Finds the first free slot that can accommodate the given `duration` (in minutes or as a `Time` object). Returns the found `Slot` or `False` if no slot is found.
  - **`is_available_for_duration(self, duration: int)`**: Checks if there is a free slot of the specified duration (in minutes). Returns the index of the free slot or `-1`.
  - **`is_available(self, slot: Slot)`**: Checks if the given `slot` is available in the day's schedule (i.e., it does not overlap with busy slots and is within the workday boundaries). Returns the index of the free slot that `slot` fits into, or `-1`.
  - **`_get_duration(self, timeslot: Slot)`**: Internal method to calculate the duration of a slot in minutes.
  - **`_update_busy_timeslot(self, slot)`**: Internal method to add a slot to the busy list.
  - **`_update_free_timeslot(self, slot)`**: Internal method to update the list of free slots after a busy slot has been added.

### `Scheduler`

The main class for managing schedules across multiple days.

  - **`__init__(self, url=None, json=None)`**: Constructor. Initializes the schedule either from a URL (commented out in the current version) or from a JSON object. The JSON should contain `days` and `timeslots` keys.
  - **`get_busy_slots(self, date)`**: Returns a list of busy slots for the specified date.
  - **`get_free_slots(self, date)`**: Returns a list of free slots for the specified date.
  - **`is_available(self, date, start, end)`**: Checks if the specified time interval is available on the given date.
  - **`find_slot_for_duration(self, duration_minutes)`**: Searches for the first available slot of the specified duration (in minutes) across all days in the schedule. Returns a tuple `(date, start_time, end_time)` or `False` if no slot is found.
  - **`_get_day_by_date(self, date)`**: Internal method to retrieve a `Day` object by date.

-----
