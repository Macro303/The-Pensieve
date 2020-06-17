#!/usr/bin/python3
import logging

from Data.Database import Foundable, Threat
from Logger import init_logger
from pony.orm import db_session

LOGGER = logging.getLogger(__name__)


@db_session
def main():
    create_foundables()


def create_foundables():
    registry = {
        'Care of Magical Creatures': {
            'Forbidden Forest': {
                'Baby Unicorn': {
                    'Threat': Threat.MEDIUM,
                    'Standard': 12
                },
                'Blast-Ended Skrewt': {
                    'Threat': Threat.MEDIUM,
                    'Standard': 12
                },
                'Dragon Egg': {
                    'Threat': Threat.MEDIUM,
                    'Standard': 12
                },
                'Firenze': {
                    'Threat': Threat.SEVERE,
                    'Standard': 5
                },
                'Hippogriff': {
                    'Threat': Threat.HIGH,
                    'Standard': 9
                },
                # 'Unknown': {
                #     'Threat': Threat.RARE,
                #     'Standard': 7
                # }
            },
            'Hagrid\'s Hut': {
                'Abraxian Winged Horse': {
                    'Threat': Threat.RARE,
                    'Standard': 7
                },
                'Baby Norwegian Ridgeback': {
                    'Threat': Threat.HIGH,
                    'Standard': 9
                },
                'Buckbeak': {
                    'Threat': Threat.SEVERE,
                    'Standard': 5
                },
                'Rubeus Hagrid': {
                    'Threat': Threat.EMERGENCY,
                    'Standard': 1
                },
                # 'Unknown': {
                #     'Threat': Threat.RARE,
                #     'Standard': 7
                # }
            },
            'Pumpkin Patch': {
                'Acromantula Eggs': {
                    'Threat': Threat.LOW,
                    'Standard': 15
                },
                'Baby Hippogriff': {
                    'Threat': Threat.LOW,
                    'Standard': 15
                },
                'Flobberwurm': {
                    'Threat': Threat.LOW,
                    'Standard': 15
                },
                'Kneazle': {
                    'Threat': Threat.LOW,
                    'Standard': 15
                },
                'Monster Book of Monsters': {
                    'Threat': Threat.MEDIUM,
                    'Standard': 12
                }
            }
        },
        'Dark Arts': {
            'Borgin & Burkes': {
                'Flesh-Eating Slugs': {
                    'Threat': Threat.LOW,
                    'Standard': 15
                },
                'Hand of Glory': {
                    'Threat': Threat.LOW,
                    'Standard': 15
                },
                'Magick Moste Evile': {
                    'Threat': Threat.LOW,
                    'Standard': 15
                },
                'Vanishing Cabinet': {
                    'Threat': Threat.MEDIUM,
                    'Standard': 12
                },
                'Wanted Poster of an Azkaban Escapee': {
                    'Threat': Threat.LOW,
                    'Standard': 15
                }
            },
            'Fallen Ministry Atrium': {
                'Portrait of Voldemort': {
                    'Threat': Threat.HIGH,
                    'Standard': 9
                },
                # 'Unknown': {
                #     'Threat': Threat.RARE,
                #     'Standard': 7
                # },
                # 'Unknown': {
                #     'Threat': Threat.RARE,
                #     'Standard': 7
                # },
                # 'Unknown': {
                #     'Threat': Threat.SEVERE,
                #     'Standard': 5
                # },
                # 'Unknown': {
                #     'Threat': Threat.EMERGENCY,
                #     'Standard': 3
                # }
            },
            'Knockturn Alley': {
                'Hag': {
                    'Threat': Threat.MEDIUM,
                    'Standard': 12
                },
                'Ministry Executioner': {
                    'Threat': Threat.MEDIUM,
                    'Standard': 12
                },
                'Portrait of Bellatrix Lestrange': {
                    'Threat': Threat.MEDIUM,
                    'Standard': 12
                },
                'Thestral': {
                    'Threat': Threat.HIGH,
                    'Standard': 9
                },
                # 'Unknown': {
                #     'Threat': Threat.RARE,
                #     'Standard': 7
                # },
                # 'Unknown': {
                #     'Threat': Threat.SEVERE,
                #     'Standard': 5
                # }
            }
        },
        'Hogwarts School': {
            'DADA Classroom': {
                'Boggart Cabinet': {
                    'Threat': Threat.MEDIUM,
                    'Standard': 12
                },
                'Gryffindor Student': {
                    'Threat': Threat.LOW,
                    'Standard': 15
                },
                'Hufflepuff Student': {
                    'Threat': Threat.LOW,
                    'Standard': 15
                },
                'Ravenclaw Student': {
                    'Threat': Threat.LOW,
                    'Standard': 15
                },
                'Slytherin Student': {
                    'Threat': Threat.LOW,
                    'Standard': 15
                }
            },
            'Great Hall': {
                'Owl Lecturn': {
                    'Threat': Threat.RARE,
                    'Standard': 7
                },
                'Portrait of Albus Dumbledore': {
                    'Threat': Threat.MEDIUM,
                    'Standard': 12
                },
                # 'Unknown': {
                #     'Threat': Threat.RARE,
                #     'Standard': 7
                # },
                # 'Unknown': {
                #     'Threat': Threat.SEVERE,
                #     'Standard': 5
                # },
                # 'Unknown': {
                #     'Threat': Threat.SEVERE,
                #     'Standard': 5
                # }
            },
            'Moving Staircases': {
                'Moaning Myrtle': {
                    'Threat': Threat.HIGH,
                    'Standard': 9
                },
                'Peeves': {
                    'Threat': Threat.HIGH,
                    'Standard': 9
                },
                'Pomona Sprout': {
                    'Threat': Threat.MEDIUM,
                    'Standard': 12
                },
                'Professor Flitwick': {
                    'Threat': Threat.MEDIUM,
                    'Standard': 12
                },
                # 'Unknown': {
                #     'Threat': Threat.RARE,
                #     'Standard': 7
                # },
                # 'Unknown': {
                #     'Threat': Threat.EMERGENCY,
                #     'Standard': 3
                # }
            },
            'Moving Staircases II': {
                'Portrait of Godric Gryffindor': {
                    'Threat': Threat.HIGH,
                    'Standard': 9
                },
                'Portrait of Rowena Ravenclaw': {
                    'Threat': Threat.HIGH,
                    'Standard': 9
                },
                # 'Unknown': {
                #     'Threat': Threat.HIGH,
                #     'Standard': 9
                # },
                # 'Unknown': {
                #     'Threat': Threat.HIGH,
                #     'Standard': 9
                # },
                # 'Unknown': {
                #     'Threat': Threat.RARE,
                #     'Standard': 7
                # }
            }
        },
        'Legends of Hogwarts': {
            'Chess Chamber': {
                # 'Unknown': {
                #     'Threat': Threat.EMERGENCY,
                #     'Standard': 3
                # },
                # 'Unknown': {
                #     'Threat': Threat.SEVERE,
                #     'Standard': 5
                # },
                # 'Unknown': {
                #     'Threat': Threat.RARE,
                #     'Standard': 7
                # },
                # 'Unknown': {
                #     'Threat': Threat.RARE,
                #     'Standard': 7
                # },
                'Young Ron Weasley': {
                    'Threat': Threat.MEDIUM,
                    'Standard': 12
                }
            },
            'Hogwarts Grounds': {
                # 'Unknown': {
                #     'Threat': Threat.HIGH,
                #     'Standard': 9
                # },
                # 'Unknown': {
                #     'Threat': Threat.RARE,
                #     'Standard': 7
                # },
                # 'Unknown': {
                #     'Threat': Threat.SEVERE,
                #     'Standard': 5
                # },
                'Young Peter Pettigrew': {
                    'Threat': Threat.HIGH,
                    'Standard': 9
                },
                'Young Remus Lupin': {
                    'Threat': Threat.SEVERE,
                    'Standard': 5
                }
            },
            'Potions Classroom': {
                'Hedwig': {
                    'Threat': Threat.LOW,
                    'Standard': 15
                },
                'Professor Snape': {
                    'Threat': Threat.HIGH,
                    'Standard': 9
                },
                # 'Unknown': {
                #     'Threat': Threat.HIGH,
                #     'Standard': 9
                # },
                # 'Unknown': {
                #     'Threat': Threat.RARE,
                #     'Standard': 7
                # },
                'Young Harry Potter': {
                    'Threat': Threat.SEVERE,
                    'Standard': 5
                }
            },
            'Room of Requirements I': {
                'Filch and Mrs. Norris': Threat.LOW,
                # 'Unknown': Threat.MEDIUM,
                'Young Ginny Weasley': Threat.MEDIUM,
                'Young Luna Lovegood': Threat.MEDIUM,
                'Dumbledore\'s Army Dueling Dummy': Threat.LOW,
                'Weasley Fireworks': Threat.LOW
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
