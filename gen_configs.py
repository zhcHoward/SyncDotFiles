#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import git
import shutil
import json
import platform


class Config():
    local_home = os.path.join('/home/', os.environ['USER'])
    bakup_extension = '.bak'
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if platform.system() == 'Linux':
        cache_home = os.path.join(local_home, '.my-configs')
    elif platform.system() == 'Windowns':
        cache_home = 'd:\\my-configs'  # TODO change to \User folder
    else:
        cache_home = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        # init configs
        try:
            with open(os.path.join(self.base_dir, 'settings.json')) as reader:
                self.settings = json.load(reader)
            if not self.settings:
                with open(os.path.join(self.base_dir, 'default_settings.json')) as reader:
                    self.settings = json.load(reader)
        except FileNotFoundError:
            with open(os.path.join(self.base_dir, 'default_settings.json')) as reader:
                self.settings = json.load(reader)

    def is_first_time(self):
        if os.path.isfile(os.path.join(self.base_dir, 'last_update.txt')):
            return True
        else:
            return False

    def upload_change(self):
        self.generate_changes()
        # git commit/push

    def download_change(self):
        # create dir for remote files
        # git pull
        self.update_local()

    def read_config(self, config_path, app, is_dir=False):
        config_path = os.path.normpath(config_path)

        if os.path.isabs(config_path):
            local_path = config_path
            base_name = os.path.basename(config_path)
        else:
            local_path = os.path.join(self.local_home, config_path)
            base_name = config_path
        cache_path = os.path.join(self.cache_home, app, base_name)

        if not os.path.exists(local_path):
            raise FileNotFoundError('local config file/folder cannot be found')
        print(local_path, cache_path)
        if not os.path.exists(cache_path):
            if not is_dir:
                os.makedirs(os.path.dirname(cache_path))

        return local_path, cache_path

    def generate_changes(self):
        settings = self.settings['local']['configs']
        for app, config in settings.items():
            for conf_path in config['files']:
                local_path, cache_path = self.read_config(conf_path, app)
                shutil.copy2(local_path, cache_path)
            for conf_path in config['folders']:
                local_path, cache_path = self.read_config(conf_path, app, True)
                if os.path.exists(cache_path):
                    shutil.rmtree(cache_path)
                shutil.copytree(local_path, cache_path)

    def update_local(self):
        cache_settings = self.settings['cache']
        for app, config in cache_settings['configs']:


if __name__ == '__main__':
    c = Config()
    c.generate_changes()
