#!/usr/bin/env python3
import logging
from pathlib import Path
import re
from typing import List

import discord
import yaml

TOP_DIR = Path(__file__).resolve().parent.parent
LOGGER = logging.getLogger(__name__)

config_file = TOP_DIR.joinpath('config.yaml')
if config_file.exists():
    with open(config_file, 'r', encoding='UTF-8') as yaml_file:
        CONFIG = yaml.safe_load(yaml_file) or {
            'Prefix': '?',
            'Token': None
        }
else:
    config_file.touch()
    CONFIG = {
        'Prefix': '?',
        'Token': None
    }
with open(config_file, 'w', encoding='UTF-8') as yaml_file:
    yaml.safe_dump(CONFIG, yaml_file)