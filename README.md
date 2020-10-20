<img src="./logo.png" align="left" width="128" height="128" alt="The Pensieve Logo"/>

# The Pensieve - Discord Bot
[![Version](https://img.shields.io/github/tag-pre/Macro303/The-Pensieve.svg?label=version&style=flat-square)](https://github.com/Macro303/The-Pensieve/releases)
[![Issues](https://img.shields.io/github/issues/Macro303/The-Pensieve.svg?style=flat-square)](https://github.com/Macro303/The-Pensieve/issues)
[![Contributors](https://img.shields.io/github/contributors/Macro303/The-Pensieve.svg?style=flat-square)](https://github.com/Macro303/The-Pensieve/graphs/contributors)
[![Visits](https://badges.pufler.dev/visits/Macro303/The-Pensieve?style=flat-square)](https://badges.pufler.dev)
[![License](https://img.shields.io/github/license/Macro303/The-Pensieve.svg?style=flat-square)](https://opensource.org/licenses/MIT)

Simple bot to show stats and other useful information for **Harry Potter: Wizards Unite**.  
To add this bot to your server follow this [Link](https://discord.com/api/oauth2/authorize?client_id=723013744808165438&permissions=67464256&scope=bot)

## Commands
Searches all registries (Exploration, Challenges, Mysteries, Events)  
_Fields marked as **~~Classified~~** have missing or incomplete information._

| Keyword | Variables | Description |
| ------- | --------- | ----------- |
| `?Family` | <ul><li>Name (Required)</li></ul> | Returns all the Pages and Foundables in the searched Family/s |
| `?Page` | <ul><li>Name (Required)</li></ul> | Returns all the Foundables in the searched Page/s |
| `?Foundable` | <ul><li>Name (Required)</li></ul> | Returns details for the searched Foundable/s |
| `?Chamber` | <ul><li>Name (Required)</li></ul> | Returns details for the searched Chamber/s, including the associated challenge rewards |
| `?help` | | Shows the command menu |

## Built Using
 - [Python: 3.8.5](https://www.python.org/)
 - [pip: 20.2.4](https://pypi.org/project/pip/)
 - [discord.py: 1.5.1](https://pypi.org/project/discord.py/)
 - [PyYAML: 5.3.1](https://pypi.org/project/PyYAML/)
 - [pony: 0.7.13](https://pypi.org/project/pony/)

## Execution
1. Run the following:
   ```bash
   $ pip install -r .\requirements.txt
   $ python -m Bot
   ```
2. Stop the script
3. Update the generated `config.yaml` with your Discord Token and Prefix of choice
4. Run the following:
   ```bash
   $ python -m Bot
   ```

## Socials
[![Discord | The Playground](https://discord.com/api/v6/guilds/618581423070117932/widget.png?style=banner2)](https://discord.gg/nqGMeGg)
 - Wizards Unite - Wellington [Discord Invite](https://discord.gg/dy3ZhkT)
