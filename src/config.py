from typing import List
from pydantic import BaseSettings
import logging


class Settings(BaseSettings):
    edt_endpoint: str = "http://chronos.iut-velizy.uvsq.fr/EDT/"
    storage_folder: str = "storage/"
    check_delay: int = 900
    color_embed: int = 12866584
    icon_url_embed: str = "https://i.epvpimg.com/iqfidab.png"
    timeout: int = 30

    log_level: int = logging.DEBUG

    groups_id: List[int] = []
