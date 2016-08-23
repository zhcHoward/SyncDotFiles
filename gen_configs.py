#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import git
import shutil
import json


class Config():
    username = os.environ['USER']
    home = os.path.join('/home/', username)
    bakup_extension = '.bak'
    base_dir = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        # init configs
        # TODO load personal configs
        with open(os.path.join(self.base_dir, 'default_configs.json')) as reader:
            self.configs = json.load(reader)

    def is_first_time(self):
        if os.path.isfile(os.path.join(self.base_dir, 'last_update.txt')):
            return True
        else:
            return False

    def upload_change(self):
        self.generate_changes()
        # git commit/push

    def download_change(self):
        # git pull
        self.update_local()

    def generate_changes(self):
        for app, config in self.configs.items():
            for conf_file in config['files']:
                if os.path.isabs(conf_file):
                    local_path = conf_file
                    conf_file = os.path.basename(config_file)
                else:
                    local_path = os.path.join(self.home, conf_file)
                repo_path = os.path.join(self.base_dir, app, conf_file)

                try:
                    shutil.copy(local_path, repo_path)
                except FileNotFoundError:
                    os.mkdir(os.path.dirname(repo_path))
                    shutil.copy2(local_path, repo_path)


if __name__ == '__main__':
    c = Config()
    c.generate_changes()

# class VimConfig(Config):
#     _file = os.path.join(self._base_path, '.vimrc')
#     _file_bak = os.path.join(self._base_path, '.vimrc.bak')
#     _folder = os.path.join(self._base_path, '.vim')
#     _folder_bak = os.path.join(self._base_path, '.vim.bak')

#     def check_old_configs(self):
#         vim_config_file = self._vim_config_file
#         vim_config_file_bak = os.path.join(self._base_path, '.vimrc.bak')
#         if os.path.isfile(vim_config_file):
#             os.rename(vim_config_file, vim_config_file_bak)
#         if os.path.exists(self._vim_config_folder):
#             os.rename(self._vim_config_folder, self._folder_bak)

#     def write_new_configs(self):
#         pass

