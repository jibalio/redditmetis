from datetime import datetime, timedelta, MINYEAR
import re
import pytz
import requests
import sherlock
from sherlock import Comment,Post, Submission, Util
from text_parser import TextParser
from urllib.parse import urlparse
import time
import sys
import calendar
from collections import Counter
from itertools import groupby
import re
import json
from metis_utils import parse_submissions, parse_comments, compress_string, decompress_string
import json as j
import readability
import gzip
from textblob.en.sentiments import PatternAnalyzer
import statistics

parser = TextParser()
pa = PatternAnalyzer()

from subreddits import subreddits_dict, ignore_text_subs, default_subs
DEBUG=True



HEADERS = {
    'User-Agent': 'metis-reddit'
}

class UserNotFoundException(Exception):
    pass
class NoDataError(Exception):
    pass
class InvalidUserError(Exception):
    pass

class User:
    MIN_THRESHOLD = 3 
    MIN_THRESHOLD_FOR_DEFAULT = 10



    IMAGE_DOMAINS = [
        "imgur.com",
        "flickr.com",
        "i.reddituploads.com",
        "images.akamai.steamusercontent.com"
    ]
    VIDEO_DOMAINS = ["youtube.com", "youtu.be", "vimeo.com", "liveleak.com"]
    IMAGE_EXTENSIONS = ["jpg", "png", "gif", "bmp"]

    def __init__(self,username,tz, payload=None):

        if not payload:
            self.request_tz = tz
            self.username = username
        else:
            self.request_tz = payload['tz']
            self.username = payload['about']['name']


        self.today = datetime.now(tz=pytz.timezone(self.request_tz)).date()

            
        res = None
        url = None
        if not payload:
            url = f"http://www.reddit.com/user/{username}/about.json"
            res = requests.get(url, headers = HEADERS).json()
            if "error" in res and res["error"] == 404:
                raise UserNotFoundException
        else:
            res={"data":payload["about"]}

       
        print("Getting Basic Info...")
        self.name = res["data"]["name"]
    
        self.created_utc = datetime.fromtimestamp(res["data"]["created_utc"], tz = pytz.timezone(self.request_tz))
        self.account_age = datetime.now(tz=pytz.timezone(self.request_tz)) - self.created_utc
        self.account_age_years = self.account_age.days//365
        self.account_age_months = self.account_age.days%365//30
        self.account_age_days = self.account_age.days%30

        a_s = f"{self.account_age_years}y" if self.account_age_years else ""
        a_s += f"{self.account_age_months}m" if self.account_age_months else ""
        a_s += f"{self.account_age_days}d"
        self.age_string = a_s

        self.link_karma = res["data"]["link_karma"]
        self.comment_karma = res["data"]["comment_karma"]
        self.is_gold = res["data"]["is_gold"]
        self.reddit_id = res["data"]["id"]
        self.pos_max = 0
        self.pos_min = 0
            # Load comments
        self.signup_date = self.created_utc
        start = self.signup_date.date()

        
        """
        COMMENTS
        """
        print("Retrieving comments...")
        if not payload:
            self.comments = sherlock.get_comments(self.username,HEADERS)
            self.submissions = sherlock.get_submissions(self.username,HEADERS)
        else:
            self.comments = parse_comments(payload["comments"])
            self.submissions = parse_submissions(payload["submissions"])
        
        

        self.first_post_date = None

        self.earliest_comment = None
        self.latest_comment = None
        self.best_comment = None
        self.worst_comment = None

        self.earliest_submission = None
        self.latest_submission = None
        self.best_submission = None
        self.worst_submission = None


        print("Initializing empty values")
        self.sentiments = {
            "pos_polarity":[],
            "neg_polarity":[],
            "neu_polarity":[],
            "subjectivity":[],
            "most_positive_comment":None,
            "most_negative_comment":None
        }
        self.metrics = {
            "date" : [],
            "weekday" : [],
            "hour" : [],
            "subreddit" : [],
            "recent_karma" : [],
            "recent_posts" : []
        }

        self.submissions_by_type = {
            "name" : "All",
            "children" : [
                {
                    "name" : "Self", 
                    "children" : []
                },
                {
                    "name" : "Image", 
                    "children" : []
                },
                {
                    "name" : "Video", 
                    "children" : []
                },
                {
                    "name" : "Other", 
                    "children" : []
                }
            ]
        }

        self.metrics["date"] = []
        self.metrics["recent_karma"] = [0] * 61
        self.metrics["recent_posts"] = [0] * 61
        self.metrics["hour"] = []
        self.metrics["weekday"] = []
        self.genders = []
        self.orientations = []
        self.relationship_partners = []

        # Data that we are reasonably sure that *are* names of places.
        self.places_lived = []

        # Data that looks like it could be a place, but we're not sure.
        self.places_lived_extra = []

        # Data that we are reasonably sure that *are* names of places.
        self.places_grew_up = []

        # Data that looks like it could be a place, but we're not sure.
        self.places_grew_up_extra = []

        self.family_members = []
        self.pets = []

        self.attributes = []
        self.attributes_extra = []

        self.possessions = []
        self.possessions_extra = []
        
        self.actions = []
        self.actions_extra = []

        self.favorites = []
        
        self.derived_attributes = {
            "family_members" : [],
            "gadget" : [],
            "gender" : [],
            "locations" : [],
            "orientation" : [],
            "physical_characteristics" : [],
            "political_view" : [],
            "possessions" : [],
            "religion and spirituality" : []
        }

        self.corpus = ""
        
        self.commented_dates = []
        self.submitted_dates = []
        
        self.lurk_period = None

        self.comments_gilded = 0
        self.submissions_gilded = 0

        self.submission_score = {}
        self.comment_score = {}
        print("Process starting")
        self.process()

    def process(self):
        """
        Retrieves redditor's comments and submissions and 
        processes each of them.

        """
        if self.comments:
            print("Processing COmments")
            s = time.time()
            self.process_comments()
            e = time.time()
            print(f"Comments processed: {e-s}seconds.")

        if self.submissions:
            print("Processing sbmissions")
            s = time.time()
            self.process_submissions()
            e = time.time()
            print(f"Submissions processed: {e-s}seconds.")

        if self.comments or self.submissions:
            print("Derive Atributes")
            s = time.time()
            self.derive_attributes()
            e = time.time()
            print(f"Attributes derived: {e-s}seconds.")

    def process_comments(self):
        if not self.comments:
            return
        self.earliest_comment = self.comments[-1]
        self.latest_comment = self.comments[0]
        self.best_comment = self.comments[0]
        self.worst_comment = self.comments[0]
        for comment in self.comments:
            self.process_comment(comment)

    def process_submissions(self):
        """
        Process list of redditor's submissions.

        """

        if not self.submissions:
            return
        
        self.earliest_submission = self.submissions[-1]
        self.latest_submission = self.submissions[0]

        self.best_submission = self.submissions[0]
        self.worst_submission = self.submissions[0]

        for submission in self.submissions:
            self.process_submission(submission)

    submission_score = {}
    def process_submission(self, submission):
        """
        Process a single submission.

        * Updates metrics
        * Sanitizes and extracts chunks from self text.

        """
        
        if submission.subreddit not in self.submission_score:
            self.submission_score[submission.subreddit] = submission.score
        else:
            self.submission_score[submission.subreddit]+=submission.score

        if(submission.is_self):
            if submission.text is None:
                return True
            text = Util.sanitize_text(submission.text)
            self.corpus += text.lower()


        submission_type = None
        submission_domain = None
        submission_url_path = urlparse(submission.url).path
        
        if submission.domain.startswith("self."):
            submission_type = "Self"
            submission_domain = submission.subreddit
        elif (
            submission_url_path.endswith(tuple(self.IMAGE_EXTENSIONS)) or 
            submission.domain.endswith(tuple(self.IMAGE_DOMAINS))
        ):
            submission_type = "Image"
            submission_domain = submission.domain
        elif submission.domain.endswith(tuple(self.VIDEO_DOMAINS)):
            submission_type = "Video"
            submission_domain = submission.domain
        else:
            submission_type = "Other"
            submission_domain = submission.domain
        t = [
            x for x in self.submissions_by_type["children"] \
                if x["name"]==submission_type
        ][0]
        d = (
            [x for x in t["children"] if x["name"]==submission_domain] or \
            [None]
        )[0]
        if d:
            d["size"] += 1
        else:
            t["children"].append({
                "name" : submission_domain,
                "size" : 1
            })


        if submission.score > self.best_submission.score:
            self.best_submission = submission
        elif submission.score < self.worst_submission.score:
            self.worst_submission = submission
        
        # If submission is in a subreddit in which comments/self text 
        # are to be ignored (such as /r/jokes, /r/writingprompts, etc), 
        # do not process it further.
        if submission.subreddit in ignore_text_subs:
            return False

        # Only process self texts that contain "I" or "my"    
        if not submission.is_self or not re.search(r"\b(i|my)\b",text,re.I):
            return False
        
        (chunks, sentiments) = parser.extract_chunks(text)
        for chunk in chunks:
            self.load_attributes(chunk, submission)

        return True
    
    comment_score = {

    }

    def process_comment(self,comment):
        if comment.subreddit not in self.comment_score:
            self.comment_score[comment.subreddit] = comment.score
        else:
            self.comment_score[comment.subreddit]+=comment.score
        # Sanitize comment text.
        if comment.text is None:
            return True
            
 
        text = Util.sanitize_text(comment.text)
        # Add comment text to corpus.
        self.corpus += text.lower()
        comment_timestamp = datetime.fromtimestamp(
            comment.created_utc, tz=pytz.timezone(self.request_tz)
        )
        self.commented_dates.append(comment_timestamp)
        self.comments_gilded += comment.gilded
        

        if comment.score > self.best_comment.score:
            self.best_comment = comment
        elif comment.score < self.worst_comment.score:
            self.worst_comment = comment

        # If comment is in a subreddit in which comments/self text 
        # are to be ignored (such as /r/jokes, /r/writingprompts, etc), 
        # do not process it further.
        if comment.subreddit in ignore_text_subs:
            return False

        q = self.analyze_sentiment(comment)
        if q>=self.pos_max:
            self.sentiments["most_positive_comment"]=comment
            self.pos_max=q
        if q<=self.pos_min:
            self.sentiments["most_negative_comment"]=comment
            self.pos_min=q

        # If comment text does not contain "I" or "my", why even bother?
        if not re.search(r"\b(i|my)\b", text, re.I):
           return False
        
        # Now, this is a comment that needs to be processed.
        (chunks, sentiments) = parser.extract_chunks(text)
        

        for chunk in chunks:
            self.load_attributes(chunk, comment)

        return True        

   

    def analyze_sentiment(self, comment):
        text = comment.text
        q = pa.analyze(text)
        if q.polarity>0.07:
            self.sentiments["pos_polarity"].append(q.polarity)
        elif q.polarity<-0.07:
            self.sentiments["neg_polarity"].append(q.polarity)
        else:
            self.sentiments["neu_polarity"].append(q.polarity)
        self.sentiments["subjectivity"].append(q.subjectivity)
        return q.polarity
        


    def load_attributes(self, chunk, post):
    
        """
        Given an extracted chunk, load appropriate attribtues from it.

        """
        # Is this chunk a possession/belonging?
        if chunk["kind"] == "possession" and chunk["noun_phrase"]:
            # Extract noun from chunk
            noun_phrase = chunk["noun_phrase"]
            noun_phrase_text = " ".join([w for w, t in noun_phrase])
            norm_nouns = " ".join([
                parser.normalize(w, t) \
                    for w,t in noun_phrase if t.startswith("N")
            ])
            
            noun = next(
                (w for w, t in noun_phrase if t.startswith("N")), None
            )
            if noun:
                # See if noun is a pet, family member or a relationship partner
                pet = parser.pet_animal(noun)
                family_member = parser.family_member(noun)
                relationship_partner = parser.relationship_partner(noun)

                if pet:
                    self.pets.append((pet, post.permalink))
                elif family_member:
                    self.family_members.append((family_member, post.permalink))
                elif relationship_partner:
                    self.relationship_partners.append(
                        (relationship_partner, post.permalink)
                    )
                else:
                    self.possessions_extra.append((norm_nouns, post.permalink))

        # Is this chunk an action?
        elif chunk["kind"] == "action" and chunk["verb_phrase"]:
            verb_phrase = chunk["verb_phrase"]
            verb_phrase_text = " ".join([w for w, t in verb_phrase])

            # Extract verbs, adverbs, etc from chunk
            norm_adverbs = [
                parser.normalize(w,t) \
                    for w, t in verb_phrase if t.startswith("RB")
            ]
            adverbs = [w.lower() for w, t in verb_phrase if t.startswith("RB")]

            norm_verbs = [
                parser.normalize(w,t) \
                    for w, t in verb_phrase if t.startswith("V")
            ]
            verbs = [w.lower() for w, t in verb_phrase if t.startswith("V")]

            prepositions = [w for w, t in chunk["prepositions"]]

            noun_phrase = chunk["noun_phrase"]

            noun_phrase_text = " ".join(
                [w for w, t in noun_phrase if t not in ["DT"]]
            )
            norm_nouns = [
                parser.normalize(w,t) \
                    for w, t in noun_phrase if t.startswith("N")
            ]
            proper_nouns = [w for w, t in noun_phrase if t == "NNP"]
            determiners = [
                parser.normalize(w, t) \
                    for w, t in noun_phrase if t.startswith("DT")
            ]

            prep_noun_phrase = chunk["prep_noun_phrase"]
            prep_noun_phrase_text = " ".join([w for w, t in prep_noun_phrase])
            pnp_prepositions = [
                w.lower() for w, t in prep_noun_phrase if t in ["TO", "IN"]
            ]
            pnp_norm_nouns = [
                parser.normalize(w, t) \
                    for w, t in prep_noun_phrase if t.startswith("N")
            ]
            pnp_determiners = [
                parser.normalize(w, t) \
                    for w, t in prep_noun_phrase if t.startswith("DT")
            ]

            full_noun_phrase = (
                noun_phrase_text + " " + prep_noun_phrase_text
            ).strip()

            # TODO - Handle negative actions (such as I am not...), 
            # but for now:
            if any(
                w in ["never", "no", "not", "nothing", "neither"] \
                    for w in norm_adverbs+determiners
            ):
                return

            # I am/was ...
            if (len(norm_verbs) == 1 and "be" in norm_verbs and 
                not prepositions and noun_phrase):
                # Ignore gerund nouns for now
                if (
                    "am" in verbs and 
                    any(n.endswith("ing") for n in norm_nouns)
                ):
                    self.attributes_extra.append(
                        (full_noun_phrase, post.permalink)
                    )
                    return

                attribute = []
                for noun in norm_nouns:
                    gender = None
                    orientation = None
                    if "am" in verbs:
                        gender = parser.gender(noun)
                        orientation = parser.orientation(noun)
                    if gender:
                        self.genders.append((gender, post.permalink))
                    elif orientation:
                        self.orientations.append(
                            (orientation, post.permalink)
                        )
                    # Include only "am" phrases
                    elif "am" in verbs: 
                        attribute.append(noun)

                if attribute and (
                    (
                        # Include only attributes that end 
                        # in predefined list of endings...
                        any(
                            a.endswith(
                                parser.include_attribute_endings
                            ) for a in attribute
                        ) and not (
                            # And exclude...
                            # ...certain lone attributes
                            (
                                len(attribute) == 1 and 
                                attribute[0] in parser.skip_lone_attributes and 
                                not pnp_norm_nouns
                            )
                            or
                            # ...predefined skip attributes
                            any(a in attribute for a in parser.skip_attributes)
                            or
                            # ...attributes that end in predefined 
                            # list of endings
                            any(
                                a.endswith(
                                    parser.exclude_attribute_endings
                                ) for a in attribute
                            )
                        )
                    ) or 
                    (
                        # And include special attributes with different endings
                        any(a in attribute for a in parser.include_attributes)
                    )
                ):
                    self.attributes.append(
                        (full_noun_phrase, post.permalink)
                    )
                elif attribute:
                    self.attributes_extra.append(
                        (full_noun_phrase, post.permalink)
                    )

            # I live(d) in ...
            elif "live" in norm_verbs and prepositions and norm_nouns:
                if any(
                    p in ["in", "near", "by"] for p in prepositions
                ) and proper_nouns:
                    self.places_lived.append(
                        (
                            " ".join(prepositions) + " " + noun_phrase_text, 
                            post.permalink
                        )
                    )
                else:
                    self.places_lived_extra.append(
                        (
                            " ".join(prepositions) + " " + noun_phrase_text, 
                            post.permalink
                        )
                    )
            
            # I grew up in ...
            elif "grow" in norm_verbs and "up" in prepositions and norm_nouns:
                if any(
                    p in ["in", "near", "by"] for p in prepositions
                ) and proper_nouns:
                    self.places_grew_up.append(
                        (
                            " ".join(
                                [p for p in prepositions if p != "up"]
                            ) + " " + noun_phrase_text, 
                            post.permalink
                        )
                    )
                else:
                    self.places_grew_up_extra.append(
                        (
                            " ".join(
                                [p for p in prepositions if p != "up"]
                            ) + " " + noun_phrase_text, 
                            post.permalink
                        )
                    )

            elif(
                len(norm_verbs) == 1 and "prefer" in norm_verbs and 
                norm_nouns and not determiners and not prepositions
            ):
                self.favorites.append((full_noun_phrase, post.permalink))

            elif norm_nouns:
                actions_extra = " ".join(norm_verbs)
                self.actions_extra.append((actions_extra, post.permalink))    
    
    
    def derive_attributes(self):

        for name, count in self.commented_subreddits():
            subreddit = subreddits_dict[name] \
                if name in subreddits_dict else None
            if (
                subreddit and subreddit["attribute"] and 
                count >= self.MIN_THRESHOLD
            ):
                self.derived_attributes[subreddit["attribute"]].append(
                    subreddit["value"].lower()
                )

        for name, count in self.submitted_subreddits():
            subreddit = subreddits_dict[name] \
                if name in subreddits_dict else None
            if (
                subreddit and subreddit["attribute"] and 
                count >= self.MIN_THRESHOLD
            ):
                self.derived_attributes[subreddit["attribute"]].append(
                    subreddit["value"].lower()
                )

        # If someone mentions their wife, 
        # they should be male, and vice-versa (?)
        if "wife" in [v for v, s in self.relationship_partners]:
            self.derived_attributes["gender"].append("male")
        elif "husband" in [v for v, s in self.relationship_partners]:
            self.derived_attributes["gender"].append("female")

        commented_dates = sorted(self.commented_dates)
        submitted_dates = sorted(self.submitted_dates)
        active_dates = sorted(self.commented_dates + self.submitted_dates)

        min_date = datetime(MINYEAR, 1, 1, tzinfo=pytz.timezone(self.request_tz))
        first_comment_date = \
            min(commented_dates) if commented_dates else min_date
        first_submission_date = \
            min(submitted_dates) if submitted_dates else min_date
        

        self.first_post_date = max(first_comment_date, first_submission_date)
        
        active_dates += [datetime.now(tz=pytz.timezone(self.request_tz))]
        commented_dates += [datetime.now(tz=pytz.timezone(self.request_tz))]
        submitted_dates += [datetime.now(tz=pytz.timezone(self.request_tz))]

        # Find the longest period of inactivity
        comment_lurk_period = max(
            [
                {
                    "from" : calendar.timegm(d1.utctimetuple()), 
                    "to" : calendar.timegm(d2.utctimetuple()), 
                    "days" : (d2 - d1).total_seconds(), 
                } for d1, d2 in zip(
                    commented_dates, commented_dates[1:]
                )
            ], key=lambda x:x["days"]
        ) if len(commented_dates) > 1 else {"days":-1}

        submission_lurk_period = max(
            [
                {
                    "from" : calendar.timegm(d1.utctimetuple()), 
                    "to" : calendar.timegm(d2.utctimetuple()), 
                    "days" : (d2 - d1).total_seconds(), 
                } for d1, d2 in zip(
                    submitted_dates, submitted_dates[1:]
                )
            ], key=lambda x:x["days"]
        ) if len(submitted_dates) > 1 else {"days":-1}

        post_lurk_period = max(
            [
                {
                    "from" : calendar.timegm(d1.utctimetuple()), 
                    "to" : calendar.timegm(d2.utctimetuple()), 
                    "days" : (d2 - d1).total_seconds(),
                } for d1, d2 in zip(
                    active_dates, active_dates[1:]
                )
            ], key=lambda x:x["days"]
        )

        self.lurk_period = min(
            [
                x for x in [
                    comment_lurk_period, 
                    submission_lurk_period, 
                    post_lurk_period
                ] if x["days"]>=0
            ],
            key=lambda x:x["days"]
        )
        del self.lurk_period["days"]
    
    def commented_subreddits(self):
        """
        Returns a list of subreddits redditor has commented on.

        """

        return [
            (name, count) for (name, count) in Counter(
                [comment.subreddit for comment in self.comments]
            ).most_common()
        ]

    def commented_subreddits_by_karma(self):
        """
        Returns a list of subreddits redditor has commented on. (sorted by karma)
        """
        return [
            (name, count) for (name, count) in Counter(
                [comment.subreddit for comment in self.comments]
            ).most_common()
        ]
    
    def submitted_subreddits(self):
        """
        Returns a list of subreddits redditor has submitted to.
        
        """

        return [
            (name,count) for (name,count) in Counter(
                [submission.subreddit for submission in self.submissions]
            ).most_common()
        ]
    
    
    
    
    
    
    def get_json(self):
        d = {
            "username":self.username,
            "age_string":self.age_string,
            "link_karma":self.link_karma,
            "comment_karma":self.comment_karma,
            "is_gold":self.is_gold,
            "total_karma":self.link_karma+self.comment_karma,
            "joined":self.created_utc.strftime("%B %d, %Y")
        }
        # Redditor has no data?
        if not (self.comments or self.submissions):
            raise NoDataError
        
        # Format metrics
        metrics_date = []
        
        for d in self.metrics["date"]:
            metrics_date.append(
                {
                    "date" : "%d-%02d-01" % (d["date"][0], d["date"][1]), 
                    "comments" : d["comments"],
                    "submissions" : d["submissions"],
                    "posts" : d["comments"] + d["submissions"],
                    "comment_karma" : d["comment_karma"],
                    "submission_karma" : d["submission_karma"],
                    "karma" : d["comment_karma"] + d["submission_karma"]
                }
            )

        
        metrics_hour = []
        
        for h in self.metrics["hour"]:
            metrics_hour.append(
                {
                    "hour" : h["hour"], 
                    "comments" : h["comments"], 
                    "submissions" : h["submissions"],
                    "posts" : h["comments"] + h["submissions"],
                    "comment_karma" : h["comment_karma"],
                    "submission_karma" : h["submission_karma"],
                    "karma" : h["comment_karma"] + h["submission_karma"]
                }
            )

        weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        
        
        metrics_weekday = []
        
        for w in self.metrics["weekday"]:
            metrics_weekday.append(
                {
                    "weekday" : weekdays[w["weekday"]], 
                    "comments" : w["comments"], 
                    "submissions" : w["submissions"],
                    "posts" : w["comments"] + w["submissions"],
                    "comment_karma" : w["comment_karma"],
                    "submission_karma" : w["submission_karma"],
                    "karma" : w["comment_karma"] + w["submission_karma"]
                }
            )
        
        metrics_subreddit = {
            "name" : "All", 
            "children" : []
        }
        
        for (name, [comments, comment_karma]) in [
            (s, [sum(x) for x in zip(*[(1, r[1]) for r in group])]) \
                for s, group in groupby(
                    sorted(
                        [
                            (p.subreddit, p.score) for p in self.comments
                        ], key=lambda x: x[0]
                    ), lambda x: x[0]
                )
        ]:
            subreddit = subreddits_dict[name] if name in subreddits_dict else None
            if subreddit and subreddit["topic_level1"] != "Other":
                topic_level1 = subreddit["topic_level1"]
            else:
                topic_level1 = "Other"

            level1 = (
                [
                    t for t in metrics_subreddit["children"] if t["name"] == topic_level1
                ] or [None]
            )[0]
            if level1:
                level1["children"].append(
                    {
                        "name" : name,
                        "comments" : comments,
                        "submissions" : 0,
                        "posts" : comments,
                        "comment_karma" : comment_karma,
                        "submission_karma" : 0,
                        "karma" : comment_karma
                    }
                )
            else:
                metrics_subreddit["children"].append(
                    {
                        "name" : topic_level1, 
                        "children" : [
                            {
                                "name" : name,
                                "comments" : comments,
                                "submissions" : 0,
                                "posts" : comments,
                                "comment_karma" : comment_karma,
                                "submission_karma" : 0,
                                "karma" : comment_karma
                            }
                        ]
                    }
                )
        
        for (name, [submissions, submission_karma]) in [
            (s, [sum(x) for x in zip(*[(1,r[1]) for r in group])]) \
                for s, group in groupby(
                    sorted(
                        [
                            (p.subreddit, p.score) for p in self.submissions
                        ], key=lambda x: x[0]
                    ), lambda x: x[0]
                )
        ]:
            subreddit = subreddits_dict[name] \
                if name in subreddits_dict else None
            if subreddit and subreddit["topic_level1"] != "Other":
                topic_level1 = subreddit["topic_level1"]
            else:
                topic_level1 = "Other"
            level1 = (
                [
                    t for t in metrics_subreddit["children"] \
                        if t["name"] == topic_level1
                ] or [None]
            )[0]
            if level1:
                sub_in_level1 = (
                    [
                        s for s in level1["children"] if s["name"] == name
                    ] or [None]
                )[0]
                if sub_in_level1:
                    sub_in_level1["submissions"] = submissions
                    sub_in_level1["submission_karma"] = submission_karma
                    sub_in_level1["posts"] += submissions
                    sub_in_level1["karma"] += submission_karma
                else:
                    level1["children"].append(
                        {
                            "name" : name,
                            "comments" : 0,
                            "submissions" : submissions,
                            "posts" : submissions,
                            "comment_karma" : 0,
                            "submission_karma" : submission_karma,
                            "karma" : submission_karma
                        }
                    )
            else:
                metrics_subreddit["children"].append(
                    {
                        "name" : topic_level1, 
                        "children" : [
                            {
                                "name" : name,
                                "comments" : 0,
                                "submissions" : submissions,
                                "posts" : submissions,
                                "comment_karma" : 0,
                                "submission_karma" : submission_karma,
                                "karma" : submission_karma
                            }
                        ]
                    }
                )
        
        
        metrics_topic = {
            "name" : "All", 
            "children" : []
        }
        
        # We need both topics (for Posts across topics) and 
        # synopsis_topics (for Synopsis) because we want to include only 
        # topics that meet the threshold limits in synopsis_topics        
        synopsis_topics = []

        for name, count in Counter(
            [s.subreddit for s in self.submissions] + 
            [c.subreddit for c in self.comments]
        ).most_common():
            if (
                name in default_subs and 
                count >= self.MIN_THRESHOLD_FOR_DEFAULT
            ) or count >= self.MIN_THRESHOLD:
                subreddit = subreddits_dict[name] \
                    if name in subreddits_dict else None
                if subreddit:
                    topic = subreddit["topic_level1"]
                    if subreddit["topic_level2"]:
                        topic += ">" + subreddit["topic_level2"]
                    else:
                        topic += ">" + "Generic"
                    if subreddit["topic_level3"]:
                        topic += ">" + subreddit["topic_level3"]
                    else:
                        topic += ">" + "Generic"
                    synopsis_topics += [topic] * count

        topics = []
        
        for comment in self.comments:
            subreddit = subreddits_dict[comment.subreddit] \
                if comment.subreddit in subreddits_dict else None
            if subreddit and subreddit["topic_level1"] != "Other":
                topic = subreddit["topic_level1"]
                if subreddit["topic_level2"]:
                    topic += ">" + subreddit["topic_level2"]
                else:
                    topic += ">" + "Generic"
                if subreddit["topic_level3"]:
                    topic += ">" + subreddit["topic_level3"]
                else:
                    topic += ">" + "Generic"
                topics.append(topic)
            else:
                topics.append("Other")
        
        for submission in self.submissions:
            subreddit = subreddits_dict[submission.subreddit] \
                if submission.subreddit in subreddits_dict else None
            if subreddit and subreddit["topic_level1"] != "Other":
                topic = subreddit["topic_level1"]
                if subreddit["topic_level2"]:
                    topic += ">" + subreddit["topic_level2"]
                else:
                    topic += ">" + "Generic"
                if subreddit["topic_level3"]:
                    topic += ">" + subreddit["topic_level3"]
                else:
                    topic += ">" + "Generic"
                topics.append(topic)
            else:
                topics.append("Other")
        
        for topic, count in Counter(topics).most_common():
            level_topics = filter(None, topic.split(">"))
            current_node = metrics_topic
            for i, level_topic in enumerate(level_topics):
                children = current_node["children"]
                if i+1 < len(list(level_topics)):
                    found_child = False
                    for child in children:
                        if child["name"] == level_topic:
                            child_node = child
                            found_child = True
                            break
                    if not found_child:
                        child_node = {
                            "name" : level_topic, 
                            "children" : []
                        }
                        children.append(child_node)
                    current_node = child_node
                else:
                    child_node = {
                        "name" : level_topic, 
                        "size" : count
                    }
                    children.append(child_node)     
        
        common_words = [
            {
                "text" : word, 
                "size" : count
            } for word, count in Counter(
                parser.common_words(self.corpus)
            ).most_common(200)
        ]
        total_word_count = parser.total_word_count(self.corpus)
        unique_word_count = parser.unique_word_count(self.corpus)
        self.read_results = readability.getmeasures(self.corpus.split('.'), lang='en') 

        # Let's use an average of 40 WPM
        hours_typed = round(total_word_count/(40.00*60.00), 2) 

        gender = []
        for value, count in Counter(
            [value for value, source in self.genders]
        ).most_common(1):
            sources = [s for v, s in self.genders if v == value]
            gender.append(
                {
                    "value" : value, 
                    "count" : count, 
                    "sources" : sources
                }
            )

        orientation = []
        for value, count in Counter(
            [value for value, source in self.orientations]
        ).most_common(1):
            sources = [s for v, s in self.orientations if v == value]
            orientation.append(
                {
                    "value" : value, 
                    "count" : count, 
                    "sources" : sources
                }
            )

        relationship_partner = []
        for value, count in Counter(
            [value for value, source in self.relationship_partners]
        ).most_common(1):
            sources = [s for v, s in self.relationship_partners if v == value]
            relationship_partner.append(
                {
                    "value" : value, 
                    "count" : count, 
                    "sources" : sources
                }
            )

        places_lived = []
        for value, count in Counter(
            [value for value, source in self.places_lived]
        ).most_common():
            sources = [s for v, s in self.places_lived if v == value]
            places_lived.append(
                {
                    "value" : value, 
                    "count" : count, 
                    "sources" : sources
                }
            )

        places_lived_extra = []
        for value, count in Counter(
            [value for value, source in self.places_lived_extra]
        ).most_common():
            sources = [s for v, s in self.places_lived_extra if v == value]
            places_lived_extra.append(
                {
                    "value" : value, 
                    "count" : count, 
                    "sources" : sources
                }
            )

        places_grew_up = []
        for value, count in Counter(
            [value for value, source in self.places_grew_up]
        ).most_common():
            sources = [s for v, s in self.places_grew_up if v == value]
            places_grew_up.append(
                {
                    "value" : value, 
                    "count" : count, 
                    "sources" : sources
                }
            )

        places_grew_up_extra = []
        for value, count in Counter(
            [value for value, source in self.places_grew_up_extra]
        ).most_common():
            sources = [s for v, s in self.places_grew_up_extra if v == value]
            places_grew_up_extra.append(
                {
                    "value" : value, 
                    "count" : count, 
                    "sources" : sources
                }
            )

        family_members = []
        for value, count in Counter(
            [value for value, source in self.family_members]
        ).most_common():
            sources = [s for v, s in self.family_members if v == value]
            family_members.append(
                {
                    "value" : value, 
                    "count" : count, 
                    "sources" : sources
                }
            )

        pets = []
        for value, count in Counter(
            [value for value, source in self.pets]
        ).most_common():
            sources = [s for v, s in self.pets if v == value]
            pets.append(
                {
                    "value" : value, 
                    "count" : count, 
                    "sources" : sources
                }
            )

        favorites = []
        for value, count in Counter(
            [value for value, source in self.favorites]
        ).most_common():
            sources = [s for v, s in self.favorites if v == value]
            favorites.append(
                {
                    "value" : value, 
                    "count" : count, 
                    "sources" : sources
                }
            )

        attributes = []
        for value, count in Counter(
            [value for value, source in self.attributes]
        ).most_common():
            sources = [s for v, s in self.attributes if v == value]
            attributes.append(
                {
                    "value" : value, 
                    "count" : count, 
                    "sources" : sources
                }
            )

        attributes_extra = []
        for value, count in Counter(
            [value for value, source in self.attributes_extra]
        ).most_common():
            sources = [s for v, s in self.attributes_extra if v == value]
            attributes_extra.append(
                {
                    "value" : value, 
                    "count" : count, 
                    "sources" : sources
                }
            )

        possessions = []
        for value, count in Counter(
            [value for value, source in self.possessions]
        ).most_common():
            sources = [s for v, s in self.possessions if v == value]
            possessions.append(
                {
                    "value" : value, 
                    "count" : count, 
                    "sources" : sources
                }
            )

        possessions_extra = []
        for value, count in Counter(
            [value for value, source in self.possessions_extra]
        ).most_common():
            sources = [s for v, s in self.possessions_extra if v == value]
            possessions_extra.append(
                {
                    "value" : value, 
                    "count" : count, 
                    "sources" : sources
                }
            )
                
        actions = []
        for value, count in Counter(
            [value for value, source in self.actions]
        ).most_common():
            sources = [s for v, s in self.actions if v == value]
            actions.append(
                {
                    "value" : value, 
                    "count" : count, 
                    "sources" : sources
                }
            )

        actions_extra = []
        for value, count in Counter(
            [value for value, source in self.actions_extra]
        ).most_common():
            sources = [s for v, s in self.actions_extra if v == value]
            actions_extra.append(
                {
                    "value" : value, 
                    "count" : count, 
                    "sources" : sources
                }
            )

        synopsis = {}

        if gender:
            synopsis["gender"] = {
                "data" : gender
            }

        if orientation:
            synopsis["orientation"] = {
                "data" : orientation
            }

        if relationship_partner:
            synopsis["relationship_partner"] = {
                "data" : relationship_partner
            }

        if places_lived:
            synopsis["places_lived"] = {
                "data" : places_lived
            }

        if places_lived_extra:
            if "places_lived" in synopsis:
                synopsis["places_lived"].update(
                    {
                        "data_extra" : places_lived_extra
                    }
                )
            else:
                synopsis["places_lived"] = {
                    "data_extra" : places_lived_extra
                }

        if places_grew_up:
            synopsis["places_grew_up"] = {
                "data" : places_grew_up
            }

        if places_grew_up_extra:
            if "places_grew_up" in synopsis:
                synopsis["places_grew_up"].update(
                    {
                        "data_extra" : places_grew_up_extra
                    }
                )
            else:
                synopsis["places_grew_up"] = {
                    "data_extra" : places_grew_up_extra
                }

        if family_members:
            synopsis["family_members"] = {
                "data" : family_members
            }

        if pets:
            synopsis["pets"] = {
                "data" : pets
            }

        if favorites:
            synopsis["favorites"] = {
                "data" : favorites
            }

        if attributes:
            synopsis["attributes"] = {
                "data" : attributes
            }

        if attributes_extra:
            if "attributes" in synopsis:
                synopsis["attributes"].update(
                    {
                        "data_extra" : attributes_extra
                    }
                )
            else:
                synopsis["attributes"] = {
                    "data_extra" : attributes_extra
                }

        if possessions:
            synopsis["possessions"] = {
                "data" : possessions
            }

        if possessions_extra:
            if "possessions" in synopsis:
                synopsis["possessions"].update(
                    {
                        "data_extra" : possessions_extra
                    }
                )
            else:
                synopsis["possessions"] = {
                    "data_extra" : possessions_extra
                }
        
        ''' Will work on actions later
        if actions:
            synopsis["actions"] = {
                "data" : actions
            }

        if actions_extra:
            if "actions" in synopsis:
                synopsis["actions"].update(
                    {
                        "data_extra" : actions_extra
                    }
                )
            else:
                synopsis["actions"] = {
                    "data_extra" : actions_extra
                }
        '''

        level1_topic_groups = [
            "business","entertainment", "gaming", "hobbies and interests", "lifestyle", 
            "locations", "music", "science", "sports", "technology", 
            "news and politics"
        ]

        level2_topic_groups = [
            "television", "books", "celebrities", # Entertainment
            "religion and spirituality", # Lifestyle
        ]

        exclude_topics = ["general", "drugs", "meta", "adult and nsfw", "other"]

        exclude_coalesced_topics = [
            "religion and spirituality", "more interests", "alternative"
        ]

        topic_min_levels = {
            "business" : 2, 
            "entertainment" : 3,
            "gaming" : 2,
            "hobbies and interests" : 2,
            "lifestyle" : 2,
            "locations" : 3,
            "music" : 2,
            "science" : 2,
            "sports" : 2,
            "technology" : 2,
            "news and politics" : 2
        }


        for topic, count in Counter(synopsis_topics).most_common():
            if count < self.MIN_THRESHOLD:
                continue
            level_topics = [
                x.lower() for x in topic.split(">") if x.lower() != "generic"
            ]
            key = None
            if level_topics[0] not in exclude_topics:
                m = 2
                if level_topics[0] in level1_topic_groups:
                    m = topic_min_levels[level_topics[0]]
                if (
                    len(level_topics) >= m and 
                    level_topics[1] in level2_topic_groups and 
                    level_topics[1] not in exclude_topics
                ):
                    key = level_topics[1]
                elif (
                    len(level_topics) >= m and 
                    level_topics[1] not in exclude_topics
                ):
                    key = level_topics[0]
                elif level_topics[0] not in level1_topic_groups:
                    key = "other"
                coalesced_topic = Util.coalesce(level_topics).lower()     
                if key and coalesced_topic not in exclude_coalesced_topics:
                    if key in synopsis:
                        if key not in ["gender", "religion and spirituality"]:
                            synopsis[key]["data"].append(
                                {
                                    "value" : coalesced_topic, 
                                    "count" : count
                                }
                            )
                    else:
                        synopsis[key] = {
                            "data" : [
                                {
                                    "value" : coalesced_topic, 
                                    "count" : count
                                }
                            ]
                        }

        for k in {k: v for k, v in self.derived_attributes.items() if len(v)}:
            dd = [
                {
                    "value" : v, 
                    "count" : c, 
                    "sources" : None
                } for v, c in Counter(self.derived_attributes[k]).most_common()
            ]
            if k in ["gender", "religion and spirituality"]:
                dd = dd[:1]
            if k in synopsis:
                synopsis[k].update(
                    {
                        "data_derived" : dd 
                    }
                )
            else:
                synopsis[k] = {
                    "data_derived" : dd
                }

        computed_comment_karma = sum(
            [x["comment_karma"] for x in metrics_date]
        )
        computed_submission_karma = sum(
            [x["submission_karma"] for x in metrics_date]
        )

        

        
        


        
        top_subs_karma = [(i,self.submission_score[i]) for i in self.submission_score]
        top_comments_karma = [(i,self.comment_score[i]) for i in self.comment_score]
        results = {
            "metis_meta":{
                "version":"0.1",
                "request_tz":self.request_tz,
            },
            "username":self.username,
            "age_string":self.age_string,
            "link_karma":self.link_karma,
            "comment_karma":self.comment_karma,
            "is_gold":self.is_gold,
            "total_karma":self.link_karma+self.comment_karma,
            "joined":self.created_utc.strftime("%B %d, %Y"),
            "sherlock_version" : 8,
            "metadata" : {
                "reddit_id" : self.reddit_id,
                "latest_comment_id" : self.latest_comment.id \
                    if self.latest_comment else None,
                "latest_submission_id" : self.latest_submission.id \
                    if self.latest_submission else None
            },
            "top_subs":{
                "post":self.submitted_subreddits()[:min(10,len(self.submitted_subreddits()))],
                "comment":self.commented_subreddits()[:min(10,len(self.commented_subreddits()))],
            },
            "top_subs_by_karma":{
                "submission":sorted(top_subs_karma, key=lambda x:x[1],reverse=True)[:min(10,len(list(top_subs_karma)))],
                "comment":sorted(top_comments_karma, key=lambda x:x[1],reverse=True)[:min(10,len(list(top_comments_karma)))],
            },
            "summary" : {
                "signup_date" : calendar.timegm(
                        self.signup_date.utctimetuple()
                    ),
                "first_post_date" : calendar.timegm(
                        self.first_post_date.utctimetuple()
                    ),
                "lurk_period" : self.lurk_period,
                "comments" : {
                    "count" : len(self.comments),
                    "gilded" : self.comments_gilded,
                    "best" : {
                        "text" : self.best_comment.text \
                            if self.best_comment else None,
                        "permalink" : self.best_comment.permalink \
                            if self.best_comment else None,
                        "votes": self.best_comment.score \
                            if self.best_comment else None,
                        "created_utc":self.best_comment.created_utc \
                            if self.best_comment else None,
                        "sub":self.best_comment.subreddit \
                            if self.best_comment else None,
                    },
                    "worst" : {
                        "text" : self.worst_comment.text \
                            if self.worst_comment else None,
                        "permalink" : self.worst_comment.permalink \
                            if self.worst_comment else None,
                        "votes": self.worst_comment.score \
                            if self.worst_comment else None,
                        "created_utc":self.worst_comment.created_utc \
                            if self.worst_comment else None,
                        "sub":self.worst_comment.subreddit \
                            if self.worst_comment else None,
                    },
                    "all_time_karma" : self.comment_karma,
                    "computed_karma" : computed_comment_karma,
                    "average_karma" : round(
                        self.comment_karma/(len(self.comments) or 1), 2
                    ),
                    "total_word_count" : total_word_count,
                    "unique_word_count" : unique_word_count,
                    "hours_typed" : hours_typed,
                    "karma_per_word" : round(
                        self.comment_karma/(total_word_count*1.00 or 1), 2
                    )
                },
                "submissions" : {
                    "count" : len(self.submissions),
                    "gilded" : self.submissions_gilded,
                    "best" : {
                        "title" : self.best_submission.title \
                            if self.best_submission else None,
                        "permalink" : self.best_submission.permalink \
                            if self.best_submission else None,
                        "votes": self.best_submission.score \
                            if self.best_submission else None,
                        "created_utc":self.best_submission.created_utc \
                            if self.best_submission else None,
                        "sub":self.best_submission.subreddit \
                            if self.best_submission else None,
                    },
                    "worst" : {
                        "title" : self.worst_submission.title \
                            if self.worst_submission else None,
                        "permalink" : self.worst_submission.permalink \
                            if self.worst_submission else None,
                        "votes": self.worst_submission.score \
                            if self.worst_submission else None ,
                        "created_utc":self.best_submission.created_utc \
                            if self.worst_submission else None,
                        "sub":self.worst_submission.subreddit \
                            if self.worst_submission else None,
                    },
                    "all_time_karma" : self.link_karma,
                    "computed_karma" : self.link_karma,
                    "average_karma" : round(
                        self.link_karma / 
                        (len(self.submissions) or 1), 2
                    ),
                    "type_domain_breakdown" : self.submissions_by_type
                }
            },
            "synopsis" : synopsis,
            "metrics" : {
                "date" : metrics_date,
                "hour" : metrics_hour,
                "weekday" : metrics_weekday,
                "subreddit" : metrics_subreddit,
                "topic" : metrics_topic,
                "common_words" : common_words,
                "recent_karma" : self.metrics["recent_karma"],
                "recent_posts" : self.metrics["recent_posts"]
            },
            "readability":{
                'gf-index':self.read_results['readability grades']['GunningFogIndex'],
                'syll_per_word':self.read_results['sentence info']['syll_per_word'],
            },
            "sentiments":{
                "pos_polarity":statistics.mean(self.sentiments["pos_polarity"] or [0]),
                "neg_polarity":statistics.mean(self.sentiments["neg_polarity"] or [0]),
                "subjectivity":statistics.mean(self.sentiments["subjectivity"]),
                "most_positive_comment" : {
                    "text" : self.sentiments["most_positive_comment"].text \
                        if self.sentiments["most_positive_comment"] else None,
                    "permalink" : self.sentiments["most_positive_comment"].permalink \
                        if self.sentiments["most_positive_comment"] else None,
                    "votes": self.sentiments["most_positive_comment"].score,
                    "created_utc":self.sentiments["most_positive_comment"].created_utc,
                    "sub":self.sentiments["most_positive_comment"].subreddit
                    },
                "most_negative_comment" : {
                    "text" : self.sentiments["most_negative_comment"].text \
                        if self.sentiments["most_negative_comment"] else None,
                    "permalink" : self.sentiments["most_negative_comment"].permalink \
                        if self.sentiments["most_negative_comment"] else None,
                    "votes": self.sentiments["most_negative_comment"].score,
                    "created_utc":self.sentiments["most_negative_comment"].created_utc,
                    "sub":self.sentiments["most_negative_comment"].subreddit
                },
                "positive":len(self.sentiments["pos_polarity"]),
                "negative":len(self.sentiments["neg_polarity"]),
                "neutral":len(self.sentiments["neu_polarity"]),
            }
        }

        return results

    


    