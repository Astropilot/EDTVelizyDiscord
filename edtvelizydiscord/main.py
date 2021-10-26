from datetime import date
from typing import Dict, List

from config import Settings
from core.discord import send_diff_to_webhook
from core.timetable import (
    compare_two_timetables,
    get_local_timetable,
    get_remote_timetable,
    save_as_local_timetable,
)
from logger import get_logger
from models.diff import CourseDiff

logger = get_logger(__name__)


def worder_update(group_id: int, webhook_url: str, settings: Settings) -> None:
    edt_current, xml_timetable = get_remote_timetable(group_id, settings)
    edt_old = get_local_timetable(group_id, settings)

    if edt_old is None and edt_current is not None and xml_timetable is not None:
        save_as_local_timetable(group_id, xml_timetable, settings)
        return

    if edt_old is None or edt_current is None or xml_timetable is None:
        return

    courses_diff: Dict[date, List[CourseDiff]] = compare_two_timetables(
        edt_old, edt_current
    )

    if len(courses_diff) == 0:
        return

    send_diff_to_webhook(
        edt_current.group_name, group_id, webhook_url, courses_diff, settings
    )

    save_as_local_timetable(group_id, xml_timetable, settings)


settings = Settings()

worder_update(
    178207,
    "",
    settings,
)
