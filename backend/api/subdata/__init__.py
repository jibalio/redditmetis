import json
import csv
import datetime 
import os
from shutil import copyfile
from flask import Blueprint, request, Response
from flask import current_app as app


from libraries.cacher.cacher import get_user_result, try_add_key
from libraries.constants import SETTINGS
from libraries.mysqlconn import DB, settings
import mysql.connector


SUBREDDIT_EXPORT_DIR = SETTINGS["core"]["subreddit_export_dir"]

api_subdata = Blueprint('api_subdata', __name__,
                    template_folder='templates',
                    static_folder='static',)




@api_subdata.route('/api/subdata/export_subreddits')
def export_subreddits():
    db = DB()
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM sub_export;")
    result = cursor.fetchall()

    f = open(SUBREDDIT_EXPORT_DIR, 'w', newline='')

    with f:
        writer = csv.writer(f)
        for row in result:
            writer.writerow(row)

    return Response(json.dumps({"success":True,"error":None}), mimetype="application/json")


@api_subdata.route('/api/subdata/topics')
def get_topics():
    db = DB()
    cursor = db.connection.cursor()
    cursor.execute("SELECT `id`, `name` FROM `topic` ORDER BY `name` ASC;")
    result = cursor.fetchall()
    topics = []
    for t in result:
        x = dict()
        x["name"] = t[1]
        x["value"] = t[0]
        topics.append(x)
    return Response(json.dumps(topics), mimetype="application/json")

@api_subdata.route('/api/subdata/getrandom')
def get_random():
    db = DB()
    cursor = db.connection.cursor()
    cursor.execute("select * from random_subs")
    result = cursor.fetchall()
    result = [x[0] for x in result]
    return Response(json.dumps(result), mimetype="application/json")

@api_subdata.route('/api/subdata/submitcategorization', methods=["POST"])
def submit_subreddit_categorization():
    data = request.json
    data = [(x['subreddit'], x['topic_id'], 1) for x in data]

    query = """
        INSERT INTO subreddit_topic_suggestion 
            (`name`, topic_id, votes) 
        VALUES 
            (%s, %s, %s)
        ON DUPLICATE KEY UPDATE votes = votes + 1;
        """

    db = DB()

    # Prepared Statement
    cursor = db.connection.cursor(prepared=True)
    for row in data:
        cursor.execute(query, row)
    
    db.connection.commit()

    return Response("{success:true}", mimetype="application/json")


@api_subdata.route('/api/subdata/update_subreddits')
def update_subreddits():
    """
    update_subreddits
    Cron job set to run daily. This updates the subreddits table based on the 
    categorization suggestions. Then deletes the suggestions that have already been categorized.
    This exports 'subreddits.csv' in the server that will be fetched by
    the metis function in AWS Lambda.
    """
    db = mysql.connector.connect(**settings)
    cursor = db.cursor()
    cursor.callproc("update_subreddits")
    db.commit()
    cursor.close()
    db.close()

    db = mysql.connector.connect(**settings)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM sub_export")
    
    csvfile = os.path.join(SUBREDDIT_EXPORT_DIR, "subreddits.csv")
    if os.path.isfile(csvfile):
        copyfile(csvfile, os.path.join(SUBREDDIT_EXPORT_DIR, "subreddit_"+datetime.datetime.now().strftime("%Y%m%d_%H%M")+".csv"))
    
    with open(csvfile, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in cursor:
            writer.writerow([x if x else '' for x in row])

    return Response("{success:true}", mimetype="application/json")


    

