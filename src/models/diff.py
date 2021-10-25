from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from .timetable import Course


class DiffType(Enum):
    ADDED = 1
    REMOVED = 2
    UPDATED = 3


class ModifiedOnType(Enum):
    MODULE = 1
    STAFF = 2
    ROOM = 3


@dataclass(frozen=True)
class CourseDiff:
    type: DiffType
    course: Course
    compare_to: Optional[Course] = None
    modified_on: Optional[List[ModifiedOnType]] = None
