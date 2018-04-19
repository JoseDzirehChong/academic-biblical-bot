#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on August 24 20:04 2017

@author: Jose Dzireh Chong
"""

#imports
import praw
import time
import os
from datetime import datetime
import calendar

#TODO
    #Give code a quick read before releasing it
    #Find a server to host this bot
    #Check if POSIX time works with DST transitions
    #Test a final time
    
#ID of already answered comments goes here
alreadyRespondedComments = 'PastComments.txt'
automatedResponse = """This is an automatic notification that your comment has been removed. Your comment was a top level comment, and unless you were hostile it is likely that your comment was removed for not meeting /r/AcademicBiblical's standards. Please check that you have provided academic sources, which are almost always necessary. Once you have edited your comment to comply with the rules, please contact a moderator to get your comment reapproved.

*I am a bot, bleep bloop. Contact my creator /u/JoseDzirehChong if there are any issues with this bot. [Source code](https://github.com/JoseDzirehChong/academic-biblical-bot)*"""

test_conditions = True

comment_batch_size = 250
minimum_comment_age = 1209600
subreddit_to_check = "AcademicBiblical"

if test_conditions:
    comment_batch_size = 10
    minimum_comment_age = 180
    subreddit_to_check = "ABBotTestSite"
    
def authenticate(): #get reddit instance
    
    print('Authenticating...\n')
    reddit = praw.Reddit('AcademicBiblicalBot', user_agent = 'web:AcademicBiblicalBot:v1.0.0 (by /u/JoseDzirehChong)')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    
    return reddit

def find_duplicate_comments(comment_id): #check if comment has been evaluated before
    past_comments = open(alreadyRespondedComments, 'r')
    comment_list = past_comments.readlines()
    past_comments.close()
    
    for line in comment_list:
        if str(comment_id) in line:
            return True
    return False

def save_id(comment): #add current comment to list of already evaluated comment
    with open(alreadyRespondedComments, "a") as myfile:
                myfile.write(comment.id + "\n")
                
def check_if_removed(reddit, comment_id):
    return reddit.comment(comment_id).banned_by is not None
    
def UTC_to_posix(timestamp):
    posix = calendar.timegm(timestamp.utctimetuple())
    return posix

def get_age(comment):
    now_posix = time.time() #working
    creation = datetime.utcfromtimestamp(comment.created_utc) #working
    creation_posix = UTC_to_posix(creation)
        
    print(str(now_posix) + " now") #working
    print(str(creation_posix) + " created")
    
    age = now_posix - creation_posix
        
    return age

def respond_if_removed(comment):
    print(comment.body + "(removed)")
    to_distinguish = comment.reply(automatedResponse)
    to_distinguish.mod.distinguish(sticky=False)
    save_id(comment)
        
def run_bot(reddit): #evaluates batches of comments (max batch size is 250 comments)
    
    print("Getting {} comments...\n".format(comment_batch_size))
    
    for comment in reddit.subreddit(subreddit_to_check).comments(limit = comment_batch_size):
        
        ageVar = get_age(comment)
        
        conditions = comment.parent_id == comment.link_id and find_duplicate_comments(comment.id) == False and ageVar < minimum_comment_age
        
        if conditions:
            
            if check_if_removed(reddit, comment.id):
                respond_if_removed(comment)
                
            else:
                print(comment.body + "(not_removed)")
            
            
def main():
    reddit = authenticate() #get the reddit instance
    while True:
        assert os.path.exists('praw.ini')
        assert os.path.exists('PastComments.txt')
        run_bot(reddit) #use reddit instance to run bot whenever program is active
        time.sleep(30) #to make sure I don't burn computer resources
        
if __name__ == "__main__":
    main()
