#!/usr/bin/env python3
import logging

from discord import Embed
from discord.ext import commands
from pony.orm import db_session

from Bot import load_colour
from Bot.cogs import get_message
from Database.database import Exploration, Challenge, Mystery, Event, Threat

LOGGER = logging.getLogger(__name__)


def exploration_embed(foundable: Exploration, author_name: str, author_icon_url: str) -> Embed:
    embed = Embed(
        title='Exploration Foundable Found',
        colour=load_colour(foundable.get_colour()),
        description=f"```{foundable.description}```" if foundable.description else None
    )

    embed.add_field(name='Family', value=foundable.family)
    embed.add_field(name='Page', value=foundable.page)
    embed.add_field(name='Name', value=foundable.name)
    embed.add_field(name='Threat', value=foundable.threat.get_name() if foundable.threat else '~~Classified~~')
    embed.add_field(name='Fragments',
                    value='/'.join([str(i) for i in foundable.threat.fragments])
                    if foundable.threat else '~~Classified~~')
    embed.add_field(name='Returned To', value=foundable.returned if foundable.returned else '~~Classified~~')

    image_name = '/'.join([x.replace('\'/:,', '') for x in [foundable.family, foundable.name]]) \
        .replace(' ', '-').lower()
    url = f"https://raw.githubusercontent.com/Macro303/The-Pensieve/main/Resources/Images/exploration/{image_name}.png"
    LOGGER.debug(f"URL: {url}")
    embed.set_thumbnail(url=url)

    embed.set_footer(
        text=f"Requested by {author_name} | Icons from https://github.com/Macro303/The-Pensieve",
        icon_url=author_icon_url
    )
    return embed


def challenge_embed(foundable: Challenge, author_name: str, author_icon_url: str) -> Embed:
    embed = Embed(
        title='Challenge Foundable Found',
        colour=load_colour(foundable.get_colour()),
        description=f"```{foundable.description}```" if foundable.description else None
    )

    embed.add_field(name='Family', value=foundable.family)
    embed.add_field(name='Page', value=foundable.page)
    embed.add_field(name='Name', value=foundable.name)
    embed.add_field(name='Threat', value=Threat.FORTRESS.get_name())
    embed.add_field(name='Fragments', value='/'.join([str(i) for i in Threat.FORTRESS.fragments]))
    # embed.add_field(name='Rooms', value=', '.join([x.get_name() for x in foundable.get_rooms()]))
    embed.add_field(name='Returned To', value=foundable.returned if foundable.returned else '~~Classified~~')

    image_name = '/'.join([x.replace('\'/:,', '') for x in [foundable.page, foundable.name]]) \
        .replace(' ', '-').lower()
    url = f"https://raw.githubusercontent.com/Macro303/The-Pensieve/main/Resources/Images/challenges/{image_name}.png"
    LOGGER.debug(f"URL: {url}")
    embed.set_thumbnail(url=url)

    embed.set_footer(
        text=f"Requested by {author_name} | Icons from https://github.com/Macro303/The-Pensieve",
        icon_url=author_icon_url
    )
    return embed


