#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sh
import shutil
import json
import platform
import datetime


class SyncDotfiles():
    def __init__(self):
        # init configs
        self.bakup_extension = '.bak'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            with open(os.path.join(base_dir, 'settings.json')) as reader:
                self.settings = json.load(reader)
        except FileNotFoundError:
            with open(os.path.join(base_dir, 'default_settings.json')) as reader:
                self.settings = json.load(reader)
        else:
            if not self.settings:
                with open(os.path.join(base_dir, 'default_settings.json')) as reader:
                    self.settings = json.load(reader)

        self.local_home = self.settings['local']['home']
        self.cache_base = self.settings['cache']['base']
        self.cache_home = os.path.join(self.cache_base, '.mydotfiles')
        self.git = sh.git.bake(_cwd=self.cache_home)

    def upload_change(self):
        self.update_cache()
        self.push()

    def download_change(self):
        self.pull()
        self.update_local()

    def push(self):
        # git add->commit->push
        self.git.add('-A')
        now = datetime.datetime.now()
        self.git.commit("-m '{}'".format(now))
        self.git.push()

    def pull(self):
        """git pull
        If the cache_home does not exist, this function will clone
        the git repository defined in your setting file.
        """
        if not os.path.exists(self.cache_home):
            if not os.path.exists(self.cache_base):
                os.makedirs(self.cache_base, exist_ok=True)
            sh.git.clone(self.settings['git_repo'], _cwd=self.cache_base)
        else:
            self.git.pull()

    def update_cache(self):
        """Using local dotfiles to update files in the cache.
        If cache files exists, old files will be directly deleted.
        No '.bak' files in local cache since all versions of files are stored on git.
        """
        for app, config in self.settings['configs'].items():
            for path in config['paths']:
                local_path, cache_path = self.get_paths(app, path)
                self.check_src_and_dst(local_path, cache_path)
                if os.path.isdir(local_path):
                    shutil.rmtree(cache_path)
                    shutil.copytree(local_path, cache_path)
                else:
                    shutil.copy2(local_path, cache_path)

    def update_local(self):
        """Using dotfiles in cache to update local dotfiles
        If local files exists, old files will be renamed to 'name.bak' first.
        If 'name.bak' exists, the old '.bak' file will be directly deleted
        """
        for app, config in self.settings['configs'].items():
            for path in config['paths']:
                local_path, cache_path = self.get_paths(app, path)
                self.check_src_and_dst(cache_path, local_path)

                try:
                    if os.path.exists(local_path):
                        os.rename(local_path, local_path + self.bakup_extension)
                except OSError:
                    shutil.rmtree(local_path + self.bakup_extension)
                    os.rename(local_path, local_path + self.bakup_extension)

                if os.path.isdir(cache_path):
                    shutil.copytree(cache_path, local_path)
                else:
                    shutil.copy2(cache_path, local_path)

    def get_paths(self, app, path):
        """Generate path of local and cache from path in configs."""
        path = os.path.normpath(path)

        if os.path.isabs(path):
            local_path = path
            base_name = os.path.basename(path)
        else:
            local_path = os.path.join(self.local_home, path)
            base_name = path
        cache_path = os.path.join(self.cache_home, app, base_name)

        print(local_path, cache_path)
        return local_path, cache_path

    def check_src_and_dst(self, src, dst):
        """This function checks:
        1. The source(src) path exists or not.
           If source does not exist, a FileNotFoundError will be raised.
        2. The destination(dst) path exists or not.
           If destination does not exists, the path to its parent folder will be created, no matter
           its parent folder exists or not.
        """
        if not os.path.exists(src):
            raise FileNotFoundError('source file/folder "{}" cannot be found'.format(src))

        if not os.path.exists(dst):
            os.makedirs(os.path.dirname(dst), exist_ok=True)

