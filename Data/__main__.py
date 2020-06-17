#!/usr/bin/python3
import logging
from Logger import init_logger
from pony.orm import db_session
from Data.Database import Foundable, Threat

LOGGER = logging.getLogger(__name__)

@db_session
def main():
    create_foundables()

def create_foundables():
    registry = {
        'Care of Magical Creatures': {
            'Hagrid\'s Hut': {
                'Abraxian Winged Horse': Threat.RARE,
                'Hagrid\'s Hut': Threat.RARE,
                'Rubeus Hagrid': Threat.EMERGENCY,
                'Buckbeak': Threat.SEVERE,
                'Baby Norwegian Ridgeback': Threat.HIGH
            },
            'Pumpkin Patch': {
                'Kneazle': Threat.LOW,
                'Baby Hippogriff': Threat.LOW,
                'Flobberwurm': Threat.LOW,
                'Monster Book of Monsters': Threat.MEDIUM,
                'Acromantula Eggs': Threat.LOW
            },
            'Forbidden Forest': {
                'Hippogriff': Threat.HIGH,
                'Firenze': Threat.SEVERE,
                'Baby Unicorn': Threat.MEDIUM,
                'Blast-Ended Skrewt': Threat.MEDIUM,
                'Dragon Egg': Threat.MEDIUM,
                # 'Unknown': Threat.RARE
            }
        },
        'Dark Arts': {
            'Borgin & Burkes': {
                'Wanted Poster of an Azkaban Escapee': Threat.LOW,
                'Magick Moste Evile': Threat.LOW,
                'Vanishing Cabinet': Threat.MEDIUM,
                'Flesh-Eating Slugs': Threat.LOW,
                'Hand of Glory': Threat.LOW
            },
            'Knockturn Alley': {
                # 'Unknown': Threat.SEVERE,
                # 'Unknown': Threat.RARE,
                'Portrait of Bellatrix Lestrange': Threat.MEDIUM,
                'Hag': Threat.MEDIUM,
                'Thestral': Threat.HIGH,
                'Ministry Executioner': Threat.HIGH
            },
            'Fallen Ministry Atrium': {
                # 'Unknown': Threat.RARE,
                # 'Unknown': Threat.RARE,
                # 'Unknown': Threat.SEVERE,
                # 'Unknown': Threat.EMERGENCY,
                # 'Unknown': Threat.HIGH
            }
        },
        'Hogwarts School': {
            'DADA Classroom': {
                'Gryffindor Student': Threat.LOW,
                'Ravenclaw Student': Threat.LOW,
                'Hufflepuff Student': Threat.LOW,
                'Boggart Cabinet': Threat.MEDIUM,
                'Slytherin Student': Threat.LOW
            },
            'Moving Staircases': {
                'Professor Flitwick': Threat.MEDIUM,
                # 'Unknown': Threat.EMERGENCY,
                'Peeves': Threat.HIGH,
                # 'Unknown': Threat.RARE,
                # 'Unknown': Threat.HIGH,
                'Pomona Sprout': Threat.MEDIUM
            },
            'Great Hall': {
                # 'Unknown': Threat.SEVERE,
                # 'Unknown': Threat.MEDIUM,
                # 'Unknown': Threat.RARE,
                'Owl Lecturn': Threat.RARE,
                # 'Unknown': Threat.SEVERE
            },
            'Moving Staircases II': {
                # 'Unknown': Threat.HIGH,
                # 'Unknown': Threat.RARE,
                # 'Unknown': Threat.HIGH,
                'Portrait of Rowena Ravenclaw': Threat.HIGH,
                'Portrait of Godric Gryffindor': Threat.HIGH
            }
        },
        'Legends of Hogwarts': {
            'Room of Requirements I': {
                'Filch and Mrs. Norris': Threat.LOW,
                # 'Unknown': Threat.MEDIUM,
                'Young Ginny Weasley': Threat.MEDIUM,
                'Young Luna Lovegood': Threat.MEDIUM,
                'Dumbledore\'s Army Dueling Dummy': Threat.LOW,
                'Weasley Fireworks': Threat.LOW
            },
            'Potions Classroom': {
                'Young Harry Potter': Threat.SEVERE,
                'Hedwig': Threat.LOW,
                # 'Unknown': Threat.RARE,
                # 'Unknown': Threat.HIGH,
                # 'Unknown': Threat.HIGH
            },
            'Chess Chamber': {
                # 'Unknown': Threat.SEVERE,
                # 'Unknown': Threat.RARE,
                # 'Unknown': Threat.EMERGENCY,
                # 'Unknown': Threat.RARE,
                'Young Ron Weasley': Threat.MEDIUM
            },
            'Room of Requirement V': {
                # 'Unknown': Threat.SEVERE,
                'Angelina Johnson': Threat.MEDIUM,
                'Parvati Patil': Threat.HIGH,
                # 'Unknown': Threat.SEVERE,
                # 'Unknown': Threat.RARE
            },
            'Yule Ball Great Hall': {
                # 'Unknown': Threat.HIGH,
                # 'Unknown': Threat.HIGH,
                # 'Unknown': Threat.SEVERE,
                # 'Unknown': Threat.SEVERE,
                # 'Unknown': Threat.RARE
            },
            'Hogwarts Grounds': {
                # 'Unknown': Threat.HIGH,
                # 'Unknown': Threat.SEVERE,
                'Young Remus Lupin': Threat.SEVERE,
                # 'Unknown': Threat.HIGH,
                # 'Unknown': Threat.RARE
            }
        },
        'Ministry of Magic': {
            'Ministry Atrium': {
                'Ministry Official': Threat.LOW,
                'Flock of Interdepartmental Memos': Threat.MEDIUM,
                'Daily Prophet Stand': Threat.LOW,
                'Ministry Administrator': Threat.LOW,
                'Prophecy Record': Threat.LOW
            },
            'Ministry Atrium II': {
                'Bogrod': Threat.MEDIUM,
                # 'Unknown': Threat.SEVERE,
                # 'Unknown': Threat.SEVERE,
                # 'Unknown': Threat.RARE,
                # 'Unknown': Threat.EMERGENCY
            },
            'Courtroom Ten': {
                'Arthur Weasley': Threat.MEDIUM,
                # 'Unknown': Threat.RARE,
                # 'Unknown': Threat.RARE,
                'Nymphadora Tonks': Threat.HIGH,
                'Mad-Eye Moody': Threat.HIGH
            }
        },
        'Magizoology': {
            'Newt\'s Case': {
                'Young Graphorn': Threat.LOW,
                'Billywig': Threat.LOW,
                'Niffler': Threat.MEDIUM,
                'Baby Niffler': Threat.LOW,
                'Mooncalf': Threat.MEDIUM
            },
            'Central Park': {
                'Mountain Troll': Threat.HIGH,
                'Erumpent': Threat.MEDIUM,
                # 'Unknown': Threat.SEVERE,
                # 'Unknown': Threat.HIGH,
                # 'Unknown': Threat.RARE,
                'Branch of Bowtruckles': Threat.MEDIUM
            },
            'New York City Street': {
                # 'Unknown': Threat.RARE,
                'Newt Scamander': Threat.EMERGENCY,
                'Occamy Eggs': Threat.HIGH,
                # 'Unknown': Threat.SEVERE,
                # 'Unknown': Threat.RARE
            }
        },
        'Magical Games and Sports': {
            'World Cup Grounds': {
                'Magical Megaphone': Threat.LOW,
                'Quidditch World Cup': Threat.MEDIUM,
                'Chudley Cannons Player': Threat.LOW,
                'Gobstone Set': Threat.LOW,
                # 'Unknown': Threat.LOW
            },
            'Hogwarts Quidditch Pitch': {
                'Quidditch Pitch Stands': Threat.RARE,
                'Bludger': Threat.MEDIUM,
                'Beater\'s Bat': Threat.MEDIUM,
                'Golden Snitch': Threat.HIGH,
                'Quidditch Keeper Ron': Threat.SEVERE,
                'House of Exploding Snap Cards': Threat.MEDIUM
            },
            'Triwizard Maze': {
                'Nimbus 2000': Threat.HIGH,
                # 'Unknown': Threat.EMERGENCY,
                # 'Unknown': Threat.RARE,
                # 'Unknown': Threat.SEVERE,
                # 'Unknown': Threat.RARE
            },
            'Hogwarts Quidditch Stands': {
                # 'Unknown': Threat.HIGH,
                # 'Unknown': Threat.RARE,
                'Quidditch Tryouts Seamus Finnigan': Threat.MEDIUM,
                # 'Unknown': Threat.HIGH,
                # 'Unknown': Threat.SEVERE
            },
            'Hogwarts Quidditch Pitch II': {
                # 'Unknown': Threat.RARE,
                'Quidditch Captain Marcus Flint': Threat.MEDIUM,
                # 'Unknown': Threat.SEVERE,
                # 'Unknown': Threat.SEVERE,
                'Madam Hooch': Threat.HIGH
            }
        },
        'Mysterious Artefacts': {
            'Room of Requirement II': {
                'Quill of Acceptance and Book of Admittance': Threat.LOW,
                'Weasley Clock': Threat.LOW,
                'Remembrall': Threat.LOW,
                'Hagrid\'s Umbrella': Threat.LOW,
                'Decoy Detonators': Threat.MEDIUM
            },
            'Dumbledore\'s Office': {
                'Sword of Gryffindor': Threat.RARE,
                'Mirror of Erised': Threat.HIGH,
                'Pensieve': Threat.SEVERE,
                'Philosopher\'s Stone': Threat.SEVERE,
                'Dumbledore\'s Memory Cabinet': Threat.MEDIUM
            },
            'Room of Requirement III': {
                # 'Unknown': Threat.EMERGENCY,
                'Marauder\'s Map': Threat.MEDIUM,
                # 'Unknown': Threat.MEDIUM,
                # 'Unknown': Threat.RARE,
                # 'Unknown': Threat.RARE,
                'Mad-Eye Moody\'s Eye': Threat.HIGH
            }
        }
    }

    for family, pages in registry.items():
        for page, foundables in pages.items():
            for name, threat in foundables.items():
                foundable = Foundable.get_or_create(family=family, page=page, name=name, threat=threat)
                LOGGER.info(foundable)

if __name__ == '__main__':
    init_logger('The-Pensieve_Data')
    main()