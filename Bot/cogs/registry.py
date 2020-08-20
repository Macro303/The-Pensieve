#!/usr/bin/env python3
import logging
from typing import List, Union

from discord import Embed
from discord.ext import commands
from pony.orm import db_session

from Bot import load_colour
from Database.database import Exploration, Challenge, Mystery, Event, Threat

LOGGER = logging.getLogger(__name__)


def family_embed(items: List[Union[Exploration, Challenge, Mystery, Event]], author_name: str,
                 author_icon_url: str) -> Embed:
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


def page_embed(items: List[Union[Exploration, Challenge, Mystery, Event]], author_name: str,
               author_icon_url: str) -> Embed:
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


def foundable_embed(foundable: Union[Exploration, Challenge, Mystery, Event], author_name: str,
                    author_icon_url: str) -> Embed:
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
        embed.add_field(name='Fragments', value='/'.join(
            [str(x) for x in foundable.threat.fragments]) if foundable.threat else '~~Classified~~')
    elif isinstance(foundable, Challenge):
        embed.add_field(name='Threat', value=Threat.FORTRESS.get_name())
        embed.add_field(name='Fragments', value='/'.join([str(x) for x in Threat.FORTRESS.fragments]))
        embed.add_field(name='Chambers', value=', '.join(
            [x.name for x in foundable.chambers]) if foundable.chambers else '~~Classified~~')
    elif isinstance(foundable, Mystery):
        embed.add_field(name='Fragments', value=foundable.fragments)
    elif isinstance(foundable, Event):
        embed.add_field(name='Threat', value=foundable.threat.get_name() if foundable.threat else '~~Classified~~')
        embed.add_field(name='Method', value=foundable.method.get_name() if foundable.method else '~~Classified~~')
        embed.add_field(name='Fragments', value=foundable.method.fragments if foundable.method else '/'.join(
            [str(i) for i in foundable.threat.fragments]) if foundable.threat else '~~Classified~~')

    image_name = '/'.join(
        [x.replace('\'/:,!', '') for x in [foundable.family, foundable.page, foundable.name]]).replace(' ', '-').lower()
    url = f"https://raw.githubusercontent.com/Macro303/The-Pensieve/main/Resources/Images/{image_name}.png"
    LOGGER.debug(f"Image URL: {url}")
    embed.set_thumbnail(url=url)

    embed.set_footer(
        text=f"Requested by {author_name} | Icons found at https://github.com/Macro303/The-Pensieve",
        icon_url=author_icon_url
    )
    return embed


class RegistryCog(commands.Cog, name='Registry'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='Family',
        description='Returns all the Pages and Foundables in the searched Family/s.',
        usage='[Name of Family]'
    )
    async def family_search(self, ctx, *family_name: str):
        name = ' '.join(family_name)
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
                    await ctx.send(embed=family_embed(
                        items=family,
                        author_name=ctx.author.name,
                        author_icon_url=ctx.author.avatar_url
                    ))
                await ctx.message.delete()
            else:
                LOGGER.warning(f"Unable to find the `{name}` family in the Registry")
                await ctx.send(f"Unable to find the `{name}` family in the Registry")

    @commands.command(
        name='Page',
        description='Returns all the Foundables in the searched Page/s.',
        usage='[Name of Page]'
    )
    async def page_search(self, ctx, *page_name: str):
        name = ' '.join(page_name)
        LOGGER.info(f"Looking for Page: {name}")
        registries = [Exploration, Challenge, Mystery, Event]
        with db_session:
            found = []
            for registry in registries:
                found.extend(registry.select(lambda x: name.lower() == x.page.lower())
                             .order_by(registry.family, registry.page, registry.name)[:])
            if not found:
                for registry in registries:
                    found.extend(registry.select(lambda x: name.lower() in x.page.lower())
                                 .order_by(registry.family, registry.page, registry.name)[:])
            if not found:
                for registry in registries:
                    found.extend(registry.select(lambda x: x.page.lower() in name.lower())
                                 .order_by(registry.family, registry.page, registry.name)[:])
            if found:
                items = {}
                for item in found:
                    if item.family not in items:
                        items[item.family] = []
                    items[item.family].append(item)
                for key, page in items.items():
                    await ctx.send(embed=page_embed(
                        items=page,
                        author_name=ctx.author.name,
                        author_icon_url=ctx.author.avatar_url
                    ))
                await ctx.message.delete()
            else:
                LOGGER.warning(f"Unable to find the `{name}` Page in the Registry")
                await ctx.send(f"Unable to find the `{name}` Page in the Registry")

    @commands.command(
        name='Foundable',
        description='Returns details for the searched Foundable/s.',
        usage='[Name of Foundable]'
    )
    async def foundable_search(self, ctx, *foundable_name: str):
        name = ' '.join(foundable_name)
        LOGGER.info(f"Looking for Foundable: {name}")
        registries = [Exploration, Challenge, Mystery, Event]
        with db_session:
            found = []
            for registry in registries:
                found.extend(registry.select(lambda x: name.lower() == x.name.lower())
                             .order_by(registry.family, registry.page, registry.name)[:])
            if not found:
                for registry in registries:
                    found.extend(registry.select(lambda x: name.lower() in x.name.lower())
                                 .order_by(registry.family, registry.page, registry.name)[:])
            if not found:
                for registry in registries:
                    found.extend(registry.select(lambda x: x.name.lower() in name.lower())
                                 .order_by(registry.family, registry.page, registry.name)[:])
            if found:
                for foundable in found:
                    await ctx.send(embed=foundable_embed(
                        foundable=foundable,
                        author_name=ctx.author.name,
                        author_icon_url=ctx.author.avatar_url
                    ))
                await ctx.message.delete()
            else:
                LOGGER.warning(f"Unable to find the `{name}` Foundable in the Registry")
                await ctx.send(f"Unable to find the `{name}` Foundable in the Registry")


def setup(bot):
    bot.add_cog(RegistryCog(bot))
