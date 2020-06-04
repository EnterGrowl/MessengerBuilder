from builder import MessengerBuilder
from exporter import Export

import json
import os
import random
import re

regex = re.compile('.*?\.zip')
cwd = os.getcwd()

def _default(name):
    name = name.replace(' ', '')
    if name == 'f':
        name = 'MessengerBuilder{}.zip'.format(
            str(random.randrange(99999)))
    if not regex.match(name):
        name += '.zip'

    return name

def start():
    """Entry point to builder, get JSON and start building!"""
    try:
        with open('./store/messenger.json') as json_file:
            data = json.load(json_file)
            if not data:
                raise ValueError('missing messenger JSON from builder')
            if not os.environ['PORT']:
                raise ValueError('missing PORT number in ENV')
            port = os.environ['PORT']
            out = _default(port)
            mb = MessengerBuilder(data, port)
            err = mb.build()
            print(err)
            if err:
                raise SystemError('Build failed')
            exporter = Export(out, cwd, port)
            err = exporter.config()
            if err:
                raise SystemError('Build compression failed')
            print('Ok')
            return 0

    except Exception as e:
        print(e)
        raise e

if __name__ == '__main__':
    start()
