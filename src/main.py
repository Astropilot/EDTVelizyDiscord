from datetime import date
from typing import Dict, List
from discord_webhook import DiscordWebhook, DiscordEmbed
from babel.dates import format_date

from core.timetable import (
    get_local_timetable,
    get_remote_timetable,
    save_as_local_timetable,
    compare_two_timetables
)
from models.diff import CourseDiff, DiffType, ModifiedOnType


def worder_update(group_id: int, webhook_url: str) -> None:
    edt_current, xml_timetable = get_remote_timetable(group_id)
    edt_old = get_local_timetable(group_id)

    if edt_old is None and edt_current is not None:
        save_as_local_timetable(group_id, xml_timetable)
        return

    if edt_current is None:
        return

    courses_diff: Dict[date, List[CourseDiff]] = compare_two_timetables(edt_old, edt_current)

    print(courses_diff)

    if len(courses_diff) == 0:
        return

    webhook = DiscordWebhook(url=webhook_url, rate_limit_retry=True)
    embed = DiscordEmbed(title=f'Changement de l\'emploi du temps {edt_current.group_name}', color='12866584')

    embed.set_url(f'http://chronos.iut-velizy.uvsq.fr/EDT/g{group_id}.html')
    embed.set_timestamp()
    embed.set_footer(text='Changement détecté le')
    embed.set_thumbnail(url='https://i.epvpimg.com/iqfidab.png')
    embed.set_author(
        name='EDTVelizy',
        url='https://github.com/Astropilot/EDTVelizyDiscord',
        icon_url='https://i.epvpimg.com/iqfidab.png'
    )

    for course_diff_date in sorted(courses_diff):
        courses_diff_list = courses_diff[course_diff_date]
        diff_str = ''

        for course_diff in courses_diff_list:

            if course_diff.type == DiffType.ADDED:
                diff_str += f'+ {course_diff.course.module} ({course_diff.course.pretty_times})\n'
            elif course_diff.type == DiffType.REMOVED:
                diff_str += f'- {course_diff.course.module} ({course_diff.course.pretty_times})\n'
            elif course_diff.type == DiffType.UPDATED:
                diff_str += f'! {course_diff.course.module} ({course_diff.course.pretty_times}):\n'

                if ModifiedOnType.MODULE in course_diff.modified_on:
                    diff_str += f'\tChangement du module: "{course_diff.course.module}" -> "{course_diff.compare_to.module}"\n'
                if ModifiedOnType.STAFF in course_diff.modified_on:
                    diff_str += f'\tChangement du professeur: "{course_diff.course.staff}" -> "{course_diff.compare_to.staff}"\n'
                if ModifiedOnType.ROOM in course_diff.modified_on:
                    diff_str += f'\tChangement de la salle: "{course_diff.course.room}" -> "{course_diff.compare_to.room}"\n'

        embed.add_embed_field(
            name=format_date(course_diff_date, 'EEEE dd MMMM yyyy', locale='fr'),
            value=f'```diff\n{diff_str}```'
        )

    print(embed.__dict__)

    webhook.add_embed(embed)
    webhook.execute()

    # save_as_local_timetable(group_id, xml_timetable)


worder_update(178207, '')
