#!/usr/bin/env python3
import logging
from typing import List

import discord
from discord.ext import commands
from pony.orm import db_session

from Bot import CONFIG, load_colour
from Database.database import Exploration, Challenge, Mystery, Event
from Logger import init_logger

LOGGER = logging.getLogger(__name__)
bot = commands.Bot(command_prefix=commands.when_mentioned_or(CONFIG['Prefix']), case_insensitive=True)


@bot.command(name='Family')
async def family_search(ctx, *family: str):
    search = ' '.join(family)
    LOGGER.info(f"Looking up Family: `{search}`")
    with db_session:
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
                await ctx.send(embed=family_embed(family))
        else:
            LOGGER.warning(f"Unable to find `{search}` in the Exploration Registry")
            await ctx.send(f"Unable to find `{search}` in the Exploration Registry")


def family_embed(foundables: List[Exploration]) -> discord.Embed:
    embed = discord.Embed(title=foundables[0].family.title())

    pages = {}
    for item in foundables:
        if item.page not in pages:
            pages[item.page] = []
        pages[item.page].append(item.name)
    for page, items in pages.items():
        embed.add_field(name=page, value=' - ' + ('\n - '.join(items)))

    image_name = foundables[0].family.replace('\'/:,', '').replace(' ', '-').lower()
    url = f"https://raw.githubusercontent.com/Macro303/The-Pensieve/main/Resources/Images/family/{image_name}.png"
    LOGGER.debug(f"URL: {url}")
    embed.set_thumbnail(url=url)

    embed.set_footer(text='Icons from https://github.com/Macro303/The-Pensieve')
    return embed


@bot.command(name='Page')
async def foundable_list(ctx, *page: str):
    search = ' '.join(page)
    LOGGER.info(f"Looking up Page: `{search}`")
    with db_session:
        found = Exploration.select(lambda x: search.lower() == x.page.lower()) \
                    .order_by(Exploration.family, Exploration.page, Exploration.name)[:]
        if not found:
            found = Exploration.select(lambda x: search.lower() in x.page.lower()) \
                        .order_by(Exploration.family, Exploration.page, Exploration.name)[:]
        if not found:
            found = Exploration.select(lambda x: x.page.lower() in search.lower()) \
                        .order_by(Exploration.family, Exploration.page, Exploration.name)[:]
        if found:
            for item in found:
                await ctx.send(embed=foundable_embed(item))
        else:
            LOGGER.warning(f"Unable to find `{search}` in the Exploration Registry")
            await ctx.send(f"Unable to find `{search}` in the Exploration Registry")


@bot.command(name='Foundable')
async def foundable_search(ctx, *foundable: str):
    search = ' '.join(foundable)
    LOGGER.info(f"Looking up Foundable: `{search}`")
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
                await ctx.send(embed=foundable_embed(item))
        else:
            LOGGER.warning(f"Unable to find `{search}` in the Exploration Registry")
            await ctx.send(f"Unable to find `{search}` in the Exploration Registry")


@db_session
def foundable_embed(foundable: Exploration) -> discord.Embed:
    colour = foundable.threat.get_colour() if foundable.threat else '000000'
    embed = discord.Embed(
        title='Foundable Found',
        colour=load_colour(colour),
        description=f"```{foundable.description}```" if foundable.description else None
    )
    image_name = '/'.join([x.replace('\'/:,', '') for x in [foundable.family, foundable.name]]) \
        .replace(' ', '-').lower()
    url = f"https://raw.githubusercontent.com/Macro303/The-Pensieve/main/Resources/Images/exploration/{image_name}.png"
    embed.set_thumbnail(url=url)
    embed.add_field(name='Family', value=foundable.family)
    embed.add_field(name='Page', value=foundable.page)
    embed.add_field(name='Name', value=foundable.name)
    embed.add_field(name='Threat', value=('' if foundable.threat is Threat.BLANK else foundable.threat.name.title()) if foundable.threat else '~~Classified~~')
    embed.add_field(name='Fragments', value='/'.join(
        [str(i) for i in foundable.threat.get_fragments()]) if foundable.threat else '~~Classified~~')
    embed.add_field(name='Returned To', value=foundable.returned if foundable.returned else '~~Classified~~')
    LOGGER.debug(f"URL: {url}")
    embed.set_footer(text='Icons from https://github.com/Macro303/The-Pensieve')
    return embed


