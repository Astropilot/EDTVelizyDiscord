from datetime import datetime
from pathlib import Path
from typing import Optional

from core.timetable import convert_xml_to_timetable
from models.timetable import TimeTable


def test_valid_xml_timetable() -> None:
    file = Path(__file__).parent / Path("data", "edt_1_valid.xml")

    edt_xml = file.read_text("utf-8")

    timetable: Optional[TimeTable] = convert_xml_to_timetable(edt_xml)

    assert timetable is not None

    assert timetable.group_name == "INF1-A1"

    assert len(timetable.weeks) == 2

    assert timetable.weeks[0] == datetime(2021, 10, 18, 0, 0, 0)
    assert timetable.weeks[1] == datetime(2021, 10, 25, 0, 0, 0)

    assert len(timetable.courses) == 3

    print(timetable.courses[0])

    assert timetable.courses[0].week_date == datetime(2021, 10, 18, 0, 0, 0)
    assert timetable.courses[0].start_date == datetime(2021, 10, 18, 8, 0, 0)
    assert timetable.courses[0].end_date == datetime(2021, 10, 18, 10, 30, 0)
    assert timetable.courses[0].module == "Dev. interfaces web"
    assert timetable.courses[0].staff == "Jean Dupont"
    assert timetable.courses[0].room == ""

    assert timetable.courses[1].week_date == datetime(2021, 10, 25, 0, 0, 0)
    assert timetable.courses[1].start_date == datetime(2021, 10, 26, 9, 0, 0)
    assert timetable.courses[1].end_date == datetime(2021, 10, 26, 10, 30, 0)
    assert timetable.courses[1].module == "Création BD"
    assert timetable.courses[1].staff == ""
    assert timetable.courses[1].room == "G22"

    assert timetable.courses[2].week_date == datetime(2021, 10, 25, 0, 0, 0)
    assert timetable.courses[2].start_date == datetime(2021, 10, 27, 16, 15, 0)
    assert timetable.courses[2].end_date == datetime(2021, 10, 27, 17, 30, 0)
    assert timetable.courses[2].module == "[Cours sans nom]"
    assert timetable.courses[2].staff == ""
    assert timetable.courses[2].room == ""
