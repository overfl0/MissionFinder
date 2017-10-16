# Test if pythia is working
# hint str(["pythia.test"] call py3_fnc_callExtension)

# Run the function:
# hint str(["python.MissionFinder.get_missions"] call py3_fnc_callExtension)

import logging
import os

from yapbol import PBOFile
from .dummy_parser import parse_classfile


logger = logging.getLogger(__name__)

def get_missions_dir():
    #return r'D:\Steam\steamapps\common\Arma 3\MPMissions'
    return os.path.join(os.getcwd(), 'MPMissions')


def get_mission_metadata(filepath):
    #print('Loading file: {}'.format(filepath))
    f = PBOFile.read_file(filepath)

    try:
        entry = f['metadata.hpp']
        metadata = parse_classfile(entry.data.decode('utf-8'))
        return metadata

    except KeyError:
        return None

    return None


def get_missions():
    missions_dir = get_missions_dir()
    missions = []

    for filename in os.listdir(missions_dir):
        filepath = os.path.join(missions_dir, filename)

        if not os.path.isfile(filepath):
            continue

        if not filename.endswith('.pbo'):
            continue

        if not filename.startswith('FL_') and not filename.startswith('DFL_'):
            continue

        mission_metadata = get_mission_metadata(filepath)
        if not mission_metadata:
            continue

        mission_metadata['filename'] = filename
        entry = [[key, val] for key, val in mission_metadata.items()]
        missions.append(entry)

        logger.info('Adding file: {}'.format(filename))

    return missions