@bot.command(name='Challenge-Page')
async def challenge_page(ctx, *page: str):
    search = ' '.join(page)
    LOGGER.info(f"Looking up Challenge Page: `{search}`")
    with db_session:
        found = Challenge.select(lambda x: search.lower() == x.page.lower()) \
                    .order_by(Challenge.family, Challenge.page, Challenge.name)[:]
        if not found:
            found = Challenge.select(lambda x: search.lower() in x.page.lower()) \
                        .order_by(Challenge.family, Challenge.page, Challenge.name)[:]
        if not found:
            found = Challenge.select(lambda x: x.page.lower() in search.lower()) \
                        .order_by(Challenge.family, Challenge.page, Challenge.name)[:]
        if found:
            for item in found:
                await ctx.send(embed=challenge_embed(item))
        else:
            LOGGER.warning(f"Unable to find `{search}` in the Challenge Registry")
            await ctx.send(f"Unable to find `{search}` in the Challenge Registry")


@bot.command(name='Challenge')
async def challenge_search(ctx, *name: str):
    search = ' '.join(name)
    LOGGER.info(f"Looking up Challenge: `{search}`")
    with db_session:
        found = Challenge.select(lambda x: search.lower() == x.name.lower()) \
                    .order_by(Challenge.family, Challenge.page, Challenge.name)[:]
        if not found:
            found = Challenge.select(lambda x: search.lower() in x.name.lower()) \
                        .order_by(Challenge.family, Challenge.page, Challenge.name)[:]
        if not found:
            found = Challenge.select(lambda x: x.name.lower() in search.lower()) \
                        .order_by(Challenge.family, Challenge.page, Challenge.name)[:]
        if found:
            for item in found:
                await ctx.send(embed=challenge_embed(item))
        else:
            LOGGER.warning(f"Unable to find `{search}` in the Registry")
            await ctx.send(f"Unable to find `{search}` in the Registry")


@db_session
def challenge_embed(foundable: Challenge) -> discord.Embed:
    colour = foundable.threat.get_colour() if foundable.threat else '000000'
    embed = discord.Embed(
        title='Challenge Found',
        colour=load_colour(colour),
        description=f"```{foundable.description}```" if foundable.description else None
    )
    image_name = '/'.join([x.replace('\'/:,', '') for x in [foundable.family, foundable.name]]) \
        .replace(' ', '-').lower()
    url = f"https://raw.githubusercontent.com/Macro303/The-Pensieve/main/Resources/Images/challenge/{image_name}.png"
    embed.set_thumbnail(url=url)
    embed.add_field(name='Family', value=foundable.family)
    embed.add_field(name='Page', value=foundable.page)
    embed.add_field(name='Name', value=foundable.name)
    embed.add_field(name='Threat', value=('' if foundable.threat is Threat.BLANK else foundable.threat.name.title()) if foundable.threat else '~~Classified~~')
    embed.add_field(name='Fragments', value='/'.join(
        [str(i) for i in foundable.threat.get_fragments()]) if foundable.threat else '~~Classified~~')
    embed.add_field(name='Returned To', value=foundable.returned if foundable.returned else '~~Classified~~')
    LOGGER.debug(f"URL: {url}")
    embed.set_footer(text='Icons from https://github.com/Macro303/The-Pensieve')
    return embed


@bot.command(name='Mystery-Family')
async def mystery_family(ctx, *family: str):
    search = ' '.join(family)
    LOGGER.info(f"Looking up Mystery Family: `{search}`")
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
                await ctx.send(embed=mystery_family_embed(family))
        else:
            LOGGER.warning(f"Unable to find `{search}` in the Mystery Registry")
            await ctx.send(f"Unable to find `{search}` in the Mystery Registry")


