#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Usage:
  sdf.py [push | pull | download | upload]

Options:
  -h --help         Show this screen.
  -V --version      Show version.
  -v --verbose      Show verbose info.(Not Implemented Yet!)
"""

from docopt import docopt
from sync_dotfiles import SyncDotfiles


if __name__ == '__main__':
    args = docopt(__doc__, version='Sync Dot Files 0.1')
    print(args)
    sync = SyncDotfiles()
    if args['download']:
        # sync.download_change()
        print('download')
    elif args['upload']:
        # sync.upload_change()
        print('upload')
    elif args['pull']:
        # sync.pull()
        print('pull')
    elif args['push']:
        # sync.push()
        print('push')
    else:
        print(__doc__)

