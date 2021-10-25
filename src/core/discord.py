
import requests
from datetime import date
from typing import Dict, List
from discord_webhook.webhook import DiscordWebhook, DiscordEmbed
from babel.dates import format_date
from config import Settings

from models.diff import CourseDiff, DiffType, ModifiedOnType
from logger import get_logger

logger = get_logger(__name__)

def send_diff_to_webhook(group_name: str, group_id: int, webhook_url: str, courses_diff: Dict[date, List[CourseDiff]], settings: Settings) -> None:
    webhook = DiscordWebhook(url=webhook_url, rate_limit_retry=True, timeout=settings.timeout)
    embed = DiscordEmbed(title=f'Changement de l\'emploi du temps {group_name}')

    embed.set_color(settings.color_embed)
    embed.set_url(f'{settings.edt_endpoint}g{group_id}.html')
    embed.set_timestamp()
    embed.set_footer(text='Changement détecté le')
    embed.set_thumbnail(url=settings.icon_url_embed)
    embed.set_author(
        name='EDTVelizy',
        url='https://github.com/Astropilot/EDTVelizyDiscord',
        icon_url=settings.icon_url_embed
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
            value=f'```diff\n{diff_str}```',
            inline=False
        )

    webhook.add_embed(embed)

    try:
        webhook.execute()
    except requests.exceptions.ConnectionError:
        logger.exception(f'The Discord server seems to be unreachable!')
    except requests.exceptions.Timeout:
        logger.exception(f'The Discord server did not respond within the {settings.timeout}s!')
    except requests.exceptions.TooManyRedirects:
        logger.exception(f'The Discord server started too many redirects!')
