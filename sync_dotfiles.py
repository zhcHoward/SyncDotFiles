#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sh
import shutil
import json
import platform
import datetime


class SyncDotfiles():
    # TODO
    # if platform.system() == 'Linux':
    #     cache_home = os.path.join(local_home, '.mydotfiles')
    # elif platform.system() == 'Windowns':
    #     cache_home = 'd:\\my-configs'  # TODO change to \User folder
    # else:
    #     cache_home = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        # init configs
        self.bakup_extension = '.bak'
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            with open(os.path.join(self.base_dir, 'settings.json')) as reader:
                self.settings = json.load(reader)
            if not self.settings:
                with open(os.path.join(self.base_dir, 'default_settings.json')) as reader:
                    self.settings = json.load(reader)
        except FileNotFoundError:
            with open(os.path.join(self.base_dir, 'default_settings.json')) as reader:
                self.settings = json.load(reader)

        self.local_home = self.settings['local']['home']
        self.cache_base = self.settings['cache']['base']
        self.cache_home = os.path.join(self.cache_base, '.mydotfiles')
        self.git = sh.git.bake(_cwd=self.cache_home)

    def upload_change(self):
        self.update_cache()
        self.push()

    def push(self):
        # git add->commit->push
        self.git.add('-A')
        now = datetime.datetime.now()
        self.git.commit("-m '{}'".format(now))
        self.git.push()

    def download_change(self):
        self.pull()
        self.update_local()

    def pull(self):
        # create dir for remote files
        # git pull
        if not os.path.exists(self.cache_home):
            if not os.path.exists(self.cache_base):
                os.makedirs(self.cache_base, exist_ok=True)
            sh.git.clone(self.settings['remote']['git_repo'], _cwd=self.cache_base)
        else:
            self.git.pull()

    def read_config(self, config_path, app, is_dir=False):
        config_path = os.path.normpath(config_path)

        if os.path.isabs(config_path):
            local_path = config_path
            base_name = os.path.basename(config_path)
        else:
            local_path = os.path.join(self.local_home, config_path)
            base_name = config_path
        cache_path = os.path.join(self.cache_home, app, base_name)

        print(local_path, cache_path)
        if not os.path.exists(local_path):
            raise FileNotFoundError('local config file/folder cannot be found')

        if not os.path.exists(cache_path):
            if not is_dir:
                os.makedirs(os.path.dirname(cache_path), exist_ok=True)

        return local_path, cache_path

    def update_cache(self):
        for app, config in self.settings['configs'].items():
            for conf_path in config['files']:
                local_path, cache_path = self.read_config(conf_path, app)
                shutil.copy2(local_path, cache_path)
            for conf_path in config['folders']:
                local_path, cache_path = self.read_config(conf_path, app, True)
                if os.path.exists(cache_path):
                    shutil.rmtree(cache_path)
                shutil.copytree(local_path, cache_path)

    def update_local(self):
        for app, config in self.settings['configs'].items():
            for config_path in config['files']:
                source_path = os.path.join(self.cache_home, app, config_path)
                target_path = os.path.join(self.local_home, config_path)
                if os.path.exists(target_path):
                    os.rename(target_path, target_path + self.bakup_extension)
                if not os.path.exists(target_path):
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                shutil.copy2(source_path, target_path)
            for config_path in config['folders']:
                config_path = os.path.normpath(config_path)
                source_path = os.path.join(self.cache_home, app, config_path)
                target_path = os.path.join(self.local_home, config_path)
                if os.path.exists(target_path):
                    #os.rename(target_path, target_path + self.bakup_extension)
                    os.renames(source_path, target_path + self.bakup_extension)
                if not os.path.exists(target_path):
                    os.makedirs(target_path, exist_ok=False)
                shutil.copytree(source_path, target_path)

