# coding: utf-8
import json
import nltk
import datetime
import time
import requests
import traceback
import os
from metis import User, UserNotFoundException, InvalidUserError, NoDataError
from metis_utils import compress_string
#import metis_db_interface as mdi

production = False
prod_error_api = "https://redditmetis.com/api/mg/error"
dev_error_api = "http://localhost:5000/api/mg/error"

def lambda_handler(event, context):
    nltk.data.path.append("/tmp/nltk_data")
    
    MIN_CORPORA = [
    'brown',  # Required for FastNPExtractor
    'punkt',  # Required for WordTokenizer
    'wordnet',  # Required for lemmatization
    'averaged_perceptron_tagger',  # Required for NLTKTagger
    ]

    ADDITIONAL_CORPORA = [
        'conll2000',  # Required for ConllExtractor
        'movie_reviews',  # Required for NaiveBayesAnalyzer
    ]

    ALL_CORPORA = MIN_CORPORA + ADDITIONAL_CORPORA
    for each in ALL_CORPORA:
        nltk.download(each,"/tmp/nltk_data")
    
    s = event['body']

    #uname = event["queryStringParameters"]["uname"]
    #tz = event["queryStringParameters"]["tz"]

    response = {
        'statusCode': 200
    }
    
    response["headers"] = {
        'Content-Type': 'application/json', 
        'Access-Control-Allow-Origin': '*' 
    }   

    response['body'] = json.dumps(execute(s))

    return response
    
    
def execute(s_data):
    
    if production:
        error_api = prod_error_api
    else:
        error_api = dev_error_api

    print("Downloading subreddit data from 3.23.9.237.")
    
    # Production
    #CSV_DIR = os.path.join("/tmp/","subreddits.csv")
    # Development
    CSV_DIR = os.path.join("D:\\Files\\Documents\\Projects\\redditmetis-rs\\backend\\libraries\\metis_core","subreddits.csv")

    CSV_URL = "http://3.23.9.237/redditmetis/subreddits.csv"

    req = requests.get(CSV_URL, allow_redirects=True)
    open(CSV_DIR, 'wb').write(req.content)

    data = json.loads(s_data)
    username = data["about"]["name"]
    try:
        a = User(None,None,payload=data)
    except Exception as e:
        callstack = traceback.format_exc()
        requests.post(
            error_api, 
            data={
                "error_type":"LambdaError",
                "details":json.dumps({ 
                    "User Query":username,
                    "Message" : str(e),
		            "Callstack" : callstack,
                })
            }
        )
        return {"error":"UnexpectedError"}

    rs = compress_string(json.dumps(a.get_json())).decode("utf-8")
    
    # Put lambda upload here
    """The process here will be:
    1. read username in dynamodb. thanks to TTL, the data will always be new
    2. if keyerror, that means data isn't fresh anymore (or wasn't recorded at all),in this case:
        2.1. Run the crunching (existing code above)
        2.2. Save the data
    3. If not keyerror, simply return the data read!
    """
    


    return {
        "u": "uname",
        "b": rs,
        "n":"1",
        "l": datetime.datetime.now().timestamp()
    }
    
    
    
