"""Functions for reading and writing task configurations to disk."""
import ConfigParser
import os.path

def get_config(filename):
    """Get a task config object from the filename.
    :param filename: the file to read for the config. Understands ~.
    :returns: a ConfigParser object containing the config in the file"""
    cfg = ConfigParser.ConfigParser()
    cfg.read(os.path.expanduser(filename))
    return cfg

def write_default_config(filename):
    """Write a sane default config to a file.
    :param filename: the file to write the config to. Understands ~."""
    cfg = ConfigParser.ConfigParser()
    cfg.add_section('database')
    cfg.set('database', 'storage_path', os.path.expanduser('~/.jacktask/storage'))

    with open(os.path.expanduser(filename), 'wb') as f:
        cfg.write(f)
