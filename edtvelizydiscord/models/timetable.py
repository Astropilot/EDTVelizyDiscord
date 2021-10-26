from dataclasses import dataclass
from datetime import datetime
from typing import List


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
        start_time = self.start_date.strftime("%H:%M")
        end_time = self.end_date.strftime("%H:%M")
        return f"{start_time}-{end_time}"


@dataclass(frozen=True)
class TimeTable:
    group_name: str
    weeks: List[Week]
    courses: List[Course]
