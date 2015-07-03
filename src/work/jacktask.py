#!/usr/bin/env python

import jacktask.task_config
from jacktask.commands import Command
from jacktask.db import Database

import sys
import json

if __name__ == '__main__':
    CONFIG_PATH = '~/.jacktask/config'

    config = jacktask.task_config.get_config(CONFIG_PATH)
    db = Database(config.get('database','storage_path'))

    command = sys.argv[1]
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    print 'args:',args
    cmd = Command(config, db)
    run_command = getattr(cmd, command)
    run_command(**args)
