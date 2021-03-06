#!/usr/bin/env python3
import logging

from discord import Embed
from discord.ext import commands
from pony.orm import db_session

from Bot import load_colour
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
        description='Returns details for the searched Chamber/s, including the associated challenge rewards.',
        usage='[Name of Chamber]'
    )
    async def chamber_search(self, ctx, *chamber_name: str):
        name = ' '.join(chamber_name)
        LOGGER.info(f"Looking for Chamber: {name}")
        with db_session:
            found = Chamber.select(lambda x: name.lower() == x.name.lower()).order_by(Chamber.name)[:]
            if not found:
                found = Chamber.select(lambda x: name.lower() in x.name.lower()).order_by(Chamber.name)[:]
            if not found:
                found = Chamber.select(lambda x: x.name.lower() in name.lower()).order_by(Chamber.name)[:]
            if found:
                for item in found:
                    await ctx.send(embed=cog_embed(
                        chamber=item,
                        author_name=ctx.message.author.name,
                        author_icon_url=ctx.message.author.avatar_url
                    ))
                await ctx.message.delete()
            else:
                LOGGER.warning(f"Unable to find the `{name}` Chamber.")
                await ctx.send(f"Unable to find the `{name}` Chamber.")


def setup(bot):
    bot.add_cog(ChamberCog(bot))
