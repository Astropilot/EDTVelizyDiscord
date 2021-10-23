from core.timetable import get_local_timetable
from models.timetable import TimeTable


timetable: TimeTable = get_local_timetable(178207)

for course in timetable.courses:
    print(f'{course.module}: {course.start_date} -> {course.end_date}')
