#!/usr/bin/env python3
import logging
from typing import List, Any

from discord import Embed
from discord.ext import commands
from pony.orm import db_session

from Bot.cogs import get_message
from Database.database import Exploration, Challenge, Mystery, Event

LOGGER = logging.getLogger(__name__)


def cog_embed(items: List[Any], author_name: str, author_icon_url: str) -> Embed:
    embed = Embed(title=items[0].family)

    pages = {}
    for item in items:
        if item.page not in pages:
            pages[item.page] = []
        pages[item.page].append(item.name)
    for page, items in pages.items():
        embed.add_field(name=page, value=' - ' + ('\n - '.join(items)))

    embed.set_footer(
        text=f"Requested by {author_name} | Icons from https://github.com/Macro303/The-Pensieve",
        icon_url=author_icon_url
    )
    return embed


class FamilyCog(commands.Cog, name='Registry Families'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='Family',
        description='Returns an embed with the pages and foundables in the searched for Family/s in the Registry.',
        usage='[Name of Family]'
    )
    async def family_search(self, ctx):
        search = get_message(ctx)
        LOGGER.info(f"Looking up Family: `{search}`")

        if not search:
            LOGGER.warning(f"Unable to find the `{search}` family in the Registry")
            await ctx.send(f"Unable to find the `{search}` family in the Registry")
            return
        if len(search) < 3:
            LOGGER.warning('Your search is too short, must be longer than 3 characters')
            await ctx.send('Your search is too short, must be longer than 3 characters')
            return

        with db_session:
            found = [
                *Exploration.select(lambda x: search.lower() == x.family.lower())
                    .order_by(Exploration.family, Exploration.page, Exploration.name)[:],
                *Challenge.select(lambda x: search.lower() == x.family.lower())
                    .order_by(Challenge.family, Challenge.page, Challenge.name)[:],
                *Mystery.select(lambda x: search.lower() == x.family.lower())
                    .order_by(Mystery.family, Mystery.page, Mystery.name)[:],
                *Event.select(lambda x: search.lower() == x.family.lower())
                    .order_by(Event.family, Event.page, Event.name)[:],
            ]
            if not found:
                found = [
                    *Exploration.select(lambda x: search.lower() in x.family.lower())
                        .order_by(Exploration.family, Exploration.page, Exploration.name)[:],
                    *Challenge.select(lambda x: search.lower() in x.family.lower())
                        .order_by(Challenge.family, Challenge.page, Challenge.name)[:],
                    *Mystery.select(lambda x: search.lower() in x.family.lower())
                        .order_by(Mystery.family, Mystery.page, Mystery.name)[:],
                    *Event.select(lambda x: search.lower() in x.family.lower())
                        .order_by(Event.family, Event.page, Event.name)[:],
                ]
            if not found:
                found = [
                    *Exploration.select(lambda x: x.family.lower() in search.lower())
                        .order_by(Exploration.family, Exploration.page, Exploration.name)[:],
                    *Challenge.select(lambda x: x.family.lower() in search.lower())
                        .order_by(Challenge.family, Challenge.page, Challenge.name)[:],
                    *Mystery.select(lambda x: x.family.lower() in search.lower())
                        .order_by(Mystery.family, Mystery.page, Mystery.name)[:],
                    *Event.select(lambda x: x.family.lower() in search.lower())
                        .order_by(Event.family, Event.page, Event.name)[:],
                ]
            if found:
                items = {}
                for item in found:
                    if item.family not in items:
                        items[item.family] = []
                    items[item.family].append(item)
                for key, family in items.items():
                    await ctx.send(embed=cog_embed(
                        items=family,
                        author_name=ctx.message.author.name,
                        author_icon_url=ctx.message.author.avatar_url
                    ))
            else:
                LOGGER.warning(f"Unable to find the `{search}` family in the Registry")
                await ctx.send(f"Unable to find the `{search}` family in the Registry")


def setup(bot):
    bot.add_cog(FamilyCog(bot))
