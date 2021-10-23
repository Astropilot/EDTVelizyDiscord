from typing import List, Optional
from datetime import datetime


class Week:

    def __init__(self, week_date: datetime, index: int) -> None:
        self.week_date: datetime = week_date
        self.index = index


class Course:

    def __init__(self, start_date: datetime, end_date: datetime, module: str, staff: str, room: str) -> None:
        self.start_date: datetime = start_date
        self.end_date: datetime = end_date
        self.module: str = module
        self.staff: str = staff
        self.room: str = room


class TimeTable:

    def __init__(self, weeks: List[Week], courses: List[Course]) -> None:
        self.weeks: List[Week] = weeks
        self.courses: List[Course] = courses
