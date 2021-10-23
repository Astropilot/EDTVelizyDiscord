from typing import List
from pydantic import BaseSettings


class Settings(BaseSettings):
    groups_id: List[int] = []
    groups_name: List[str] = []
