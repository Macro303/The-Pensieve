#!/usr/bin/python3
import logging
from enum import Enum, auto
from typing import Optional as Opt, List
from uuid import UUID, uuid4

from pony.orm import Database, db_session, PrimaryKey, Required, Optional, composite_key

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


class Room(Enum):
    RUINS_CHAMBER_I = 0, 'Ruins Chamber I'
    RUINS_CHAMBER_II = 1, 'Ruins Chamber II'
    RUINS_CHAMBER_III = 2, 'Ruins Chamber III'
    RUINS_CHAMBER_IV = 3, 'Ruins Chamber IV'
    RUINS_CHAMBER_V = 4, 'Ruins Chamber V'
    TOWER_CHAMBER_I = 5, 'Tower Chamber I'
    TOWER_CHAMBER_II = 6, 'Tower Chamber II'
    TOWER_CHAMBER_III = 7, 'Tower Chamber III'
    TOWER_CHAMBER_IV = 8, 'Tower Chamber IV'
    TOWER_CHAMBER_V = 9, 'Tower Chamber V'
    FOREST_CHAMBER_I = 10, 'Forest Chamber I'
    FOREST_CHAMBER_II = 11, 'Forest Chamber II'
    FOREST_CHAMBER_III = 12, 'Forest Chamber III'
    FOREST_CHAMBER_IV = 13, 'Forest Chamber IV'
    FOREST_CHAMBER_V = 14, 'Forest Chamber V'
    DARK_CHAMBER_I = 15, 'Dark Chamber I'
    DARK_CHAMBER_II = 16, 'Dark Chamber II'
    DARK_CHAMBER_III = 17, 'Dark Chamber III'
    DARK_CHAMBER_IV = 18, 'Dark Chamber IV'
    DARK_CHAMBER_V = 19, 'Dark Chamber V'

    def __new__(cls, value, clean_name):
        member = object.__new__(cls)
        member._value_ = value
        member.clean_name = clean_name
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
        return self.clean_name


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
    min_room = Optional(Room, nullable=True)
    max_room = Optional(Room, nullable=True)
    returned = Optional(str, nullable=True)
    description = Optional(str, nullable=True)

    composite_key(family, page, name)

    @classmethod
    def create_or_update(cls, family: str, page: str, name: str, min_room: Room, max_room: Room,
                         returned: Opt[str] = None, description: Opt[str] = None):
        with db_session:
            found = cls.get(family=family, page=page, name=name)
            if found:
                if min_room and found.min_room != min_room:
                    found.min_room = min_room
                if max_room and found.max_room != max_room:
                    found.max_room = max_room
                if returned and found.returned != returned:
                    found.returned = returned
                if description and found.description != description:
                    found.description = description
            else:
                cls(family=family, page=page, name=name, min_room=min_room, max_room=max_room, returned=returned,
                    description=description)
                LOGGER.info(f"Created Challenge Entry: {family}, {page}, {name}")
                return cls.get(family=family, page=page, name=name)
            return found

    def get_rooms(self) -> List[Room]:
        if self.min_room:
            min_index = int(self.min_room)
        else:
            min_index = 0
        if self.max_room:
            max_index = int(self.max_room) + 1
        else:
            max_index = 0
        names = set()
        for index in range(min_index, max_index):
            names.add(Room(index))
        return sorted(names, key=lambda x: int(x))

    def __str__(self) -> str:
        return 'Challenge(' + \
               f"uuid={self.uuid}, " + \
               f"family={self.family}, " + \
               f"page={self.page}, " + \
               f"name={self.name}, " + \
               f"min_room={self.min_room}, " + \
               f"max_room={self.max_room}, " + \
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