def mystery_embed(foundable: Mystery, author_name: str, author_icon_url: str) -> Embed:
    embed = Embed(
        title='Mystery Foundable Found',
        colour=load_colour(foundable.get_colour()),
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


def event_embed(foundable: Event, author_name: str, author_icon_url: str) -> Embed:
    embed = Embed(
        title='Event Foundable Found',
        colour=load_colour(foundable.get_colour()),
        description=f"```{foundable.description}```" if foundable.description else None
    )

    embed.add_field(name='Family', value=foundable.family)
    embed.add_field(name='Page', value=foundable.page)
    embed.add_field(name='Name', value=foundable.name)
    embed.add_field(name='Threat', value=foundable.threat.get_name() if foundable.threat else '~~Classified~~')
    embed.add_field(name='Method', value=foundable.method.get_name() if foundable.method else '~~Classified~~')
    embed.add_field(name='Fragments', value=foundable.method.fragments if foundable.method else '/'.join(
        [str(i) for i in foundable.threat.fragments]) if foundable.threat else '~~Classified~~')
    embed.add_field(name='Returned To', value=foundable.returned if foundable.returned else '~~Classified~~')

    image_name = '/'.join([x.replace('\'/:,', '') for x in [foundable.family, foundable.name]]) \
        .replace(' ', '-').lower()
    url = f"https://raw.githubusercontent.com/Macro303/The-Pensieve/main/Resources/Images/events/{image_name}.png"
    LOGGER.debug(f"URL: {url}")
    embed.set_thumbnail(url=url)

    embed.set_footer(
        text=f"Requested by {author_name} | Icons from https://github.com/Macro303/The-Pensieve",
        icon_url=author_icon_url
    )
    return embed


class FoundableCog(commands.Cog, name='Registry Foundables'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='Foundable',
        description='Returns an embed with the searched for Foundable/s in the Registry.',
        usage='[Name of Foundable]'
    )
    async def foundable_search(self, ctx):
        search = get_message(ctx)
        LOGGER.info(f"Looking up Foundable: `{search}`")

        if not search:
            LOGGER.warning(f"Unable to find the `{search}` Foundable in the Registry")
            await ctx.send(f"Unable to find the `{search}` Foundable in the Registry")
            return
        if len(search) < 3:
            LOGGER.warning('Your search is too short, must be longer than 3 characters')
            await ctx.send('Your search is too short, must be longer than 3 characters')
            return

        with db_session:
            found = [
                *Exploration.select(lambda x: search.lower() == x.name.lower())
                     .order_by(Exploration.family, Exploration.page, Exploration.name)[:],
                *Challenge.select(lambda x: search.lower() == x.name.lower())
                     .order_by(Challenge.family, Challenge.page, Challenge.name)[:],
                *Mystery.select(lambda x: search.lower() == x.name.lower())
                     .order_by(Mystery.family, Mystery.page, Mystery.name)[:],
                *Event.select(lambda x: search.lower() == x.name.lower())
                     .order_by(Event.family, Event.page, Event.name)[:],
            ]
            if not found:
                found = [
                    *Exploration.select(lambda x: search.lower() in x.name.lower())
                         .order_by(Exploration.family, Exploration.page, Exploration.name)[:],
                    *Challenge.select(lambda x: search.lower() in x.name.lower())
                         .order_by(Challenge.family, Challenge.page, Challenge.name)[:],
                    *Mystery.select(lambda x: search.lower() in x.name.lower())
                         .order_by(Mystery.family, Mystery.page, Mystery.name)[:],
                    *Event.select(lambda x: search.lower() in x.name.lower())
                         .order_by(Event.family, Event.page, Event.name)[:],
                ]
            if not found:
                found = [
                    *Exploration.select(lambda x: x.name.lower() in search.lower())
                         .order_by(Exploration.family, Exploration.page, Exploration.name)[:],
                    *Challenge.select(lambda x: x.name.lower() in search.lower())
                         .order_by(Challenge.family, Challenge.page, Challenge.name)[:],
                    *Mystery.select(lambda x: x.name.lower() in search.lower())
                         .order_by(Mystery.family, Mystery.page, Mystery.name)[:],
                    *Event.select(lambda x: x.name.lower() in search.lower())
                         .order_by(Event.family, Event.page, Event.name)[:],
                ]
            if found:
                for foundable in found:
                    if isinstance(foundable, Exploration):
                        await ctx.send(embed=exploration_embed(
                            foundable=foundable,
                            author_name=ctx.message.author.name,
                            author_icon_url=ctx.message.author.avatar_url
                        ))
                    elif isinstance(foundable, Challenge):
                        await ctx.send(embed=challenge_embed(
                            foundable=foundable,
                            author_name=ctx.message.author.name,
                            author_icon_url=ctx.message.author.avatar_url
                        ))
                    elif isinstance(foundable, Mystery):
                        await ctx.send(embed=mystery_embed(
                            foundable=foundable,
                            author_name=ctx.message.author.name,
                            author_icon_url=ctx.message.author.avatar_url
                        ))
                    elif isinstance(foundable, Event):
                        await ctx.send(embed=event_embed(
                            foundable=foundable,
                            author_name=ctx.message.author.name,
                            author_icon_url=ctx.message.author.avatar_url
                        ))
            else:
                LOGGER.warning(f"Unable to find the `{search}` Foundable in the Registry")
                await ctx.send(f"Unable to find the `{search}` Foundable in the Registry")


def setup(bot):
    bot.add_cog(FoundableCog(bot))
