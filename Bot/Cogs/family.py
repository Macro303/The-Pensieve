#!/usr/bin/env python3
import logging
from typing import List, Any

from discord import Embed
from discord.ext import commands
from pony.orm import db_session

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
    async def family_search(self, ctx, name: str):
        LOGGER.info(f"Looking for Family: {name}")
        registries = [Exploration, Challenge, Mystery, Event]
        with db_session:
            found = []
            for registry in registries:
                found.extend(registry.select(lambda x: name.lower() == x.family.lower())
                             .order_by(registry.family, registry.page, registry.name)[:])
            if not found:
                for registry in registries:
                    found.extend(registry.select(lambda x: name.lower() in x.family.lower())
                                 .order_by(registry.family, registry.page, registry.name)[:])
            if not found:
                for registry in registries:
                    found.extend(registry.select(lambda x: x.family.lower() in name.lower())
                                 .order_by(registry.family, registry.page, registry.name)[:])
            if found:
                items = {}
                for item in found:
                    if item.family not in items:
                        items[item.family] = []
                    items[item.family].append(item)
                for key, family in items.items():
                    await ctx.send(embed=cog_embed(
                        items=family,
                        author_name=ctx.author.name,
                        author_icon_url=ctx.author.avatar_url
                    ))
                await ctx.message.delete()
            else:
                LOGGER.warning(f"Unable to find the `{name}` family in the Registry")
                await ctx.send(f"Unable to find the `{name}` family in the Registry")


def setup(bot):
    bot.add_cog(FamilyCog(bot))
