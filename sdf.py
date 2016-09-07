#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Usage:
    sdf.py [download | upload | push | pull | update_local | update_cache]

Options:
    pull                git pull or clone, depends on cache files exists or not.
    push                git add -> git commit -> git push
    update_local        use cache files to update local dotfiles
    update_cache        use local files to update cache dotfiles
    download            first pull then update locals
    upload              first update_cache then push

    -h --help           Show this screen.
    -V --version        Show version.
    -v --verbose        Show verbose info.(Not Implemented Yet!)
"""

from docopt import docopt
from sync_dotfiles import SyncDotfiles


if __name__ == '__main__':
    args = docopt(__doc__, version='Sync Dot Files 0.1')

    sync = SyncDotfiles()
    if args['download']:
        print('download')
        sync.download_change()
    elif args['upload']:
        print('upload')
        sync.upload_change()
    elif args['pull']:
        print('pull')
        sync.pull()
    elif args['push']:
        print('push')
        sync.push()
    elif args['update_local']:
        print('update_local')
        sync.update_local()
    elif args['update_cache']:
        print('update_cache')
        sync.update_cache()
    else:
        print(__doc__)