@db_session
def mystery_family_embed(foundables: List[Mystery]) -> discord.Embed:
    embed = discord.Embed(title=foundables[0].family.title())

    pages = {}
    for item in foundables:
        if item.page not in pages:
            pages[item.page] = []
        pages[item.page].append(item.name)
    for page, items in pages.items():
        embed.add_field(name=page, value=' - ' + ('\n - '.join(items)))

    # image_name = foundables[0].family.replace('\'/:,', '').replace(' ', '-').lower()
    # url = f"https://raw.githubusercontent.com/Macro303/The-Pensieve/main/Resources/Images/family/{image_name}.png"
    # LOGGER.debug(f"URL: {url}")
    # embed.set_thumbnail(url=url)

    # embed.set_footer(text='Icons from https://github.com/Macro303/The-Pensieve')
    return embed


@bot.command(name='Mystery-Page')
async def mystery_page(ctx, *page: str):
    search = ' '.join(page)
    LOGGER.info(f"Looking up Mystery Page: `{search}`")
    with db_session:
        found = Mystery.select(lambda x: search.lower() == x.page.lower()) \
                    .order_by(Mystery.family, Mystery.page, Mystery.name)[:]
        if not found:
            found = Mystery.select(lambda x: search.lower() in x.page.lower()) \
                        .order_by(Mystery.family, Mystery.page, Mystery.name)[:]
        if not found:
            found = Mystery.select(lambda x: x.page.lower() in search.lower()) \
                        .order_by(Mystery.family, Mystery.page, Mystery.name)[:]
        if found:
            for item in found:
                await ctx.send(embed=mystery_embed(item))
        else:
            LOGGER.warning(f"Unable to find `{search}` in the Mystery Registry")
            await ctx.send(f"Unable to find `{search}` in the Mystery Registry")


@bot.command(name='Mystery')
async def mystery_search(ctx, *name: str):
    search = ' '.join(name)
    LOGGER.info(f"Looking up Mystery: `{search}`")
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
                await ctx.send(embed=mystery_embed(item))
        else:
            LOGGER.warning(f"Unable to find `{search}` in the Mystery Registry")
            await ctx.send(f"Unable to find `{search}` in the Mystery Registry")


@db_session
def mystery_embed(foundable: Mystery) -> discord.Embed:
    colour = foundable.threat.get_colour() if foundable.threat else '000000'
    embed = discord.Embed(
        title='Mystery Found',
        colour=load_colour(colour),
        description=f"```{foundable.description}```" if foundable.description else None
    )
    image_name = '/'.join([x.replace('\'/:,', '') for x in [foundable.family, foundable.name]]) \
        .replace(' ', '-').lower()
    url = f"https://raw.githubusercontent.com/Macro303/The-Pensieve/main/Resources/Images/mystery/{image_name}.png"
    embed.set_thumbnail(url=url)
    embed.add_field(name='Family', value=foundable.family)
    embed.add_field(name='Page', value=foundable.page)
    embed.add_field(name='Name', value=foundable.name)
    embed.add_field(name='Fragments', value=foundable.fragments if foundable.fragments else '~~Classified~~')
    embed.add_field(name='Returned To', value=foundable.returned if foundable.returned else '~~Classified~~')
    LOGGER.debug(f"URL: {url}")
    embed.set_footer(text='Icons from https://github.com/Macro303/The-Pensieve')
    return embed


@bot.command(name='Event')
async def event_family(ctx, *family: str):
    search = ' '.join(family)
    LOGGER.info(f"Looking up Event Family: `{search}`")
    with db_session:
        found = Event.select(lambda x: search.lower() == x.family.lower()) \
                    .order_by(Event.family, Event.page, Event.name)[:]
        if not found:
            found = Event.select(lambda x: search.lower() in x.family.lower()) \
                        .order_by(Event.family, Event.page, Event.name)[:]
        if not found:
            found = Event.select(lambda x: x.family.lower() in search.lower()) \
                        .order_by(Event.family, Event.page, Event.name)[:]
        if found:
            items = {}
            for item in found:
                if item.family not in items:
                    items[item.family] = []
                items[item.family].append(item)
            for key, family in items.items():
                await ctx.send(embed=event_family_embed(family))
        else:
            LOGGER.warning(f"Unable to find `{search}` in the Event Registry")
            await ctx.send(f"Unable to find `{search}` in the Event Registry")


