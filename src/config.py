from typing import List
from pydantic import BaseSettings


class Settings(BaseSettings):
    edt_endpoint: str = 'http://chronos.iut-velizy.uvsq.fr/EDT/'
    storage_folder: str = 'storage/'
    check_delay: int = 900
    color_embed: str = '12866584'
    icon_url_embed: str = 'https://i.epvpimg.com/iqfidab.png'

    bug_report: bool = False
    webhook_report: str = ''

    groups_id: List[int] = []
