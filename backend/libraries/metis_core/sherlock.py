import requests
# -*- coding: utf-8 -*-

import re
import csv
import datetime
import re
import json
import time
import sys
import calendar
from collections import Counter
from itertools import groupby


import pytz

from subreddits import subreddits_dict, ignore_text_subs, default_subs

class Post(object):
    def __init__(self, id, subreddit, text, created_utc, score, permalink, gilded):
        self.id = id
        self.subreddit = subreddit
        self.text = text
        self.created_utc = created_utc
        self.score = score
        self.permalink = permalink
        self.gilded = gilded
        

class Comment(Post):
    def __init__(self, id, subreddit, text, created_utc, score, permalink, submission_id, edited, top_level, gilded):
        super(Comment, self).__init__(
            id, subreddit, text, created_utc, score, permalink, gilded
        )
        self.submission_id = submission_id
        self.edited = edited
        self.top_level = top_level

class Submission(Post):
    """
    A class for submissions derived from Post.

    """

    def __init__(self, id, subreddit, text, created_utc, score, permalink, url, title, is_self, gilded, domain):
        super(Submission, self).__init__(
            id, subreddit, text, created_utc, score, permalink, gilded
        )
        # Submission link URL
        self.url = url
        # Submission title
        self.title = title
        # Self post?
        self.is_self = is_self
        # Domain
        self.domain = domain
        

import time
# Borrowed from https://github.com/orionmelt/sherlock
def get_comments(username,headers,limit=None):
    s = time.time()
    """
    Returns a list of redditor's comments.
    """
    comments = []
    more_comments = True
    after = None
    base_url = f"http://www.reddit.com/user/{username}/comments/.json?limit=100"
    url = base_url
    while more_comments:
        q = time.time()
        response = requests.get(url, headers=headers)
        response_json = response.json()
        # TODO - Error handling for user not found (404) and 
        # rate limiting (429) errors
        for child in response_json["data"]["children"]:
            
            id = child["data"]["id"]
            subreddit = str(child["data"]["subreddit"])
            text = str(child["data"]["body"])
            created_utc = child["data"]["created_utc"]
            score = child["data"]["score"]
            submission_id = child["data"]["link_id"].lower()[3:]
            edited = child["data"]["edited"]
            top_level = True if child["data"]["parent_id"].startswith("t3") else False
            gilded = child["data"]["gilded"]
            permalink = "http://www.reddit.com/r/%s/comments/%s/_/%s" % (subreddit, submission_id, id)
            comment = Comment(
                id=id,
                subreddit=subreddit,
                text=text,
                created_utc=created_utc,
                score=score,
                permalink=permalink,
                submission_id=submission_id,
                edited=edited,
                top_level=top_level,
                gilded=gilded
            )
            comments.append(comment)
        after = response_json["data"]["after"]
        if after:
            url = base_url + "&after=%s" % after
            # reddit may rate limit if we don't wait for 2 seconds 
            # between successive requests. If that happens, 
            # uncomment and increase sleep time in the following line.
            #time.sleep(0.5) 
        else:
            more_comments = False
        w = time.time()
        print("Scraping this page took: "+str(w-q))
    e = time.time()
    print("Time taken:" + str(e-s))
    return comments

def get_submissions(username, headers, limit=None):
    """
    Returns a list of redditor's submissions.
    
    """

    submissions = []
    more_submissions = True
    after = None
    base_url = f"http://www.reddit.com/user/{username}/submitted/.json?limit=100"
    url = base_url
    while more_submissions:
        response = requests.get(url, headers=headers)
        response_json = response.json()

        # TODO - Error handling for user not found (404) and 
        # rate limiting (429) errors
        
        for child in response_json["data"]["children"]:
            id = str(child["data"]["id"])
            subreddit = str(child["data"]["subreddit"])
            text = child["data"]["selftext"]
            created_utc = child["data"]["created_utc"]
            score = child["data"]["score"]
            permalink = "http://www.reddit.com" + str(child["data"]["permalink"].lower())
            url = str(child["data"]["url"].lower())
            title = str(child["data"]["title"])
            is_self = child["data"]["is_self"]
            gilded = child["data"]["gilded"]
            domain = child["data"]["domain"]
            submission = Submission(
                id=id,
                subreddit=subreddit,
                text=text,
                created_utc=created_utc,
                score=score,
                permalink=permalink,
                url=url,
                title=title,
                is_self=is_self,
                gilded=gilded,
                domain=domain
            )         
            submissions.append(submission)

        after = response_json["data"]["after"]

        if after:
            url = base_url + "&after=%s" % after
            # reddit may rate limit if we don't wait for 2 seconds 
            # between successive requests. If that happens, 
            # uncomment and increase sleep time in the following line.
            #time.sleep(0.5) 
        else:
            more_submissions = False

    return submissions


































class Util:
    """
    Contains a collection of common utility methods.

    """
    
    @staticmethod
    def sanitize_text(text):
        """
        Returns text after removing unnecessary parts.
        
        """
        
        MAX_WORD_LENGTH = 1024

        _text = " ".join([
            l for l in text.strip().split("\n") if (
                not l.strip().startswith("&gt;")
            )
        ])
        substitutions = [
            (r"\[(.*?)\]\((.*?)\)", r""),     # Remove links from Markdown
            (r"[\"](.*?)[\"]", r""),        # Remove text within quotes
            (r" \'(.*?)\ '", r""),            # Remove text within quotes
            (r"\.+", r". "),                # Remove ellipses
            (r"\(.*?\)", r""),                # Remove text within round brackets
            (r"&amp;", r"&"),                 # Decode HTML entities
            (r"http.?:\S+\b", r" ")         # Remove URLs
        ]
        for pattern, replacement in substitutions:
            _text = re.sub(pattern, replacement, _text, flags=re.I)

        # Remove very long words
        _text = " ".join(
            [word for word in _text.split(" ") if len(word) <= MAX_WORD_LENGTH]
        )
        return _text

    @staticmethod
    def coalesce(l):
        """
        Given a list, returns the last element that is not equal to "generic".
        
        """

        l = [x for x in l if x.lower() != "generic"]
        return next(iter(l[::-1]), "")

    @staticmethod
    def humanize_days(days):
        """
        Return text with years, months and days given number of days.
        
        """
        y = days/365 if days > 365 else 0
        m = (days - y*365)/31 if days > 30 else 0
        d = (days - m*31 - y*365)
        yy = str(y) + " year" if y else ""
        if y > 1:
            yy += "s"
        mm = str(m) + " month" if m else ""
        if m > 1:
            mm += "s"
        dd = str(d) + " day"
        if d>1 or d==0:
            dd += "s"
        return (yy + " " + mm + " " + dd).strip()

    @staticmethod
    def scale(val, src, dst):
        """
        Scale the given value from the scale of src to the scale of dst.
        """
        return ((val - src[0])/(src[1] - src[0])) * (dst[1]-dst[0]) + dst[0]
