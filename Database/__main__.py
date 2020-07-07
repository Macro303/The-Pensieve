#!/usr/bin/python3
import csv
import logging
from argparse import ArgumentParser, Namespace

from pony.orm import db_session

from Database import TOP_DIR
from Database.database import Threat, Exploration, Chamber, Challenge, Mystery, Method, Event
from Logger import init_logger

LOGGER = logging.getLogger(__name__)
DATA_DIR = TOP_DIR.joinpath('Resources').joinpath('CSV')


def get_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('-t', '--tables', action='store_true')
    return parser.parse_args()


args = get_arguments()


@db_session
def main():
    create_exploration_registry()
    if args.tables:
        Exploration.select().show(width=175)
    create_challenges_registry()
    if args.tables:
        Challenge.select().show(width=175)
    create_chambers_registry()
    if args.tables:
        Chamber.select().show(width=175)
    create_mysteries_registry()
    if args.tables:
        Mystery.select().show(width=175)
    create_events_registry()
    if args.tables:
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
                Exploration.create_or_update(
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
                Challenge.create_or_update(
                    family=row['Family'].strip(),
                    page=row['Page'].strip(),
                    name=row['Name'].strip(),
                    returned=returned,
                    description=description
                )


def create_chambers_registry():
    with open(DATA_DIR.joinpath('Registry - Chambers.csv'), mode='r') as csv_file:
        headers = [h.strip() for h in csv_file.readline().split(',')]
        csv_reader = csv.DictReader(csv_file, fieldnames=headers)
        for row in csv_reader:
            LOGGER.debug(row)
            if row['Name'].strip():
                challenge_list = [Challenge.get(name=it.strip()) for it in row['Challenge List'].strip().split('|') if it]
                challenges = [x for x in challenge_list if x]
                Chamber.create_or_update(
                    name=row['Name'].strip(),
                    exp=row['Exp'].strip() or None,
                    challenge_exp=row['Challenge Exp'].strip() or None,
                    challenges=challenges
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
                Mystery.create_or_update(
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
                Event.create_or_update(
                    family=row['Family'].strip(),
                    page=row['Page'].strip(),
                    name=row['Name'].strip(),
                    threat=Threat.find_by_name(row['Threat'].strip()),
                    method=Method.find_by_name(row['Method'].strip()),
                    returned=returned,
                    description=description
                )


if __name__ == '__main__':
    init_logger('The-Pensieve_Database')
    main()
