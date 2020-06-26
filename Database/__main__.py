#!/usr/bin/python3
import csv
import logging

from Database import TOP_DIR
from Database.database import Threat, Exploration, Challenge, Mystery, Method, Event
from Logger import init_logger
from pony.orm import db_session

LOGGER = logging.getLogger(__name__)
DATA_DIR = TOP_DIR.joinpath('Resources').joinpath('CSV')


@db_session
def main():
    create_exploration_registry()
    Exploration.select().show(width=175)
    create_challenges_registry()
    Challenge.select().show(width=175)
    create_mysteries_registry()
    Mystery.select().show(width=175)
    create_events_registry()
    Event.select().show(width=175)


def create_exploration_registry():
    with open(DATA_DIR.joinpath('Registry - Exploration.csv'), mode='r') as csv_file:
        headers = [h.strip() for h in csv_file.readline().split(',')]
        csv_reader = csv.DictReader(csv_file, fieldnames=headers)
        for row in csv_reader:
            LOGGER.debug(row)
            if row['Family'].strip() and row['Page'].strip() and row['Name'].strip():
                if not row['Returned'].strip():
                    returned = None
                else:
                    returned = row['Returned'].strip()
                if not row['Description'].strip():
                    description = None
                else:
                    description = row['Description'].strip()
                exploration = Exploration.create_or_update(
                    family=row['Family'].strip(),
                    page=row['Page'].strip(),
                    name=row['Name'].strip(),
                    threat=Threat.find_by_name(row['Threat'].strip()),
                    returned=returned,
                    description=description
                )


def create_challenges_registry():
    with open(DATA_DIR.joinpath('Registry - Challenges.csv'), mode='r') as csv_file:
        headers = [h.strip() for h in csv_file.readline().split(',')]
        csv_reader = csv.DictReader(csv_file, fieldnames=headers)
        for row in csv_reader:
            LOGGER.debug(row)
            if row['Family'].strip() and row['Page'].strip() and row['Name'].strip():
                if not row['Returned'].strip():
                    returned = None
                else:
                    returned = row['Returned'].strip()
                if not row['Description'].strip():
                    description = None
                else:
                    description = row['Description'].strip()
                challenge = Challenge.create_or_update(
                    family=row['Family'].strip(),
                    page=row['Page'].strip(),
                    name=row['Name'].strip(),
                    threat=Threat.find_by_name(row['Threat'].strip()),
                    returned=returned,
                    description=description
                )


def create_mysteries_registry():
    with open(DATA_DIR.joinpath('Registry - Mysteries.csv'), mode='r') as csv_file:
        headers = [h.strip() for h in csv_file.readline().split(',')]
        csv_reader = csv.DictReader(csv_file, fieldnames=headers)
        for row in csv_reader:
            LOGGER.debug(row)
            if row['Family'].strip() and row['Page'].strip() and row['Name'].strip():
                if not row['Returned'].strip():
                    returned = None
                else:
                    returned = row['Returned'].strip()
                if not row['Description'].strip():
                    description = None
                else:
                    description = row['Description'].strip()
                mystery = Mystery.create_or_update(
                    family=row['Family'].strip(),
                    page=row['Page'].strip(),
                    name=row['Name'].strip(),
                    fragments=int(row['Fragments'].strip()) if row['Fragments'] and
                                                               row['Fragments'].isdigit() else None,
                    returned=returned,
                    description=description
                )


def create_events_registry():
    with open(DATA_DIR.joinpath('Registry - Events.csv'), mode='r') as csv_file:
        headers = [h.strip() for h in csv_file.readline().split(',')]
        csv_reader = csv.DictReader(csv_file, fieldnames=headers)
        for row in csv_reader:
            LOGGER.debug(row)
            if row['Family'].strip() and row['Page'].strip() and row['Name'].strip():
                if not row['Returned'].strip():
                    returned = None
                else:
                    returned = row['Returned'].strip()
                if not row['Description'].strip():
                    description = None
                else:
                    description = row['Description'].strip()
                event = Event.create_or_update(
                    family=row['Family'].strip(),
                    page=row['Page'].strip(),
                    name=row['Name'].strip(),
                    threat=Threat.find_by_name(row['Threat'].strip()),
                    method=Method.find_by_name(row['Method'].strip()),
                    returned=returned,
                    description=description
                )


if __name__ == '__main__':
    init_logger('The-Pensieve_Data')
    main()
