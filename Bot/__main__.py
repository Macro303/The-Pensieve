#!/usr/bin/env python3
import logging

import discord
from Bot import CONFIG, load_colour
from Database.database import Exploration, Challenge, Mystery, Event
from Logger import init_logger
from discord.ext import commands
from pony.orm import db_session

LOGGER = logging.getLogger(__name__)
bot = commands.Bot(command_prefix=commands.when_mentioned_or(CONFIG['Prefix']), case_insensitive=True)


@bot.command(name='Family')
async def registry_family(ctx, *family: str):
    search = ' '.join(family)
    LOGGER.info(f"Looking up Family: `{search}`")
    with db_session:
        found = [
            *Exploration.select(lambda x: x.family.lower() == search.lower())
                 .order_by(Exploration.family, Exploration.page, Exploration.name)[:],
            *Challenge.select(lambda c: c.family.lower() == search.lower())
                 .order_by(Challenge.family, Challenge.page, Challenge.name)[:],
            *Mystery.select(lambda m: m.family.lower() == search.lower())
                 .order_by(Mystery.family, Mystery.page, Mystery.name)[:],
            *Event.select(lambda e: e.family.lower() == search.lower())
                 .order_by(Event.family, Event.page, Event.name)[:]
        ]
        if found:
            for item in found:
                LOGGER.debug(f"Family: {item}")
                if isinstance(item, Exploration):
                    await ctx.send(embed=exploration_embed(item))
                elif isinstance(item, Challenge):
                    await ctx.send(embed=challenge_embed(item))
                elif isinstance(item, Mystery):
                    await ctx.send(embed=mystery_embed(item))
                elif isinstance(item, Event):
                    await ctx.send(embed=event_embed(item))
                else:
                    LOGGER.error(f"Found: {item}, Unable to map it")
        else:
            LOGGER.warning(f"Unable to find `{search}` in the Registry")
            await ctx.send(f"Unable to find `{search}` in the Registry")


@bot.command(name='Page')
async def registry_page(ctx, *page: str):
    search = ' '.join(page)
    LOGGER.info(f"Looking up Page: `{search}`")
    with db_session:
        found = [
            *Exploration.select(lambda x: x.page.lower() == search.lower())
                 .order_by(Exploration.family, Exploration.page, Exploration.name)[:],
            *Challenge.select(lambda c: c.page.lower() == search.lower())
                 .order_by(Challenge.family, Challenge.page, Challenge.name)[:],
            *Mystery.select(lambda m: m.page.lower() == search.lower())
                 .order_by(Mystery.family, Mystery.page, Mystery.name)[:],
            *Event.select(lambda e: e.page.lower() == search.lower())
                 .order_by(Event.family, Event.page, Event.name)[:]
        ]
        if found:
            for item in found:
                LOGGER.debug(f"Page: {item}")
                if isinstance(item, Exploration):
                    await ctx.send(embed=exploration_embed(item))
                elif isinstance(item, Challenge):
                    await ctx.send(embed=challenge_embed(item))
                elif isinstance(item, Mystery):
                    await ctx.send(embed=mystery_embed(item))
                elif isinstance(item, Event):
                    await ctx.send(embed=event_embed(item))
                else:
                    LOGGER.error(f"Found: {item}, Unable to map it")
        else:
            LOGGER.warning(f"Unable to find `{search}` in the Registry")
            await ctx.send(f"Unable to find `{search}` in the Registry")


@bot.command(name='Foundable')
async def registry_foundable(ctx, *name: str):
    search = ' '.join(name)
    LOGGER.info(f"Looking up Foundable: `{search}`")
    with db_session:
        found = [
            *Exploration.select(lambda x: x.name.lower() == search.lower())
                 .order_by(Exploration.family, Exploration.page, Exploration.name)[:],
            *Challenge.select(lambda c: c.name.lower() == search.lower())
                 .order_by(Challenge.family, Challenge.page, Challenge.name)[:],
            *Mystery.select(lambda m: m.name.lower() == search.lower())
                 .order_by(Mystery.family, Mystery.page, Mystery.name)[:],
            *Event.select(lambda e: e.name.lower() == search.lower())
                 .order_by(Event.family, Event.page, Event.name)[:]
        ]
        if found:
            for item in found:
                LOGGER.debug(f"Foundable: {item}")
                if isinstance(item, Exploration):
                    await ctx.send(embed=exploration_embed(item))
                elif isinstance(item, Challenge):
                    await ctx.send(embed=challenge_embed(item))
                elif isinstance(item, Mystery):
                    await ctx.send(embed=mystery_embed(item))
                elif isinstance(item, Event):
                    await ctx.send(embed=event_embed(item))
                else:
                    LOGGER.error(f"Found: {item}, Unable to map it")
        else:
            LOGGER.warning(f"Unable to find `{search}` in the Registry")
            await ctx.send(f"Unable to find `{search}` in the Registry")


