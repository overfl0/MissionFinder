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
    """Return the directory where missions are stored for the current Arma installation"""
    # TODO: This may have to be rewritten to not use os.getcwd but something more reliable
    #return r'D:\Steam\steamapps\common\Arma 3\MPMissions'
    return os.path.join(os.getcwd(), 'MPMissions')


def get_mission_metadata(filepath):
    """
    Open a PBO and fetch its metadata.
    Return the metadata contents if found.
    Return None otherwise.
    """

    f = PBOFile.read_file(filepath)

    try:
        entry = f['metadata.hpp']
        metadata = parse_classfile(entry.data.decode('utf-8'))
        return metadata

    except KeyError:
        return None

    return None


def filter_last_versions(all_missions):
    """
    Filter the given dictionary of missions.
    Return a dictionary of missions with only the latest version for each mission.
    Mission version is denoted by a BARENAME_v<version>.MAP.pbo format name.
    """

    filtered = {}
    for mission in all_missions:
        try:
            name_version = mission['filename'].split('.')[0]

            try:
                bare_name, ci_version = name_version.rsplit('_v', maxsplit=1)
                ci_version = int(ci_version)

            # Probably old-style mission names
            except:
                bare_name = name_version
                ci_version = 0

            # Update filtered if current version is higher than what we already have
            dummy_entry = {'CI_version': -1}
            existing_entry = filtered.get(bare_name, dummy_entry)
            if ci_version > existing_entry['CI_version']:
                filtered[bare_name] = mission
                filtered[bare_name]['CI_version'] = ci_version

        except:
            logger.error('Error while filtering mission: {}'.format(mission))

    return filtered



def convert_to_arma_types(arg):
    """
    Convert python variables to Arma SQF variables
    Tuple -> List
    Dict -> [[key, val], [key, val], ...]
    Everything_else -> Everything_else

    Return the converted value.
    """

    # Tuple or List: Convert to list
    if isinstance(arg, tuple) or isinstance(arg, list):
        return [convert_to_arma_types(element) for element in arg]

    # Dict: Convert to [[key, val], [key, val], ...]
    if isinstance(arg, dict):
        return [[convert_to_arma_types(key), convert_to_arma_types(arg[key])] for key in sorted(arg.keys())]

    # Everything else: return it
    return arg


def get_missions():
    """
    Return a SQF dict with available missions.
    """

    missions_dir = get_missions_dir()
    missions = []

    for filename in os.listdir(missions_dir):
        try:
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
            missions.append(mission_metadata)

            logger.info('Adding file: {}'.format(filename))

        except:
            logger.error('Something bad happened while analysing file: {}'.format(filename))

    return convert_to_arma_types(filter_last_versions(missions))
