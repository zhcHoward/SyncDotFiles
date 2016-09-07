# SyncDotFiles
A small program for sync all my configs(vim, tmux, zsh ...)

## What is SyncDotFiles
SyncDotFiles is a simple python console program for synchronizing all your dotfiles.

## How to use
1. Go to project root directory
2. Install required python packages:
`pip3 install -r requirements.txt`
This program only tested under Python3. Make sure you have Python3 installed on your machine.
3. Application Configuration
It is recommanded that rename the default_settings.json to settings.json and add your custom settings only in settings.json. Since default_settings.json may be overwrited.
Do change the 'git_repo' line to your own git repository, otherwise, this program will try to clone my git repository which will certainly fail because that is a private repositoy.
4. Git Configuration
Make sure you can connect your git repository via ssh not https and when you run command `git pull` or `git push`, you won't be asked to enter password. This is because git is called inside python, the line which ask you to input the password won't show up in the console, you have no way to input your password and the whole process will fail.
I am trying to find a way to solve this problem.
5. Run Application
You can run this program by:
`python3 sdf.py download`
sdf.py defines the console interface for this program
If you want to see other options, you can try:
`python3 sdf.py -h`
