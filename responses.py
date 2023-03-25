import random

from discord import Embed

from utils.api import api_call
from utils.film import get_search_result, get_description, get_link


def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == 'hello':
        return 'Hey there!'

    if message == 'roll':
        return str(random.randint(1, 6))

    if p_message == '!help':
        return '`This is a help message that you can modify.`'

    return 'I didn\'t understand what you wrote. Try typing "!help".'


async def get_film_embed(film_keywords="", verbosity=0, film_id="", db=None):
    if film_keywords:
        film = await get_search_result(film_keywords)
        if not film:
            return None
        film_id = film["id"]
    film_details = await api_call(f"film/{film_id}")
    film_stats = await api_call(f"film/{film_id}/statistics")

    title = f"{film_details['name']}"
    if "releaseYear" in film_details:
        title += " (" + str(film_details["releaseYear"]) + ")"

    description = await get_description(film_details, film_stats, verbosity, db)
    embed = Embed(title=title, url=get_link(film_details), description=description)

    if "poster" in film_details:
        embed.set_thumbnail(url=film_details["poster"]["sizes"][-1]["url"])
    if "runTime" in film_details:
        runtime = film_details["runTime"]
        hours = runtime // 60
        minutes = runtime % 60
        if hours > 0:
            embed.set_footer(text=f"\n{hours} hour {minutes} min")
        else:
            embed.set_footer(text=f"{runtime} min")
    return embed


def get_link(film_details):
    for link in film_details["links"]:
        if link["type"] == "letterboxd":
            return link["url"]
    return None
