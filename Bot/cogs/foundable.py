#!/usr/bin/env python3
import logging
from typing import Any

from discord import Embed
from discord.ext import commands
from pony.orm import db_session

from Bot import load_colour
from Bot.cogs import get_message
from Database.database import Exploration, Challenge, Mystery, Event, Threat

LOGGER = logging.getLogger(__name__)


def cog_embed(foundable: Any, author_name: str, author_icon_url: str) -> Embed:
    embed = Embed(
        title=foundable.name,
        colour=load_colour(foundable.get_colour()),
        description=f"```{foundable.description}```" if foundable.description else None
    )

    embed.add_field(name='Family', value=foundable.family)
    embed.add_field(name='Page', value=foundable.page)
    embed.add_field(name='Returned To', value=foundable.returned if foundable.returned else '~~Classified~~')

    if isinstance(foundable, Exploration):
        embed.add_field(name='Threat', value=foundable.threat.get_name() if foundable.threat else '~~Classified~~')
        embed.add_field(name='Fragments', value='/'.join([str(x) for x in foundable.threat.fragments]) if foundable.threat else '~~Classified~~')
    elif isinstance(foundable, Challenge):
        embed.add_field(name='Threat', value=Threat.FORTRESS.get_name())
        embed.add_field(name='Fragments', value='/'.join([str(x) for x in Threat.FORTRESS.fragments]))
        embed.add_field(name='Chambers', value=', '.join([x.name for x in foundable.chambers]) if foundable.chambers else '~~Classified~~')
    elif isinstance(foundable, Mystery):
        embed.add_field(name='Fragments', value=foundable.fragments)
    elif isinstance(foundable, Event):
        embed.add_field(name='Threat', value=foundable.threat.get_name() if foundable.threat else '~~Classified~~')
        embed.add_field(name='Method', value=foundable.method.get_name() if foundable.method else '~~Classified~~')
        embed.add_field(name='Fragments', value=foundable.method.fragments if foundable.method else '/'.join([str(i) for i in foundable.threat.fragments]) if foundable.threat else '~~Classified~~')

    image_name = '/'.join([x.replace('\'/:,', '') for x in [foundable.family, foundable.page, foundable.name]]).replace(' ', '-').lower()
    url = f"https://raw.githubusercontent.com/Macro303/The-Pensieve/main/Resources/Images/{image_name}.png"
    LOGGER.debug(f"Image URL: {url}")
    embed.set_thumbnail(url=url)

    embed.set_footer(
        text=f"Requested by {author_name} | Icons found at https://github.com/Macro303/The-Pensieve",
        icon_url=author_icon_url
    )
    return embed


class FoundableCog(commands.Cog, name='Registry Foundables'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='Foundable',
        description='Returns an embed with the searched for Foundable/s in the Registry.',
        usage='[Name of Foundable]'
    )
    async def foundable_search(self, ctx):
        search = get_message(ctx)
        LOGGER.info(f"Looking up Foundable: `{search}`")

        if not search:
            LOGGER.warning(f"Unable to find the `{search}` Foundable in the Registry")
            await ctx.send(f"Unable to find the `{search}` Foundable in the Registry")
            return
        if len(search) < 3:
            LOGGER.warning('Your search is too short, must be longer than 3 characters')
            await ctx.send('Your search is too short, must be longer than 3 characters')
            return

        with db_session:
            found = [
                *Exploration.select(lambda x: search.lower() == x.name.lower())
                     .order_by(Exploration.family, Exploration.page, Exploration.name)[:],
                *Challenge.select(lambda x: search.lower() == x.name.lower())
                     .order_by(Challenge.family, Challenge.page, Challenge.name)[:],
                *Mystery.select(lambda x: search.lower() == x.name.lower())
                     .order_by(Mystery.family, Mystery.page, Mystery.name)[:],
                *Event.select(lambda x: search.lower() == x.name.lower())
                     .order_by(Event.family, Event.page, Event.name)[:],
            ]
            if not found:
                found = [
                    *Exploration.select(lambda x: search.lower() in x.name.lower())
                         .order_by(Exploration.family, Exploration.page, Exploration.name)[:],
                    *Challenge.select(lambda x: search.lower() in x.name.lower())
                         .order_by(Challenge.family, Challenge.page, Challenge.name)[:],
                    *Mystery.select(lambda x: search.lower() in x.name.lower())
                         .order_by(Mystery.family, Mystery.page, Mystery.name)[:],
                    *Event.select(lambda x: search.lower() in x.name.lower())
                         .order_by(Event.family, Event.page, Event.name)[:],
                ]
            if not found:
                found = [
                    *Exploration.select(lambda x: x.name.lower() in search.lower())
                         .order_by(Exploration.family, Exploration.page, Exploration.name)[:],
                    *Challenge.select(lambda x: x.name.lower() in search.lower())
                         .order_by(Challenge.family, Challenge.page, Challenge.name)[:],
                    *Mystery.select(lambda x: x.name.lower() in search.lower())
                         .order_by(Mystery.family, Mystery.page, Mystery.name)[:],
                    *Event.select(lambda x: x.name.lower() in search.lower())
                         .order_by(Event.family, Event.page, Event.name)[:],
                ]
            if found:
                for foundable in found:
                    await ctx.send(embed=cog_embed(
                        foundable=foundable,
                        author_name=ctx.message.author.name,
                        author_icon_url=ctx.message.author.avatar_url
                    ))
            else:
                LOGGER.warning(f"Unable to find the `{search}` Foundable in the Registry")
                await ctx.send(f"Unable to find the `{search}` Foundable in the Registry")


def setup(bot):
    bot.add_cog(FoundableCog(bot))
