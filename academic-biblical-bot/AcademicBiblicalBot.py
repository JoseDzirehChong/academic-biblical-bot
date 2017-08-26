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

#ID of already answered comments goes here
alreadyRespondedComments = 'PastComments.txt'

automatedResponse = """This is an automatic notification that your comment has been removed. Your comment was a top level comment, and unless you were hostile it is likely that your comment was removed for not meeting /r/AcademicBiblical's standards. Please check that you have provided academic sources, which are almost always necessary. Once you have edited your comment to comply with the rules, please contact a moderator to get your comment reapproved.

*I am a bot, bleep bloop. Contact my creator /u/JoseDzirehChong if there are any issues with this bot*. [Source code](https://github.com/JoseDzirehChong/academic-biblical-bot)"""

def authenticate():
    
    print('Authenticating...\n')
    reddit = praw.Reddit('AcademicBiblicalBot', user_agent = 'web:AcademicBiblicalBot:v0.1.0 (by /u/JoseDzirehChong)')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    
    return reddit

def find_duplicate_comments(comment_id):
    past_comments = open('PastComments.txt', 'r')
    comment_list = past_comments.readlines()
    past_comments.close()
    
    for line in comment_list:
        if str(comment_id) in line:
            return True
    return False


def run_bot(reddit):
    
    print("Getting 250 comments...\n")
    
    for comment in reddit.subreddit("ABBotTestSite").comments(limit = 250):

        if comment.parent_id == comment.link_id and find_duplicate_comments(comment.id) == False:
            print(comment.body)
            
            with open("PastComments.txt", "a") as myfile:
                myfile.write(comment.id + "\n")
            
            
def main():
    reddit = authenticate()
    while True:
        run_bot(reddit)
        
if __name__ == "__main__":
    main()