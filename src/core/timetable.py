import requests
import pathlib
import xml.etree.ElementTree as ElementTree
from datetime import datetime, timedelta
from typing import List, Optional, Dict

from models.timetable import TimeTable, Week, Course


def convert_xml_to_timetable(timetable_xml: str) -> Optional[TimeTable]:
    root = ElementTree.fromstring(timetable_xml)

    weeks: Dict[int, Week] = {}
    courses: List[Course] = []

    for week in root.findall('span'):
        week_date: datetime = datetime.strptime(week.get('date'), '%d/%m/%Y')
        week_index: int = int(week.get('rawix'))

        weeks[week_index] = Week(week_date, week_index)

    for course in root.findall('event'):
        week_index: int = course.find('rawweeks').text.index('Y') + 1
        week: Week = weeks.get(week_index)
        day: int = int(course.find('day').text)
        times: str = course.get('timesort')

        start_date: datetime = week.week_date + timedelta(days=day)
        end_date: datetime = week.week_date + timedelta(days=day)
        module: str = '[Cours sans nom]'
        staff: str = ''
        room: str = ''

        start_date = start_date.replace(hour=int(times[0:2]), minute=int(times[2:4]))
        end_date = end_date.replace(hour=int(times[4:6]), minute=int(times[6:8]))

        resources = course.find('resources')

        module_element = resources.find('module')
        staff_element = resources.find('staff')
        room_element = resources.find('room')

        if module_element is not None:
            module = module_element.find('item').text
        if staff_element is not None:
            staff = staff_element.find('item').text
        if room_element is not None:
            room = room_element.find('item').text

        courses.append(Course(start_date, end_date, module, staff, room))

    return TimeTable(list(weeks.items()), courses)


def get_remote_timetable(group_id: int) -> Optional[TimeTable]:
    response = requests.get(f'http://chronos.iut-velizy.uvsq.fr/EDT/g{group_id}.xml')

    if response.status_code != 200:
        return None

    return convert_xml_to_timetable(response.text)


def get_local_timetable(group_id: int) -> Optional[TimeTable]:
    local_file = pathlib.Path(f'storage/g{group_id}.xml')

    if not local_file.exists():
        return None

    xml_timetable = local_file.read_text('utf-8')

    return convert_xml_to_timetable(xml_timetable)
