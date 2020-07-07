#!/usr/bin/python3
import logging
from enum import Enum, auto
from typing import Optional as Opt, List
from uuid import UUID, uuid4

from pony.orm import Database, db_session, PrimaryKey, Required, Optional, composite_key, Set

LOGGER = logging.getLogger(__name__)
db = Database()


class Threat(Enum):
    FORTRESS = auto(), (7, 14, 21, 25), '333333'
    LOW = auto(), (15, 25, 38, 55), 'DDDDDD'
    MEDIUM = auto(), (12, 20, 30, 45), 'FFD700'
    HIGH = auto(), (9, 15, 22, 30), 'FF8C00'
    SEVERE = auto(), (5, 10, 13, 18), 'FF4500'
    EMERGENCY = auto(), (3, 5, 7, 10), 'FF6347'

    def __new__(cls, value, fragments, colour_code):
        member = object.__new__(cls)
        member._value_ = value
        member.fragments = fragments
        member.colour_code = colour_code
        return member

    def __int__(self):
        return self.value

    @classmethod
    def find_by_name(cls, name: Opt[str]):
        if not name:
            return None
        for value, entry in cls.__members__.items():
            if name.lower() == value.lower():
                return entry
        if name.lower() == 'blank':
            return Threat.FORTRESS

    def get_name(self) -> str:
        if self == Threat.FORTRESS:
            return '*Blank*'
        return self.name.title()


class Method(Enum):
    ENCOUNTER = auto(), 15, 'FFD700'
    PORTKEY = auto(), 5, 'FF8C00'
    FORTRESS = auto(), 3, 'FF4500'
    TASK = auto(), 1, 'FF6347'

    def __new__(cls, value, fragments, colour_code):
        member = object.__new__(cls)
        member._value_ = value
        member.fragments = fragments
        member.colour_code = colour_code
        return member

    def __int__(self):
        return self.value

    @classmethod
    def find_by_name(cls, name: Opt[str]):
        if not name:
            return None
        for value, entry in cls.__members__.items():
            if name.lower() == value.lower():
                return entry

    def get_name(self) -> str:
        return self.name.title()


class Exploration(db.Entity):
    uuid = PrimaryKey(UUID, default=uuid4)
    family = Required(str)
    page = Required(str)
    name = Required(str)
    threat = Optional(Threat, nullable=True)
    returned = Optional(str, nullable=True)
    description = Optional(str, nullable=True)

    composite_key(family, page, name)

    def get_colour(self) -> str:
        if self.threat:
            return self.threat.colour_code
        return '4682B4'

    @classmethod
    def create_or_update(cls, family: str, page: str, name: str, threat: Opt[Threat], returned: Opt[str] = None,
                         description: Opt[str] = None):
        with db_session:
            found = cls.get(family=family, page=page, name=name)
            if found:
                if threat and found.threat != threat:
                    found.threat = threat
                if returned and found.returned != returned:
                    found.returned = returned
                if description and found.description != description:
                    found.description = description
            else:
                cls(family=family, page=page, name=name, threat=threat, returned=returned, description=description)
                LOGGER.info(f"Created Exploration Entry: {family}, {page}, {name}")
                return cls.get(family=family, page=page, name=name)
            return found

    def __str__(self) -> str:
        return 'Exploration(' + \
               f"uuid={self.uuid}, " + \
               f"family={self.family}, " + \
               f"page={self.page}, " + \
               f"name={self.name}, " + \
               f"threat={self.threat}, " + \
               f"returned={self.returned}, " + \
               f"description={self.description}" + \
               ')'


class Challenge(db.Entity):
    uuid = PrimaryKey(UUID, default=uuid4)
    family = Required(str)
    page = Required(str)
    name = Required(str)
    returned = Optional(str, nullable=True)
    description = Optional(str, nullable=True)
    chambers = Set('Chamber')

    composite_key(family, page, name)

    def get_colour(self) -> str:
        return Threat.FORTRESS.colour_code

    @classmethod
    def create_or_update(cls, family: str, page: str, name: str, returned: Opt[str] = None,
                         description: Opt[str] = None):
        with db_session:
            found = cls.get(family=family, page=page, name=name)
            if found:
                if returned and found.returned != returned:
                    found.returned = returned
                if description and found.description != description:
                    found.description = description
            else:
                cls(family=family, page=page, name=name, returned=returned, description=description)
                LOGGER.info(f"Created Challenge Entry: {family}, {page}, {name}")
                return cls.get(family=family, page=page, name=name)
            return found

    def __str__(self) -> str:
        return 'Challenge(' + \
               f"uuid={self.uuid}, " + \
               f"family={self.family}, " + \
               f"page={self.page}, " + \
               f"name={self.name}, " + \
               f"returned={self.returned}, " + \
               f"description={self.description}" + \
               ')'


