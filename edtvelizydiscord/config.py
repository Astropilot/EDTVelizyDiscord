import logging
import re
from typing import List

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    edt_endpoint: str = "http://chronos.iut-velizy.uvsq.fr/EDT/"
    storage_folder: str = "storage/"
    check_delay: float = 900
    color_embed: int = 12866584
    icon_url_embed: str = "https://i.epvpimg.com/iqfidab.png"
    timeout: int = 30

    log_level: int = logging.DEBUG

    groups: List[str] = []

    @validator("groups")
    def groups_validator(cls, groups: List[str]) -> List[str]:
        for group in groups:
            parts = group.split(":", 1)

            assert (
                len(parts) == 2
            ), "A group must be in the following format: GROUP_ID:WEBHOOK_URL"
            assert parts[0].isdecimal(), "The group id must be a number"
            assert re.match(
                r"https://discord\.com/api/webhooks/\d+/.+",
                parts[1],
            ), "The webhook url must be a valid discord webhook url"

        return groups
