#!/usr/bin/env python3
import logging

from discord import Embed
from discord.ext import commands
from Bot import CONFIG

LOGGER = logging.getLogger(__name__)


class HelpCog(commands.Cog, name='Help'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='Help',
        description='The help command',
        usage=''
    )
    async def help_command(self, ctx, cog='all'):
        embed = Embed(
            title='Help',
            description='*Responses from **The Pensieve** marked as ~~Classified~~ have incomplete information*\nAll searches are required to be more than 3 characters long.'
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)

        cogs = [c for c in self.bot.cogs.keys()]
        for cog in cogs:
            cog_commands = self.bot.get_cog(cog).get_commands()
            commands_list = '\n'.join([f"**{comm.name}** - `{CONFIG['Prefix']}{comm.name} {comm.usage}`\n*{comm.description}*" for comm in cog_commands])

            embed.add_field(name=cog, value=commands_list, inline=False)

        embed.set_footer(
            text=f"Requested by {ctx.message.author.name}",
            icon_url=ctx.message.author.avatar_url
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(HelpCog(bot))
