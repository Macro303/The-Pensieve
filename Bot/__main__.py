#!/usr/bin/env python3
import logging
import discord
from discord.ext import commands
from pony.orm import db_session

from Bot import CONFIG
from Data import Foundable
from Logger import init_logger

LOGGER = logging.getLogger(__name__)
bot = commands.Bot(command_prefix=commands.when_mentioned_or(CONFIG['Prefix']), case_insensitive=True)

@bot.command(name='Family')
async def registry_family(ctx, name: str):
    LOGGER.info(f"Looking up `{name}`")
    with db_session:
        found = Founable.get(family=name)
        if found:
            for item in found.sorted():
                await ctx.send(embed=foundable_embed(item))
        else:
            LOGGER.warning(f"Unable to find `{name}` in the Registry")
            await ctx.send(f"Unable to find `{name}` in the Registry")

@bot.command(name='Page')
async def registry_page(ctx, name: str):
    LOGGER.info(f"Looking up `{name}`")
    with db_session:
        found = Foundable.get(page = name)
        if found:
            for item in found.sorted():
                await ctx.send(embed=founable_embed(item))
        else:
            LOGGER.warning(f"Unable to find `{name}` in the Registry")
            await ctx.send(f"Unable to find `{name}` in the Registry")

@bot.command(name='Foundable')
async def registry_founable(ctx, name: str):
    LOGGER.info(f"Looking up `{name}`")
    with db_session:
        found = Foundable.get(name = name)
        if found:
            await ctx.send(embed=foundable_embed(found))
        else:
            LOGGER.warning(f"Unable to find `{name}` in the Registry")
            await ctx.send(f"Unable to find `{name}` in the Registry")

@db_session
def foundable_embed(foundable: Foundable) -> discord.Embed:
    embed = discord.Embed(title=foundable.name, description=foundable.description)
    embed.add_field(name='Family', value=foundable.family)
    embed.add_field(name='Page', value=foundable.page)
    embed.add_field(name='Threat Level', value=foundable.threat.name.title())
    return embed

@bot.event
async def on_ready():
    LOGGER.info(f"Logged in as: {bot.user}")
    await bot.change_presence(activity=discord.Game(name='Harry Potter: Wizards Unite'))

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)

if if __name__ == "__main__":
    init_logger('The-Pensieve_Bot')
    bot.run(CONFIG['Token'])