@db_session
def exploration_embed(foundable: Exploration) -> discord.Embed:
    embed = discord.Embed(title='Foundable Found',
                          colour=load_colour(foundable.threat.get_colour() if foundable.threat else '000000'))
    image_name = (foundable.family + '/' + foundable.name.replace('\'', '')).replace(' ', '-').lower()
    url = f"https://raw.githubusercontent.com/Macro303/The-Pensieve/main/Resources/Images/exploration/{image_name}.png"
    embed.set_thumbnail(url=url)
    embed.add_field(name='Family', value=foundable.family)
    embed.add_field(name='Page', value=foundable.page)
    embed.add_field(name='Name', value=foundable.name)
    embed.add_field(name='Threat', value=foundable.threat.name.title() if foundable.threat else 'Missing')
    embed.add_field(name='Fragments', value='/'.join(
        [str(i) for i in foundable.threat.get_fragments()]) if foundable.threat else 'Missing')
    LOGGER.debug(f"URL: {url}")
    embed.set_footer(text='Icons from https://github.com/Macro303/The-Pensieve')
    return embed


@db_session
def challenge_embed(foundable: Challenge) -> discord.Embed:
    embed = discord.Embed(title='Challenge Found',
                          colour=load_colour(foundable.threat.get_colour() if foundable.threat else '000000'))
    image_name = (foundable.family + '/' + foundable.name.replace('\'', '')).replace(' ', '-').lower()
    url = f"https://raw.githubusercontent.com/Macro303/The-Pensieve/main/Resources/Images/challenge/{image_name}.png"
    embed.set_thumbnail(url=url)
    embed.add_field(name='Family', value=foundable.family)
    embed.add_field(name='Page', value=foundable.page)
    embed.add_field(name='Name', value=foundable.name)
    embed.add_field(name='Threat', value=foundable.threat.name.title() if foundable.threat else 'Missing')
    embed.add_field(name='Fragments', value='/'.join(
        [str(i) for i in foundable.threat.get_fragments()]) if foundable.threat else 'Missing')
    LOGGER.debug(f"URL: {url}")
    embed.set_footer(text='Icons from https://github.com/Macro303/The-Pensieve')
    return embed


@db_session
def mystery_embed(foundable: Mystery) -> discord.Embed:
    embed = discord.Embed(title='Mystery Found')
    image_name = (foundable.family + '/' + foundable.name.replace('\'', '')).replace(' ', '-').lower()
    url = f"https://raw.githubusercontent.com/Macro303/The-Pensieve/main/Resources/Images/mystery/{image_name}.png"
    embed.set_thumbnail(url=url)
    embed.add_field(name='Family', value=foundable.family)
    embed.add_field(name='Page', value=foundable.page)
    embed.add_field(name='Name', value=foundable.name)
    embed.add_field(name='Fragments', value=foundable.fragments if foundable.threat else 'Missing')
    LOGGER.debug(f"URL: {url}")
    embed.set_footer(text='Icons from https://github.com/Macro303/The-Pensieve')
    return embed


@db_session
def event_embed(foundable: Event) -> discord.Embed:
    embed = discord.Embed(title='Event Found',
                          colour=load_colour(foundable.method.get_colour() if foundable.method else '000000'))
    image_name = (foundable.family + '/' + foundable.name.replace('\'', '')).replace(' ', '-').lower()
    url = f"https://raw.githubusercontent.com/Macro303/The-Pensieve/main/Resources/Images/event/{image_name}.png"
    embed.set_thumbnail(url=url)
    embed.add_field(name='Family', value=foundable.family)
    embed.add_field(name='Page', value=foundable.page)
    embed.add_field(name='Name', value=foundable.name)
    embed.add_field(name='Method', value=foundable.method.name.title() if foundable.method else 'Missing')
    embed.add_field(name='Fragments', value=foundable.method.get_fragments() if foundable.method else 'Missing')
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
