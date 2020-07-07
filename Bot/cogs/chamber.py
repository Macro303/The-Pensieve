#!/usr/bin/env python3
import logging

from discord import Embed
from discord.ext import commands
from pony.orm import db_session

from Bot import load_colour
from Bot.cogs import get_message
from Database.database import Chamber

LOGGER = logging.getLogger(__name__)


def cog_embed(chamber: Chamber, author_name: str, author_icon_url: str) -> Embed:
    embed = Embed(title=chamber.name, colour=load_colour(chamber.get_colour()))

    embed.add_field(name='Exp', value=chamber.exp if chamber.exp else '~~Classified~~')
    embed.add_field(name='Challenge Exp', value=chamber.challenge_exp if chamber.challenge_exp else '~~Classified~~')

    pages = {}
    for item in chamber.challenges:
        if item.page not in pages:
            pages[item.page] = []
        pages[item.page].append(item.name)
    for page, items in pages.items():
        embed.add_field(name=f"Rewards: {page}", value=' - ' + ('\n - '.join(items)))

    embed.set_footer(
        text=f"Requested by {author_name} | Icons from https://github.com/Macro303/The-Pensieve",
        icon_url=author_icon_url
    )
    return embed


class ChamberCog(commands.Cog, name='Fortress Chambers'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='Chamber',
        description='Returns an embed with the searched for Chamber/s in the Fortress.',
        usage='[Name of Chamber]'
    )
    async def chamber_search(self, ctx):
        search = get_message(ctx)
        LOGGER.info(f"Looking up Chamber: `{search}`")

        if not search:
            LOGGER.warning(f"Unable to find the `{search}` Chamber.")
            await ctx.send(f"Unable to find the `{search}` Chamber.")
            return
        if len(search) < 3:
            LOGGER.warning('Your search is too short, must be longer than 3 characters')
            await ctx.send('Your search is too short, must be longer than 3 characters')
            return

        with db_session:
            found = Chamber.select(lambda x: search.lower() == x.name.lower()).order_by(Chamber.name)[:]
            if not found:
                found = Chamber.select(lambda x: search.lower() in x.name.lower()).order_by(Chamber.name)[:]
            if not found:
                found = Chamber.select(lambda x: x.name.lower() in search.lower()).order_by(Chamber.name)[:]
            if found:
                for item in found:
                    await ctx.send(embed=cog_embed(
                        chamber=item,
                        author_name=ctx.message.author.name,
                        author_icon_url=ctx.message.author.avatar_url
                    ))
            else:
                LOGGER.warning(f"Unable to find the `{search}` Chamber.")
                await ctx.send(f"Unable to find the `{search}` Chamber.")


def setup(bot):
    bot.add_cog(ChamberCog(bot))
