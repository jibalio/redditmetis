from sherlock import Comment,Submission
import gzip
import base64


import re
comment_key = []

def compress_string(s):
    return base64.b64encode(gzip.compress(bytes(s,'utf-8')))

def decompress_string(s):
    pass

def parse_comments(c):
    comments = []
    for item in c:
        id = item[0]
        subreddit = item[1]
        text = item[2]
        created_utc = item[3]
        score = item[4]
        submission_id = item[5]
        edited = item[6]
        top_level = item[7]
        gilded = item[8]
        permalink = "http://www.reddit.com/r/%s/comments/%s/_/%s" % (subreddit, submission_id, id)
        
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
            text = re.sub(pattern, replacement, text, flags=re.I)

        if "FIXED" in text:
            print(text)

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
    return comments

def parse_submissions(s):
    submissions = []
    for item in s:
        id = item[0]
        subreddit = item[1]
        text = item[2]
        created_utc = item[3]
        score = item[4]
        permalink = "http://www.reddit.com" + item[5]
        url = item[6]
        title = item[7]
        is_self = item[8]
        gilded = item[9]
        domain = item[10]
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
    return submissions