#!/usr/bin/env python3
import logging

import discord
from Bot import CONFIG
from Database.database import Exploration, Challenge, Mystery, Event
from Logger import init_logger
from discord.ext import commands
from pony.orm import db_session

LOGGER = logging.getLogger(__name__)
bot = commands.Bot(command_prefix=commands.when_mentioned_or(CONFIG['Prefix']), case_insensitive=True)


@bot.command(name='Family')
async def registry_family(ctx, family: str):
    LOGGER.info(f"Looking up `{family}`")
    with db_session:
        found = Exploration.select(lambda e: e.family == family) \
            .order_by(Exploration.family, Exploration.page, Exploration.name)
        if found:
            for item in found:
                await ctx.send(embed=exploration_embed(item))
        else:
            found = Challenge.select(lambda c: c.family == family) \
                .order_by(Challenge.family, Challenge.page, Challenge.name)
            if found:
                for item in found:
                    await ctx.send(embed=challenge_embed(item))
            else:
                found = Mystery.select(lambda m: m.family == family) \
                    .order_by(Mystery.family, Mystery.page, Mystery.name)
                if found:
                    for item in found:
                        await ctx.send(embed=mystery_embed(item))
                else:
                    found = Event.select(lambda e: e.family == family) \
                        .order_by(Event.family, Event.page, Event.name)
                    if found:
                        for item in found:
                            await ctx.send(embed=event_embed(item))
                    else:
                        LOGGER.warning(f"Unable to find `{family}` in the Registry")
                        await ctx.send(f"Unable to find `{family}` in the Registry")


@bot.command(name='Page')
async def registry_page(ctx, page: str):
    LOGGER.info(f"Looking up `{page}`")
    with db_session:
        found = Exploration.select(lambda e: e.page == page) \
            .order_by(Exploration.family, Exploration.page, Exploration.name)
        if found:
            for item in found:
                await ctx.send(embed=exploration_embed(item))
        else:
            found = Challenge.select(lambda c: c.page == page) \
                .order_by(Challenge.family, Challenge.page, Challenge.name)
            if found:
                for item in found:
                    await ctx.send(embed=challenge_embed(item))
            else:
                found = Mystery.select(lambda m: m.page == page) \
                    .order_by(Mystery.family, Mystery.page, Mystery.name)
                if found:
                    for item in found:
                        await ctx.send(embed=mystery_embed(item))
                else:
                    found = Event.select(lambda e: e.page == page) \
                        .order_by(Event.family, Event.page, Event.name)
                    if found:
                        for item in found:
                            await ctx.send(embed=event_embed(item))
                    else:
                        LOGGER.warning(f"Unable to find `{page}` in the Registry")
                        await ctx.send(f"Unable to find `{page}` in the Registry")


@bot.command(name='Foundable')
async def registry_foundable(ctx, name: str):
    LOGGER.info(f"Looking up `{name}`")
    with db_session:
        found = Exploration.select(lambda e: e.name == name) \
            .order_by(Exploration.family, Exploration.page, Exploration.name)
        if found:
            for item in found:
                await ctx.send(embed=exploration_embed(item))
        else:
            found = Challenge.select(lambda c: c.name == name) \
                .order_by(Challenge.family, Challenge.page, Challenge.name)
            if found:
                for item in found:
                    await ctx.send(embed=challenge_embed(item))
            else:
                found = Mystery.select(lambda m: m.name == name) \
                    .order_by(Mystery.family, Mystery.page, Mystery.name)
                if found:
                    for item in found:
                        await ctx.send(embed=mystery_embed(item))
                else:
                    found = Event.select(lambda e: e.name == name) \
                        .order_by(Event.family, Event.page, Event.name)
                    if found:
                        for item in found:
                            await ctx.send(embed=event_embed(item))
                    else:
                        LOGGER.warning(f"Unable to find `{name}` in the Registry")
                        await ctx.send(f"Unable to find `{name}` in the Registry")


@db_session
def exploration_embed(foundable: Exploration) -> discord.Embed:
    embed = discord.Embed(title=foundable.name)
    embed.add_field(name='Family', value=foundable.family)
    embed.add_field(name='Page', value=foundable.page)
    embed.add_field(name='Threat', value=foundable.threat.name.title())
    embed.add_field(name='Fragments', value=', '.join([str(i) for i in foundable.threat.get_fragments()]))
    return embed


@db_session
def challenge_embed(foundable: Challenge) -> discord.Embed:
    embed = discord.Embed(title=foundable.name)
    embed.add_field(name='Family', value=foundable.family)
    embed.add_field(name='Page', value=foundable.page)
    embed.add_field(name='Threat', value=foundable.threat.name.title())
    embed.add_field(name='Fragments', value=', '.join([str(i) for i in foundable.threat.get_fragments()]))
    return embed


@db_session
def mystery_embed(foundable: Mystery) -> discord.Embed:
    embed = discord.Embed(title=foundable.name)
    embed.add_field(name='Family', value=foundable.family)
    embed.add_field(name='Page', value=foundable.page)
    embed.add_field(name='Fragments', value=foundable.fragments)
    return embed


@db_session
def event_embed(foundable: Event) -> discord.Embed:
    embed = discord.Embed(title=foundable.name)
    embed.add_field(name='Family', value=foundable.family)
    embed.add_field(name='Page', value=foundable.page)
    embed.add_field(name='Method', value=foundable.method.name.title())
    embed.add_field(name='Fragments', value=foundable.method.get_fragments())
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
