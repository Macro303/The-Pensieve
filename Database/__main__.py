#!/usr/bin/python3
import csv
import logging

from Database import TOP_DIR
from Database.database import Threat, Exploration, Challenge, Mystery, Method, Event
from Logger import init_logger
from pony.orm import db_session

LOGGER = logging.getLogger(__name__)
DATA_DIR = TOP_DIR.joinpath('Data')


@db_session
def main():
    create_exploration_registry()
    create_challenges_registry()
    create_mysteries_registry()
    create_events_registry()


def create_exploration_registry():
    with open(DATA_DIR.joinpath('Registry - Exploration.csv'), mode='r') as csv_file:
        headers = [h.strip() for h in csv_file.readline().split(',')]
        csv_reader = csv.DictReader(csv_file, fieldnames=headers)
        for row in csv_reader:
            LOGGER.debug(row)
            exploration = Exploration.get_or_create(
                family=row['Family'].strip(),
                page=row['Page'].strip(),
                name=row['Name'].strip(),
                threat=Threat.findByName(row['Threat'].strip())
            )
            LOGGER.info(exploration)


def create_challenges_registry():
    with open(DATA_DIR.joinpath('Registry - Challenges.csv'), mode='r') as csv_file:
        headers = [h.strip() for h in csv_file.readline().split(',')]
        csv_reader = csv.DictReader(csv_file, fieldnames=headers)
        for row in csv_reader:
            LOGGER.debug(row)
            if row['Threat'].strip():
                challenge = Challenge.get_or_create(
                    family=row['Family'].strip(),
                    page=row['Page'].strip(),
                    name=row['Name'].strip(),
                    threat=Threat.findByName(row['Threat'].strip())
                )
                LOGGER.info(challenge)


def create_mysteries_registry():
    with open(DATA_DIR.joinpath('Registry - Mysteries.csv'), mode='r') as csv_file:
        headers = [h.strip() for h in csv_file.readline().split(',')]
        csv_reader = csv.DictReader(csv_file, fieldnames=headers)
        for row in csv_reader:
            LOGGER.debug(row)
            if row['Name'].strip() and row['Fragments'].strip():
                mystery = Mystery.get_or_create(
                    family=row['Family'].strip(),
                    page=row['Page'].strip(),
                    name=row['Name'].strip(),
                    fragments=int(row['Fragments'].strip())
                )
                LOGGER.info(mystery)


def create_events_registry():
    with open(DATA_DIR.joinpath('Registry - Events.csv'), mode='r') as csv_file:
        headers = [h.strip() for h in csv_file.readline().split(',')]
        csv_reader = csv.DictReader(csv_file, fieldnames=headers)
        for row in csv_reader:
            LOGGER.debug(row)
            if row['Name'].strip() and row['Method'].strip():
                event = Event.get_or_create(
                    family=row['Family'].strip(),
                    page=row['Page'].strip(),
                    name=row['Name'].strip(),
                    method=Method.findByName(row['Method'].strip())
                )
                LOGGER.info(event)


if __name__ == '__main__':
    init_logger('The-Pensieve_Data')
    main()
