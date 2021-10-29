import xml.etree.ElementTree as ElementTree
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests
from config import Settings
from logger import get_logger
from models.diff import CourseDiff, DiffType, ModifiedOnType
from models.timetable import Course, TimeTable

logger = get_logger(__name__)

REQUESTS_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive",
}


def convert_xml_to_timetable(timetable_xml: str) -> Optional[TimeTable]:
    root = ElementTree.fromstring(timetable_xml)

    weeks: Dict[int, datetime] = {}
    courses: List[Course] = []

    week_nodes: List[ElementTree.Element] = root.findall("span")
    course_nodes: List[ElementTree.Element] = root.findall("event")
    options_node = root.find("option")

    if len(week_nodes) == 0 or options_node is None:
        return None

    subheading_node = options_node.find("subheading")

    if subheading_node is None or subheading_node.text is None:
        return None

    group_name: str = subheading_node.text.replace("Emploi du temps Groupe - ", "")

    for week_node in week_nodes:
        week_date_node = week_node.get("date")
        week_rawix_node = week_node.get("rawix")

        if week_date_node is None or week_rawix_node is None:
            return None

        week_date: datetime = datetime.strptime(week_date_node, "%d/%m/%Y")
        week_index: int = int(week_rawix_node)

        weeks[week_index] = week_date

    for course_node in course_nodes:
        rawweeks_element = course_node.find("rawweeks")
        day_element = course_node.find("day")

        if rawweeks_element is None or rawweeks_element.text is None:
            return None
        if day_element is None or day_element.text is None:
            return None

        week_index: int = rawweeks_element.text.index("Y") + 1  # type: ignore [no-redef]
        week_date: Optional[datetime] = weeks.get(week_index)  # type: ignore [no-redef]
        day: int = int(day_element.text)
        times: Optional[str] = course_node.get("timesort")

        if week_date is None or times is None:
            return None

        start_date: datetime = week_date + timedelta(days=day)
        end_date: datetime = week_date + timedelta(days=day)
        module: str = "[Cours sans nom]"
        staff: str = ""
        room: str = ""

        start_date = start_date.replace(hour=int(times[0:2]), minute=int(times[2:4]))
        end_date = end_date.replace(hour=int(times[4:6]), minute=int(times[6:8]))

        resources = course_node.find("resources")

        if resources is None:
            return None

        module_element = resources.find("module")
        staff_element = resources.find("staff")
        room_element = resources.find("room")

        if module_element is not None:
            module_item = module_element.find("item")

            if module_item is not None and module_item.text is not None:
                module = module_item.text

        if staff_element is not None:
            staff_item = staff_element.find("item")

            if staff_item is not None and staff_item.text is not None:
                staff = staff_item.text

        if room_element is not None:
            room_item = room_element.find("item")

            if room_item is not None and room_item.text is not None:
                room = room_item.text

        courses.append(Course(week_date, start_date, end_date, module, staff, room))

    week_list: List[datetime] = list(weeks.values())

    week_list.sort()
    courses.sort(key=lambda x: x.start_date)

    return TimeTable(group_name, week_list, courses)


def get_remote_timetable(
    group_id: int, settings: Settings
) -> Tuple[Optional[TimeTable], Optional[str]]:
    try:
        response = requests.get(
            f"{settings.edt_endpoint}g{group_id}.xml",
            headers=REQUESTS_HEADERS,
            timeout=settings.timeout,
        )

        if response.status_code != 200:
            logger.error(
                f"The EDT server responded with an incorrect status code: {response.status_code}"
            )
            return None, None

        response.encoding = "utf-8"

        return convert_xml_to_timetable(response.text), response.text
    except requests.exceptions.ConnectionError:
        logger.exception("The EDT server seems to be unreachable!")
        return None, None
    except requests.exceptions.Timeout:
        logger.exception(
            f"The EDT server did not respond within the {settings.timeout}s!"
        )
        return None, None
    except requests.exceptions.TooManyRedirects:
        logger.exception("The EDT server started too many redirects!")
        return None, None


def get_local_timetable(group_id: int, settings: Settings) -> Optional[TimeTable]:
    local_file = Path(settings.storage_folder, f"g{group_id}.xml")

    if not local_file.exists():
        return None

    xml_timetable = local_file.read_text("utf-8")

    return convert_xml_to_timetable(xml_timetable)


def save_as_local_timetable(
    group_id: int, xml_timetable: str, settings: Settings
) -> None:
    local_file = Path(settings.storage_folder, f"g{group_id}.xml")

    if local_file.exists():
        local_file.unlink()

    local_file.write_text(xml_timetable, encoding="utf-8")


def compare_two_timetables(
    edt_old: TimeTable, edt_current: TimeTable
) -> Dict[date, List[CourseDiff]]:
    courses_diff: Dict[date, List[CourseDiff]] = {}

    # We going to ignore if occur the weeks present in the old EDT but not in the new
    # and same for the ones added in the new EDT but not present in the old
    # or else we going to have a lot of deletion and addition courses that are not relevant
    week_dates_in_common: List[datetime] = []

    for week_old in edt_old.weeks:
        if week_old in edt_current.weeks:
            week_dates_in_common.append(week_old)

    # Checking removed courses (present in the old EDT but not in the new)
    for course_old in edt_old.courses:
        if course_old.week_date not in week_dates_in_common:
            continue

        found = False
        for course_current in edt_current.courses:
            if (
                course_old.start_date == course_current.start_date
                and course_old.end_date == course_current.end_date
            ):
                found = True

        if not found:
            courses_diff.setdefault(course_old.start_date.date(), []).append(
                CourseDiff(DiffType.REMOVED, course_old)
            )

    # Checking added courses (present in the current EDT but not in the old)
    for course_current in edt_current.courses:
        if course_current.week_date not in week_dates_in_common:
            continue

        found = False
        for course_old in edt_old.courses:
            if (
                course_current.start_date == course_old.start_date
                and course_current.end_date == course_old.end_date
            ):
                found = True

        if not found:
            courses_diff.setdefault(course_current.start_date.date(), []).append(
                CourseDiff(DiffType.ADDED, course_current)
            )

    # Checking modified courses (same time but either different module name, staff or room)
    for course_old in edt_old.courses:
        if course_old.week_date not in week_dates_in_common:
            continue

        for course_current in edt_current.courses:
            if (
                course_old.start_date == course_current.start_date
                and course_old.end_date == course_current.end_date
            ):
                modified_on: List[ModifiedOnType] = []

                if course_old.module != course_current.module:
                    modified_on.append(ModifiedOnType.MODULE)
                if course_old.staff != course_current.staff:
                    modified_on.append(ModifiedOnType.STAFF)
                if course_old.room != course_current.room:
                    modified_on.append(ModifiedOnType.ROOM)

                if len(modified_on) > 0:
                    courses_diff.setdefault(course_old.start_date.date(), []).append(
                        CourseDiff(
                            DiffType.UPDATED, course_old, course_current, modified_on
                        )
                    )

    return courses_diff