class Chamber(db.Entity):
    uuid = PrimaryKey(UUID, default=uuid4)
    name = Required(str)
    exp = Optional(int, nullable=True)
    challenge_exp = Optional(int, nullable=True)
    challenges = Set('Challenge')

    def get_colour(self) -> str:
        return '4682B4'

    @classmethod
    def create_or_update(cls, name: str, exp: Opt[int], challenge_exp: Opt[int], challenges: List[Challenge]):
        with db_session:
            found = cls.get(name=name)
            if found:
                if found.exp != exp:
                    found.exp = exp
                if found.challenge_exp != challenge_exp:
                    found.challenge_exp = challenge_exp
                if challenges and found.challenges != challenges:
                    found.challenges = challenges
            else:
                cls(name=name, exp=exp, challenge_exp=challenge_exp, challenges=challenges)
                LOGGER.info(f"Created Chamber Entry: {name}")
                return cls.get(name=name)
            return found

    def __str__(self) -> str:
        return 'Chamber(' + \
               f"uuid={self.uuid}, " + \
               f"name={self.name}, " + \
               f"exp={self.exp}, " + \
               f"challenge_exp={self.challenge_exp}, " + \
               f"challenges={self.challenges}" + \
               ')'


class Mystery(db.Entity):
    uuid = PrimaryKey(UUID, default=uuid4)
    family = Required(str)
    page = Required(str)
    name = Required(str)
    fragments = Optional(int, nullable=True)
    returned = Optional(str, nullable=True)
    description = Optional(str, nullable=True)

    composite_key(family, page, name)

    def get_colour(self) -> str:
        return '4682B4'

    @classmethod
    def create_or_update(cls, family: str, page: str, name: str, fragments: int, returned: Opt[str] = None,
                         description: Opt[str] = None):
        with db_session:
            found = cls.get(family=family, page=page, name=name)
            if found:
                if fragments and found.fragments != fragments:
                    found.fragments = fragments
                if returned and found.returned != returned:
                    found.returned = returned
                if description and found.description != description:
                    found.description = description
            else:
                cls(family=family, page=page, name=name, fragments=fragments, returned=returned,
                    description=description)
                LOGGER.info(f"Created Mystery Entry: {family}, {page}, {name}")
                return cls.get(family=family, page=page, name=name)
            return found

    def __str__(self) -> str:
        return 'Mystery(' + \
               f"uuid={self.uuid}, " + \
               f"family={self.family}, " + \
               f"page={self.page}, " + \
               f"name={self.name}, " + \
               f"fragments={self.fragments}, " + \
               f"returned={self.returned}, " + \
               f"description={self.description}" + \
               ')'


class Event(db.Entity):
    uuid = PrimaryKey(UUID, default=uuid4)
    family = Required(str)
    page = Required(str)
    name = Required(str)
    threat = Optional(Threat, nullable=True)
    method = Optional(Method, nullable=True)
    returned = Optional(str, nullable=True)
    description = Optional(str, nullable=True)

    composite_key(family, page, name)

    def get_colour(self) -> str:
        if self.threat:
            return self.threat.colour_code
        if self.method:
            return self.method.colour_code
        return '4682B4'

    @classmethod
    def create_or_update(cls, family: str, page: str, name: str, threat: Opt[Threat] = None, method: Opt[Method] = None,
                         returned: Opt[str] = None, description: Opt[str] = None):
        with db_session:
            found = cls.get(family=family, page=page, name=name)
            if found:
                if threat and found.threat != threat:
                    found.threat = threat
                if method and found.method != method:
                    found.method = method
                if returned and found.returned != returned:
                    found.returned = returned
                if description and found.description != description:
                    found.description = description
            else:
                cls(family=family, page=page, name=name, threat=threat, method=method, returned=returned,
                    description=description)
                LOGGER.info(f"Created Event Entry: {family}, {page}, {name}")
                return cls.get(family=family, page=page, name=name)
            return found

    def __str__(self) -> str:
        return 'Event(' + \
               f"uuid={self.uuid}, " + \
               f"family={self.family}, " + \
               f"page={self.page}, " + \
               f"name={self.name}, " + \
               f"threat={self.threat}, " + \
               f"method={self.method}, " + \
               f"returned={self.returned}, " + \
               f"description={self.description}" + \
               ')'
