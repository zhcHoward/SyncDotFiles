#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Usage:
  sync_dotfiles.py [download | upload]

Options:
  -h --help         Show this screen.
  -V --version      Show version.
  -v --verbose      Show verbose info.(Not Implemented Yet!)
"""

from docopt import docopt
from sync_dotfiles import SyncDotfiles


if __name__ == '__main__':
    args = docopt(__doc__, version='Sync Dot Files 0.1')

    sync = SyncDotfiles()
    if args['download'] or not (args['download'] or args['upload']):
        sync.download_change()
        print('download')
    elif args['upload']:
        sync.upload_change()
        print('upload')
    else:
        print(__doc__)