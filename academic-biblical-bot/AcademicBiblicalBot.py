#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on August 24 20:04 2017

@author: Jose Dzireh Chong
"""

#imports
import praw
import time
import re
import requests
import bs4
import os

assert os.path.exists('praw.ini')

#ID of already answered comments go here
alreadyRespondedComments = '/Users/clarence/Desktop/Jose/AcademicBiblicalBot/PastComments.txt'

automatedResponse = """This is an automatic notification that your comment has been removed. If your comment was a top-level response to the question in the OP and not an insult, troll etc., it is likely that your comment was removed for not meeting /r/AcademicBiblical's standards. Please check that you have provided academic sources, which are almost always necessary. Once you have edited your comment to comply with the rules, please contact a moderator to get your comment reapproved.

*I am a bot, bleep bloop. Contact my creator /u/JoseDzirehChong if there are any issues with this bot*. [Source code]()"""

def authenticate():
    
    print('Authenticating...\n')
    reddit = praw.Reddit('AcademicBiblicalBot', user_agent = 'web:AcademicBiblicalBot:v0.1.0 (by /u/JoseDzirehChong)')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit

authenticate()