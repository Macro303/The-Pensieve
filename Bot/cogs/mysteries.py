#!/usr/bin/env python3
import logging
from typing import List

from Bot import load_colour
from Bot.cogs import get_message
from Database.database import Mystery
from discord import Embed
from discord.ext import commands
from pony.orm import db_session

LOGGER = logging.getLogger(__name__)


def family_embed(foundables: List[Mystery], author_name: str, author_icon_url: str) -> Embed:
    embed = Embed(title=foundables[0].family)

    pages = {}
    for item in foundables:
        if item.page not in pages:
            pages[item.page] = []
        pages[item.page].append(item.name)
    for page, items in pages.items():
        embed.add_field(name=page, value=' - ' + ('\n - '.join(items)))

    image_name = foundables[0].family.replace('\'/:,', '').replace(' ', '-').lower()
    url = f"https://raw.githubusercontent.com/Macro303/The-Pensieve/main/Resources/Images/mysteries-family/{image_name}.png"
    LOGGER.debug(f"URL: {url}")
    embed.set_thumbnail(url=url)

    embed.set_footer(
        text=f"Requested by {author_name} | Icons from https://github.com/Macro303/The-Pensieve",
        icon_url=author_icon_url
    )
    return embed


def foundable_embed(foundable: Mystery, author_name: str, author_icon_url: str) -> Embed:
    embed = Embed(
        title='Mystery Foundable Found',
        colour=load_colour('000000'),
        description=f"```{foundable.description}```" if foundable.description else None
    )

    embed.add_field(name='Family', value=foundable.family)
    embed.add_field(name='Page', value=foundable.page)
    embed.add_field(name='Name', value=foundable.name)
    embed.add_field(name='Fragments', value=foundable.fragments)
    embed.add_field(name='Returned To', value=foundable.returned if foundable.returned else '~~Classified~~')

    image_name = '/'.join([x.replace('\'/:,', '') for x in [foundable.family, foundable.name]]) \
        .replace(' ', '-').lower()
    url = f"https://raw.githubusercontent.com/Macro303/The-Pensieve/main/Resources/Images/mysteries/{image_name}.png"
    LOGGER.debug(f"URL: {url}")
    embed.set_thumbnail(url=url)

    embed.set_footer(
        text=f"Requested by {author_name} | Icons from https://github.com/Macro303/The-Pensieve",
        icon_url=author_icon_url
    )
    return embed


class MysteriesCog(commands.Cog, name='Mysteries Registry'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='Mystery',
        description='Returns an embed with the pages and foundables in the searched for Mystery/s in the Mysteries Registry.',
        usage='[Name of Mystery]'
    )
    async def family_search(self, ctx):
        search = get_message(ctx)
        LOGGER.info(f"Looking up Family: `{search}`")

        if not search:
            LOGGER.warning(f"Unable to find `{search}` in the Mystery Registry")
            await ctx.send(f"Unable to find `{search}` in the Mystery Registry")
            return
        if len(search) < 3:
            LOGGER.warning('Your search is too short, must be longer than 3 characters')
            await ctx.send('Your search is too short, must be longer than 3 characters')
            return

        with db_session:
            found = Mystery.select(lambda x: search.lower() == x.family.lower()) \
                        .order_by(Mystery.family, Mystery.page, Mystery.name)[:]
            if not found:
                found = Mystery.select(lambda x: search.lower() in x.family.lower()) \
                            .order_by(Mystery.family, Mystery.page, Mystery.name)[:]
            if not found:
                found = Mystery.select(lambda x: x.family.lower() in search.lower()) \
                            .order_by(Mystery.family, Mystery.page, Mystery.name)[:]
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
                LOGGER.warning(f"Unable to find `{search}` in the Mystery Registry")
                await ctx.send(f"Unable to find `{search}` in the Mystery Registry")

    @commands.command(
        name='Mystery-Foundable',
        description='Returns an embed with the details for the searched for Foundable/s in the Mysteries Registry.',
        usage='[Name of Foundable]'
    )
    async def foundable_search(self, ctx):
        search = get_message(ctx)
        LOGGER.info(f"Looking up Foundable: `{search}`")

        if not search:
            LOGGER.warning(f"Unable to find `{search}` in the Mystery Registry")
            await ctx.send(f"Unable to find `{search}` in the Mystery Registry")
            return
        if len(search) < 3:
            LOGGER.warning('Your search is too short, must be longer than 3 characters')
            await ctx.send('Your search is too short, must be longer than 3 characters')
            return

        with db_session:
            found = Mystery.select(lambda x: search.lower() == x.name.lower()) \
                        .order_by(Mystery.family, Mystery.page, Mystery.name)[:]
            if not found:
                found = Mystery.select(lambda x: search.lower() in x.name.lower()) \
                            .order_by(Mystery.family, Mystery.page, Mystery.name)[:]
            if not found:
                found = Mystery.select(lambda x: x.name.lower() in search.lower()) \
                            .order_by(Mystery.family, Mystery.page, Mystery.name)[:]
            if found:
                for item in found:
                    await ctx.send(embed=foundable_embed(
                        foundable=item,
                        author_name=ctx.message.author.name,
                        author_icon_url=ctx.message.author.avatar_url
                    ))
            else:
                LOGGER.warning(f"Unable to find `{search}` in the Mystery Registry")
                await ctx.send(f"Unable to find `{search}` in the Mystery Registry")


def setup(bot):
    bot.add_cog(MysteriesCog(bot))
