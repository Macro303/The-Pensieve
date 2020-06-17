#!/usr/bin/python3
from pony.orm import Database, db_session, PrimaryKey, Required, composite_key
from uuid import UUID, uuid4
import logging
from typing import Optional as Opt
from enum import Enum

LOGGER = logging.getLogger(__name__)
db = Database()

class Threat(Enum):
    UNMAPPED = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    RARE = 4
    SEVERE = 5
    EMERGENCY = 6

    @classmethod
    def findByName(cls, name: Opt[str]):
        if not value:
            return None
        for value, entry in cls.__members__.items():
            if name.lower() == value.lower():
                return entry

class Foundable(db.Entity):
    uuid = PrimaryKey(UUID, default=uuid4)
    family = Required(str)
    page = Required(str)
    name = Required(str)
    threat = Required(Threat, default=Threat.UNMAPPED)

    composite_key(family, page, name)

    @classmethod
    def get_or_create(cls, family: str, page: str, name: str, threat: Threat = Threat.UNMAPPED):
        with db_session:
            found = cls.get(family=family, page=page, name=name, threat=threat)
            if not found:
                cls(family=family, page=page, name=name, threat=threat)
                return cls.get_or_create(family=family, page=page, name=name, threat=threat)
            return found

    
    def __str__(self) -> str:
        return 'Foundable(' +\
            f"uuid={self.uuid}, " +\
            f"family={self.family}, " +\
            f"page={self.page}, " +\
            f"name={self.name}, " +\
            f"threat={self.threat}" +\
            ')'