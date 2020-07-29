<img src="https://raw.githubusercontent.com/Macro303/The-Pensieve/main/logo.png" align="left" width="128" height="128" alt="The Pensieve Logo"/>

# The Pensieve - Discord Bot
[![Version](https://img.shields.io/github/tag-pre/Macro303/The-Pensieve.svg?label=version&style=flat-square)](https://github.com/Macro303/The-Pensieve/releases)
[![Issues](https://img.shields.io/github/issues/Macro303/The-Pensieve.svg?style=flat-square)](https://github.com/Macro303/The-Pensieve/issues)
[![Contributors](https://img.shields.io/github/contributors/Macro303/The-Pensieve.svg?style=flat-square)](https://github.com/Macro303/The-Pensieve/graphs/contributors)
[![License](https://img.shields.io/github/license/Macro303/The-Pensieve.svg?style=flat-square)](https://opensource.org/licenses/MIT)

Simple bot to show stats and other useful information for **Harry Potter: Wizards Unite**.  
Current Commands _Searches all registries (Exploration, Challenges, Mysteries, Events)_:
 - **Family**: Returns all the Pages and Foundables in the searched for Family/s.
 - **Page**: Returns all the Families with the searched for Page/s, listing all the Foundables in the found Page/s.
 - **Foundable**: Returns details about the searched for Foundable/s _Fields marked as ~~Classified~~ have missing or incomplete information_.
 - **Chamber**: Returns details about the searched for Chamber/s, includes a list of possible challenge rewards in found chamber/s.
 - **Help**: Lists off commands, descriptions and their usages.

To add this bot to your server follow this [Link](https://discord.com/api/oauth2/authorize?client_id=723013744808165438&permissions=67464256&scope=bot)

## Built Using
 - [Python: 3.8.5](https://www.python.org/)
 - [pip: 20.1.1](https://pypi.org/project/pip/)
 - [PyInstaller: 3.6](https://pypi.org/project/PyInstaller/)
 - [discord.py: 1.3.4](https://pypi.org/project/discord.py/)
 - [PyYAML: 5.3.1](https://pypi.org/project/PyYAML/)
 - [pony: 0.7.13](https://pypi.org/project/pony/)

## Execution
Update `config.yaml` to add your Discord Token and other settings
```bash
$ pip install -r requirements.txt
$ python -m Bot
```
To pull data run
```bash
$ python -m Database
```

## Socials
[![Discord | The Playground](https://discord.com/api/v6/guilds/618581423070117932/widget.png?style=banner2)](https://discord.gg/nqGMeGg)
[![Discord | Wizards Unite - Wellington](https://discord.com/api/v6/guilds/577714667535728670/widget.png?style=banner2)](https://discord.gg/dy3ZhkT)