@db_session
def event_family_embed(foundables: List[Event]) -> discord.Embed:
    embed = discord.Embed(title=foundables[0].family.title())

    pages = {}
    for item in foundables:
        if item.page not in pages:
            pages[item.page] = []
        pages[item.page].append(item.name)
    for page, items in pages.items():
        embed.add_field(name=page, value=' - ' + ('\n - '.join(items)))

    # image_name = foundables[0].family.replace('\'/:,', '').replace(' ', '-').lower()
    # url = f"https://raw.githubusercontent.com/Macro303/The-Pensieve/main/Resources/Images/family/{image_name}.png"
    # LOGGER.debug(f"URL: {url}")
    # embed.set_thumbnail(url=url)

    # embed.set_footer(text='Icons from https://github.com/Macro303/The-Pensieve')
    return embed


@bot.command(name='Sub-Event')
async def event_page(ctx, *page: str):
    search = ' '.join(page)
    LOGGER.info(f"Looking up Event Page: `{search}`")
    with db_session:
        found = Event.select(lambda x: search.lower() == x.page.lower()) \
                    .order_by(Event.family, Event.page, Event.name)[:]
        if not found:
            found = Event.select(lambda x: search.lower() in x.page.lower()) \
                        .order_by(Event.family, Event.page, Event.name)[:]
        if not found:
            found = Event.select(lambda x: x.page.lower() in search.lower()) \
                        .order_by(Event.family, Event.page, Event.name)[:]
        if found:
            for item in found:
                await ctx.send(embed=event_embed(item))
        else:
            LOGGER.warning(f"Unable to find `{search}` in the Event Registry")
            await ctx.send(f"Unable to find `{search}` in the Event Registry")


@bot.command(name='Event-Foundable')
async def event_search(ctx, *name: str):
    search = ' '.join(name)
    LOGGER.info(f"Looking up Event: `{search}`")
    with db_session:
        found = Event.select(lambda x: search.lower() == x.name.lower()) \
                    .order_by(Event.family, Event.page, Event.name)[:]
        if not found:
            found = Event.select(lambda x: search.lower() in x.name.lower()) \
                        .order_by(Event.family, Event.page, Event.name)[:]
        if not found:
            found = Event.select(lambda x: x.name.lower() in search.lower()) \
                        .order_by(Event.family, Event.page, Event.name)[:]
        if found:
            for item in found:
                await ctx.send(embed=event_embed(item))
        else:
            LOGGER.warning(f"Unable to find `{search}` in the Event Registry")
            await ctx.send(f"Unable to find `{search}` in the Event Registry")


@db_session
def event_embed(foundable: Event) -> discord.Embed:
    colour = foundable.threat.get_colour() if foundable.threat else foundable.method.get_colour() if foundable.method else '000000'
    embed = discord.Embed(
        title='Event Found',
        colour=load_colour(colour),
        description=f"```{foundable.description}```" if foundable.description else None
    )
    image_name = '/'.join([x.replace('\'/:,', '') for x in [foundable.family, foundable.name]]) \
        .replace(' ', '-').lower()
    url = f"https://raw.githubusercontent.com/Macro303/The-Pensieve/main/Resources/Images/event/{image_name}.png"
    embed.set_thumbnail(url=url)
    embed.add_field(name='Family', value=foundable.family)
    embed.add_field(name='Page', value=foundable.page)
    embed.add_field(name='Name', value=foundable.name)
    embed.add_field(name='Threat', value=('' if foundable.threat is Threat.BLANK else foundable.threat.name.title()) if foundable.threat else '~~Classified~~')
    embed.add_field(name='Method', value=foundable.method.name.title() if foundable.method else '~~Classified~~')
    embed.add_field(name='Fragments', value=foundable.method.get_fragments() if foundable.method else '~~Classified~~')
    embed.add_field(name='Returned To', value=foundable.returned if foundable.returned else '~~Classified~~')
    LOGGER.debug(f"URL: {url}")
    embed.set_footer(text='Icons from https://github.com/Macro303/The-Pensieve')
    return embed


@bot.event
async def on_ready():
    LOGGER.info(f"Logged in as: {bot.user}")
    await bot.change_presence(activity=discord.Game(name='Wizards Unite'))


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)


if __name__ == "__main__":
    init_logger('The-Pensieve_Bot')
    bot.run(CONFIG['Token'])
