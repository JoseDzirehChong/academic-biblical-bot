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

#TODO
    #Give code a quick read before releasing it
    #Update 40 second age limit of comment to "minimum_comment_age"
    #Change the intervals of time between when this bot is run
    #Find a server to host this bot
    #Check if POSIX time works with DST transitions
    #Point bot towards AcademicBiblical
    
#ID of already answered comments goes here
alreadyRespondedComments = 'PastComments.txt'
automatedResponse = """This is an automatic notification that your comment has been removed. Your comment was a top level comment, and unless you were hostile it is likely that your comment was removed for not meeting /r/AcademicBiblical's standards. Please check that you have provided academic sources, which are almost always necessary. Once you have edited your comment to comply with the rules, please contact a moderator to get your comment reapproved.

*I am a bot, bleep bloop. Contact my creator /u/JoseDzirehChong if there are any issues with this bot. [Source code](https://github.com/JoseDzirehChong/academic-biblical-bot)*"""

comment_batch_size = 250
minimum_comment_age = 1209600
subreddit_to_check = "ABBotTestSite"

def authenticate(): #get reddit instance
    
    print('Authenticating...\n')
    reddit = praw.Reddit('AcademicBiblicalBot', user_agent = 'web:AcademicBiblicalBot:v0.1.0 (by /u/JoseDzirehChong)')
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
    if reddit.comment(comment_id).banned_by == None:
        return False
    else:
        return True

def run_bot(reddit): #evaluates batches of comments (max batch size is 250 comments)
    
    print("Getting {} comments...\n".format(comment_batch_size))
    
    for comment in reddit.subreddit(subreddit_to_check).comments(limit = comment_batch_size):
        
        now = time.time()
        creation = comment.created_utc
        age = now - creation

        conditions = comment.parent_id == comment.link_id and find_duplicate_comments(comment.id) == False and age < minimum_comment_age
        
        if conditions:
            
            if check_if_removed(reddit, comment.id) == True:
                print(comment.body + "(removed)")
                to_distinguish = comment.reply(automatedResponse)
                to_distinguish.mod.distinguish(sticky=False)
                save_id(comment)
                
            elif check_if_removed(reddit, comment.id) == False:
                print(comment.body + "(not_removed)")
            
        elif not conditions:
            pass
        
        else:
            print("Ya messed up the code, bucko")
            
            
def main():
    reddit = authenticate() #get the reddit instance
    while True:
        assert os.path.exists('praw.ini')
        assert os.path.exists('PastComments.txt')
        run_bot(reddit) #use reddit instance to run bot whenever program is active
        time.sleep(10) #to make sure I don't burn computer resources
        
if __name__ == "__main__":
    main()