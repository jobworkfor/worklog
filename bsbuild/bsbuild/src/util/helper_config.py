from configparser import ConfigParser
from src.util.helper_log import Log

_ = (Log)


class ConfigHelper(object):
    def __init__(self, path):
        self.configPath = path
        self.configParser = ConfigParser()
        self.configParser.read(path)
        pass

    def items(self, section):
        '''
        RawConfigParser.items(section)
            Return a list of (name, value) pairs for each option in the given section.
        '''
        items = None
        if self.configParser.has_section(section):
            items = self.configParser.items(section)
        return items

    def save(self, section, dict):
        self.configParser.remove_section(section)
        self.configParser.add_section(section)
        for key in dict.keys():
            self.configParser.set(section, key, dict[key])

        with open(self.configPath, 'w') as f:
            self.configParser.write(f)
