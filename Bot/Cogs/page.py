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


class PageCog(commands.Cog, name='Registry Pages'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='Page',
        description='Returns an embed with the foundables in the searched for Page/s in the Registry.',
        usage='[Name of Page]'
    )
    async def page_search(self, ctx, name: str):
        registries = [Exploration, Challenge, Mystery, Event]
        with db_session:
            found = []
            for registry in registries:
                found.extend(*registry.select(lambda x: name.lower() == x.page.lower())
                             .order_by(registry.family, registry.page, registry.name)[:])
            if not found:
                for registry in registries:
                    found.extend(*registry.select(lambda x: name.lower() in x.page.lower())
                                 .order_by(registry.family, registry.page, registry.name)[:])
            if not found:
                for registry in registries:
                    found.extend(*registry.select(lambda x: x.page.lower() in name.lower())
                                 .order_by(registry.family, registry.page, registry.name)[:])
            if found:
                items = {}
                for item in found:
                    if item.family not in items:
                        items[item.family] = []
                    items[item.family].append(item)
                for key, page in items.items():
                    await ctx.send(embed=cog_embed(
                        items=page,
                        author_name=ctx.author.name,
                        author_icon_url=ctx.author.avatar_url
                    ))
            else:
                LOGGER.warning(f"Unable to find the `{name}` Page in the Registry")
                await ctx.send(f"Unable to find the `{name}` Page in the Registry")


def setup(bot):
    bot.add_cog(PageCog(bot))
