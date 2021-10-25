from typing import List
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Week:
    week_date: datetime
    index: int


@dataclass(frozen=True)
class Course:
    week: Week
    start_date: datetime
    end_date: datetime
    module: str
    staff: str
    room: str

    @property
    def pretty_times(self) -> str:
        return f'{self.start_date.strftime("%H:%M")}-{self.end_date.strftime("%H:%M")}'

@dataclass(frozen=True)
class TimeTable:
    group_name: str
    weeks: List[Week]
    courses: List[Course]
