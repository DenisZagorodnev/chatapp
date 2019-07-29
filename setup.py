#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 14:42:02 2019

@author: deniszagorodnev
"""

from setuptools import setup

APP = ['main.py']
DATA_FILES = ['message.png']
#'find_usr.py', 'sql.py', 'start_page.py', 'usr_page.py' 
APP_NAME = "ChatApp"
OPTIONS = {
    'argv_emulation': True,
    'includes': ('find_usr', 'sql', 'sys', 'usr_page', 'start_page', 'PyQt5', 'mysql', 'sip'),
    'iconfile': 'message.icns'
}

setup(
    name=APP_NAME,
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)