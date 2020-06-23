#!/usr/bin/env python3
import logging
from typing import List

from discord import Embed
from discord.ext import commands
from pony.orm import db_session

from Bot import load_colour
from Bot.cogs import get_message
from Database.database import Exploration

LOGGER = logging.getLogger(__name__)


def family_embed(foundables: List[Exploration], author_name: str, author_icon_url: str) -> Embed:
    embed = Embed(title=foundables[0].family.title())

    pages = {}
    for item in foundables:
        if item.page not in pages:
            pages[item.page] = []
        pages[item.page].append(item.name)
    for page, items in pages.items():
        embed.add_field(name=page, value=' - ' + ('\n - '.join(items)))

    image_name = foundables[0].family.replace('\'/:,', '').replace(' ', '-').lower()
    url = f"https://raw.githubusercontent.com/Macro303/The-Pensieve/main/Resources/Images/exploration-family/{image_name}.png"
    LOGGER.debug(f"URL: {url}")
    embed.set_thumbnail(url=url)

    embed.set_author(name=author_name, icon_url=author_icon_url)
    embed.set_footer(text='Icons from https://github.com/Macro303/The-Pensieve')
    return embed


def foundable_embed(foundable: Exploration, author_name: str, author_icon_url: str) -> Embed:
    colour = foundable.threat.get_colour() if foundable.threat else '000000'
    embed = Embed(
        title='Exploration Foundable Found',
        colour=load_colour(colour),
        description=f"```{foundable.description}```" if foundable.description else None
    )

    embed.add_field(name='Family', value=foundable.family)
    embed.add_field(name='Page', value=foundable.page)
    embed.add_field(name='Name', value=foundable.name)
    embed.add_field(name='Threat', value=foundable.threat.get_name() if foundable.threat else '~~Classified~~')
    embed.add_field(name='Fragments', value='/'.join(
        [str(i) for i in foundable.threat.get_fragments()]) if foundable.threat else '~~Classified~~')
    embed.add_field(name='Returned To', value=foundable.returned if foundable.returned else '~~Classified~~')

    image_name = '/'.join([x.replace('\'/:,', '') for x in [foundable.family, foundable.name]]) \
        .replace(' ', '-').lower()
    url = f"https://raw.githubusercontent.com/Macro303/The-Pensieve/main/Resources/Images/exploration/{image_name}.png"
    LOGGER.debug(f"URL: {url}")
    embed.set_thumbnail(url=url)

    embed.set_author(name=author_name, icon_url=author_icon_url)
    embed.set_footer(text='Icons from https://github.com/Macro303/The-Pensieve')
    return embed


class ExplorationCog(commands.Cog, name='Exploration Registry'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='Family',
        description='Returns an embed with the pages and foundables in the searched for Family/s in the Exploration Registry.',
        usage='["all" or Name of Family]'
    )
    async def family_search(self, ctx):
        search = get_message(ctx)
        LOGGER.info(f"Looking up Family: `{search}`")

        if not search:
            LOGGER.warning(f"Unable to find `{search}` in the Exploration Registry")
            await ctx.send(f"Unable to find `{search}` in the Exploration Registry")
            return

        with db_session:
            if search.lower() == 'all':
                found = Exploration.select() \
                            .order_by(Exploration.family, Exploration.page, Exploration.name)[:]
            else:
                found = Exploration.select(lambda x: search.lower() == x.family.lower()) \
                            .order_by(Exploration.family, Exploration.page, Exploration.name)[:]
                if not found:
                    found = Exploration.select(lambda x: search.lower() in x.family.lower()) \
                                .order_by(Exploration.family, Exploration.page, Exploration.name)[:]
                if not found:
                    found = Exploration.select(lambda x: x.family.lower() in search.lower()) \
                                .order_by(Exploration.family, Exploration.page, Exploration.name)[:]
            if found:
                items = {}
                for item in found:
                    if item.family not in items:
                        items[item.family] = []
                    items[item.family].append(item)
                for key, family in items.items():
                    await ctx.send(embed=family_embed(
                        foundables=family,
                        author_name=ctx.message.author.name,
                        author_icon_url=ctx.message.author.avatar_url
                    ))
            else:
                LOGGER.warning(f"Unable to find `{search}` in the Exploration Registry")
                await ctx.send(f"Unable to find `{search}` in the Exploration Registry")

    @commands.command(
        name='Foundable',
        description='Returns an embed with the details for the searched for Foundable/s in the Exploration Registry.',
        usage='[Name of Foundable]'
    )
    async def foundable_search(self, ctx):
        search = get_message(ctx)
        LOGGER.info(f"Looking up Foundable: `{search}`")

        if not search:
            LOGGER.warning(f"Unable to find `{search}` in the Exploration Registry")
            await ctx.send(f"Unable to find `{search}` in the Exploration Registry")
            return

        with db_session:
            found = Exploration.select(lambda x: search.lower() == x.name.lower()) \
                        .order_by(Exploration.family, Exploration.page, Exploration.name)[:]
            if not found:
                found = Exploration.select(lambda x: search.lower() in x.name.lower()) \
                            .order_by(Exploration.family, Exploration.page, Exploration.name)[:]
            if not found:
                found = Exploration.select(lambda x: x.name.lower() in search.lower()) \
                            .order_by(Exploration.family, Exploration.page, Exploration.name)[:]
            if found:
                for item in found:
                    await ctx.send(embed=foundable_embed(
                        foundable=item,
                        author_name=ctx.message.author.name,
                        author_icon_url=ctx.message.author.avatar_url
                    ))
            else:
                LOGGER.warning(f"Unable to find `{search}` in the Exploration Registry")
                await ctx.send(f"Unable to find `{search}` in the Exploration Registry")


def setup(bot):
    bot.add_cog(ExplorationCog(bot))
