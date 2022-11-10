import os
import zipfile
from zipfile import ZipFile

from src.util.helper_log import Log

_ = (Log)

all_commands = {}

my_dir = os.path.dirname(__file__)
rootDir = my_dir[:-len(__name__) - 1]


def _importCmd(py):
    if py.endswith('.py'):
        name = py[:-3]
    else:
        return
    clsn = name.capitalize()
    while clsn.find('_') > 0:
        h = clsn.index('_')
        clsn = clsn[0:h] + clsn[h + 1:].capitalize()

    mod = __import__(__name__,
                     globals(),
                     locals(),
                     ['%s' % name])
    mod = getattr(mod, name)
    try:
        cmd = getattr(mod, clsn)()
    except AttributeError:
        raise SyntaxError('%s/%s does not define class %s' % (
            __name__, py, clsn))

    name = name.replace('_', '-')
    cmd.NAME = name
    all_commands[name] = cmd
    return


def _loadCmdsFromFile():
    for py in os.listdir(my_dir):
        if py == '__init__.py':
            continue

        _importCmd(py)
    return


def _loadCmdsFromZip():
    pathPrefix = my_dir[len(rootDir) + 1:]
    with ZipFile(rootDir, 'r') as zipObj:
        # Get list of files names in zip
        listOfiles = zipObj.namelist()
        # Iterate over the list of file names in given list & print them
        for py in listOfiles:
            if pathPrefix in py:
                py = py[len(pathPrefix) + 1:]
                if '/' in py:
                    continue
                if py == '__init__.py':
                    continue
                if len(py) == 0:
                    continue

                _importCmd(py)
    return


if zipfile.is_zipfile(rootDir):
    _loadCmdsFromZip()
else:
    _loadCmdsFromFile()

if 'help' in all_commands:
    all_commands['help'].commands = all_commands

for c in all_commands:
    Log.d("support command:", c)
