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
    def findByName(cls, name: Opt[str]):
        if not name:
            return None
        for value, entry in cls.__members__.items():
            if name.lower() == value.lower():
                return entry

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


class Method(Enum):
    ENCOUNTER = 0
    PORTKEY = 1
    FORTRESS = 2
    TASK = 3

    @classmethod
    def findByName(cls, name: Opt[str]):
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


class Exploration(db.Entity):
    uuid = PrimaryKey(UUID, default=uuid4)
    family = Required(str)
    page = Required(str)
    name = Required(str)
    threat = Optional(Threat, nullable=True)

    composite_key(family, page, name)

    @classmethod
    def get_or_create(cls, family: str, page: str, name: str, threat: Opt[Threat]):
        with db_session:
            found = cls.get(family=family, page=page, name=name, threat=threat)
            if not found:
                cls(family=family, page=page, name=name, threat=threat)
                return cls.get_or_create(family=family, page=page, name=name, threat=threat)
            return found

    def __str__(self) -> str:
        return 'Exploration(' + \
               f"uuid={self.uuid}, " + \
               f"family={self.family}, " + \
               f"page={self.page}, " + \
               f"name={self.name}, " + \
               f"threat={self.threat}" + \
               ')'


class Challenge(db.Entity):
    uuid = PrimaryKey(UUID, default=uuid4)
    family = Required(str)
    page = Required(str)
    name = Required(str)
    threat = Optional(Threat, nullable=True)

    composite_key(family, page, name)

    @classmethod
    def get_or_create(cls, family: str, page: str, name: str, threat: Threat):
        with db_session:
            found = cls.get(family=family, page=page, name=name, threat=threat)
            if not found:
                cls(family=family, page=page, name=name, threat=threat)
                return cls.get_or_create(family=family, page=page, name=name, threat=threat)
            return found

    def __str__(self) -> str:
        return 'Challenge(' + \
               f"uuid={self.uuid}, " + \
               f"family={self.family}, " + \
               f"page={self.page}, " + \
               f"name={self.name}, " + \
               f"threat={self.threat}" + \
               ')'


class Mystery(db.Entity):
    uuid = PrimaryKey(UUID, default=uuid4)
    family = Required(str)
    page = Required(str)
    name = Required(str)
    fragments = Optional(int, nullable=True)

    composite_key(family, page, name)

    @classmethod
    def get_or_create(cls, family: str, page: str, name: str, fragments: int):
        with db_session:
            found = cls.get(family=family, page=page, name=name, fragments=fragments)
            if not found:
                cls(family=family, page=page, name=name, fragments=fragments)
                return cls.get_or_create(family=family, page=page, name=name, fragments=fragments)
            return found

    def __str__(self) -> str:
        return 'Mystery(' + \
               f"uuid={self.uuid}, " + \
               f"family={self.family}, " + \
               f"page={self.page}, " + \
               f"name={self.name}, " + \
               f"fragments={self.fragments}" + \
               ')'


class Event(db.Entity):
    uuid = PrimaryKey(UUID, default=uuid4)
    family = Required(str)
    page = Required(str)
    name = Required(str)
    method = Optional(Method, nullable=True)

    composite_key(family, page, name)

    @classmethod
    def get_or_create(cls, family: str, page: str, name: str, method: Method):
        with db_session:
            found = cls.get(family=family, page=page, name=name, method=method)
            if not found:
                cls(family=family, page=page, name=name, method=method)
                return cls.get_or_create(family=family, page=page, name=name, method=method)
            return found

    def __str__(self) -> str:
        return 'Event(' + \
               f"uuid={self.uuid}, " + \
               f"family={self.family}, " + \
               f"page={self.page}, " + \
               f"name={self.name}, " + \
               f"method={self.method}" + \
               ')'
