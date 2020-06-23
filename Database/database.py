#!/usr/bin/python3
import logging
from enum import Enum
from typing import Optional as Opt, Tuple
from uuid import UUID, uuid4

from pony.orm import Database, db_session, PrimaryKey, Required, Optional, composite_key

LOGGER = logging.getLogger(__name__)
db = Database()


class Threat(Enum):
    FORTRESS = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    SEVERE = 4
    EMERGENCY = 5

    @classmethod
    def find_by_name(cls, name: Opt[str]):
        if not name:
            return None
        for value, entry in cls.__members__.items():
            if name.lower() == value.lower():
                return entry
        if name.lower() == 'blank':
            return Threat.FORTRESS

    def get_fragments(self) -> Tuple[int, int, int, int]:
        if self == Threat.FORTRESS:
            return 7, 14, 21, 25
        elif self == Threat.LOW:
            return 15, 25, 38, 55
        elif self == Threat.MEDIUM:
            return 12, 20, 30, 45
        elif self == Threat.HIGH:
            return 9, 15, 22, 30
        elif self == Threat.SEVERE:
            return 5, 10, 13, 18
        elif self == Threat.EMERGENCY:
            return 3, 5, 7, 10

    def get_colour(self) -> str:
        if self == Threat.FORTRESS:
            return '000000'
        elif self == Threat.LOW:
            return 'FFFFFF'
        elif self == Threat.MEDIUM:
            return 'FFD700'
        elif self == Threat.HIGH:
            return 'FF8C00'
        elif self == Threat.SEVERE:
            return 'FF4500'
        elif self == Threat.EMERGENCY:
            return 'FF6347'

    def get_name(self) -> str:
        if self == Threat.FORTRESS:
            return '*Blank*'
        return self.name.title()


class Method(Enum):
    ENCOUNTER = 0
    PORTKEY = 1
    FORTRESS = 2
    TASK = 3

    @classmethod
    def find_by_name(cls, name: Opt[str]):
        if not name:
            return None
        for value, entry in cls.__members__.items():
            if name.lower() == value.lower():
                return entry

    def get_fragments(self) -> int:
        if self == Method.ENCOUNTER:
            return 15
        elif self == Method.PORTKEY:
            return 5
        elif self == Method.FORTRESS:
            return 3
        elif self == Method.TASK:
            return 1

    def get_colour(self) -> str:
        if self == Method.ENCOUNTER:
            return 'FFD700'
        elif self == Method.PORTKEY:
            return 'FF8C00'
        elif self == Method.FORTRESS:
            return 'FF4500'
        elif self == Method.TASK:
            return 'FF6347'

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

    @classmethod
    def get_or_create(cls, family: str, page: str, name: str, threat: Opt[Threat], returned: Opt[str] = None,
                      description: Opt[str] = None):
        with db_session:
            if not returned:
                returned = None
            if not description:
                description = None
            found = cls.get(family=family, page=page, name=name)
            if not found:
                cls(family=family, page=page, name=name, threat=threat, returned=returned, description=description)
                return cls.get_or_create(family=family, page=page, name=name, threat=threat, returned=returned,
                                         description=description)
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
    threat = Optional(Threat, nullable=True)
    returned = Optional(str, nullable=True)
    description = Optional(str, nullable=True)

    composite_key(family, page, name)

    @classmethod
    def get_or_create(cls, family: str, page: str, name: str, threat: Threat, returned: Opt[str] = None,
                      description: Opt[str] = None):
        with db_session:
            if not returned:
                returned = None
            if not description:
                description = None
            found = cls.get(family=family, page=page, name=name)
            if not found:
                cls(family=family, page=page, name=name, threat=threat, returned=returned, description=description)
                return cls.get_or_create(family=family, page=page, name=name, threat=threat, returned=returned,
                                         description=description)
            return found

    def __str__(self) -> str:
        return 'Challenge(' + \
               f"uuid={self.uuid}, " + \
               f"family={self.family}, " + \
               f"page={self.page}, " + \
               f"name={self.name}, " + \
               f"threat={self.threat}, " + \
               f"returned={self.returned}, " + \
               f"description={self.description}" + \
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

    @classmethod
    def get_or_create(cls, family: str, page: str, name: str, fragments: int, returned: Opt[str] = None,
                      description: Opt[str] = None):
        with db_session:
            if not returned:
                returned = None
            if not description:
                description = None
            found = cls.get(family=family, page=page, name=name)
            if not found:
                cls(family=family, page=page, name=name, fragments=fragments, returned=returned,
                    description=description)
                return cls.get_or_create(family=family, page=page, name=name, fragments=fragments, returned=returned,
                                         description=description)
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

    @classmethod
    def get_or_create(cls, family: str, page: str, name: str, threat: Opt[Threat] = None, method: Opt[Method] = None,
                      returned: Opt[str] = None, description: Opt[str] = None):
        with db_session:
            if not returned:
                returned = None
            if not description:
                description = None
            found = cls.get(family=family, page=page, name=name)
            if not found:
                cls(family=family, page=page, name=name, threat=threat, method=method, returned=returned,
                    description=description)
                return cls.get_or_create(family=family, page=page, name=name, threat=threat, method=method,
                                         returned=returned, description=description)
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
