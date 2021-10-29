import signal
import sys
from datetime import date
from time import sleep
from types import FrameType
from typing import Dict, List

from config import Settings
from core.discord import send_diff_to_webhook
from core.timer import RepeatTimer
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
    logger.info(f"[Watcher-{group_id}] Started checking...")

    edt_current, xml_timetable = get_remote_timetable(group_id, settings)
    edt_old = get_local_timetable(group_id, settings)

    if edt_old is None and edt_current is not None and xml_timetable is not None:
        logger.warning(f"[Watcher-{group_id}] No local file found for group")
        save_as_local_timetable(group_id, xml_timetable, settings)
        return

    if edt_old is None or edt_current is None or xml_timetable is None:
        logger.warning(
            f"[Watcher-{group_id}] Unexcepted error: remote or local EDT has not been retrieved"
        )
        return

    courses_diff: Dict[date, List[CourseDiff]] = compare_two_timetables(
        edt_old, edt_current
    )

    if len(courses_diff) == 0:
        logger.info(f"[Watcher-{group_id}] No modification found")
        return

    send_diff_to_webhook(
        edt_current.group_name, group_id, webhook_url, courses_diff, settings
    )

    logger.info(f"[Watcher-{group_id}] Modifications sended to discord")

    save_as_local_timetable(group_id, xml_timetable, settings)


if __name__ == "__main__":

    settings = Settings()
    timers: List[RepeatTimer] = []

    def close_watchers(signal: signal.Signals, frame: FrameType) -> None:
        logger.info("Closing all watchers...")
        for timer in timers:
            timer.cancel()
        for timer in timers:
            timer.join()
        sys.exit(0)

    if len(settings.groups) == 0:
        logger.error("No groups to watch has been given. Closing...")
        sys.exit(0)

    logger.info(
        f"Setting up {len(settings.groups)} group's watcher(s) for every {settings.check_delay} seconds..."
    )

    for group in settings.groups:
        group_id, group_webhook = group.split(":", 1)

        logger.info(f"\tSetting up group {group_id} watcher...")

        timer = RepeatTimer(
            settings.check_delay,
            worder_update,
            args=(int(group_id), group_webhook, settings),
        )

        timer.start()

        timers.append(timer)

    logger.info(f"All set! {len(settings.groups)} group(s) are being watched!")
    logger.info("Press Enter at any time to stop...")

    signal.signal(signal.SIGINT, close_watchers)

    while True:
        sleep(1)
