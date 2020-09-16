
import sys
import json
import os
import pytz
import base64
import requests 

from flask import Blueprint, render_template, send_from_directory, current_app
from flask import current_app as app

from libraries.constants import PRODUCTION

# from libraries.metis_core.metis import User



from libraries.glogger.glogger import write_log, improve_emotion

MAINTENANCE = False

from datetime import datetime
from flask import Flask, render_template, url_for, request, Response, send_from_directory, redirect
from pprint import pprint
# from metis_utils import compress_string, decompress_string



# Set up a Blueprint
app_redditmetis = Blueprint('app_redditmetis', __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path='/rmstatic')

@app_redditmetis.route("/maintenance")
def maintenance():
    return render_template("maintenance.html")

# Routes

@app_redditmetis.route('/render/<string:template_name>')
def render_page_template(template_name):
    return render_template(f'{template_name}.html')

@app_redditmetis.route('/robots.txt')
def static_from_root():
    return send_from_directory(app_redditmetis.static_folder, request.path[1:])


@app_redditmetis.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app_redditmetis.route('/u/<string:username>')
def userpage_legacy(username):
    return redirect(f"/user/{username}", code=302)


@app_redditmetis.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app_redditmetis.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')



@app_redditmetis.route('/')
def asdsbvc():
    return render_template("rm_index.html")

"""
@app_redditmetis.route('/')
def index():
    if (MAINTENANCE):
        return render_template('maintenance.html')

    return render_template('rm_index.html') 
"""

@app_redditmetis.route('/user/<string:username>')
def userpage(username):
    print(app_redditmetis.static_folder)
    return send_from_directory(os.path.join(app_redditmetis.static_folder,"spa"), "index.html")
    if (MAINTENANCE):
        return render_template('maintenance.html')
    # for debug purposes, this wont query the Reddit API and just
    # display the template instead.
    disabled = request.args.get("disabled",default=False)
    cached_json = request.args.get("cached_json",default=False)
    debug = request.args.get("debug","false")
    print(debug)
    context = {"username":username, "disabled":disabled, "cached_json":cached_json, "debug":debug.lower()}
    return render_template('userpage.html', **context)


#if not PRODUCTION:
 #   import importlib
 #   lambda_execute = importlib.import_module("libraries.metis_core.lambda").execute


@app_redditmetis.route('/api/metis_local', methods=["POST"])
def metis_local():
    if PRODUCTION:
        return Response("{'error':'Unavailable when in production mode.'}", status=403, mimetype='application/json')
    else:
        data = request.data
        result = lambda_execute(json.loads(data)["data"])
        a = {
            "Payload":
                json.dumps({
                    "statusCode":200,
                    "headers":{
                        "Access-Control-Allow-Origin":"*",
                        "Content-Type":"application/json"
                    },
                    "body":json.dumps(result)
                
                }) ,
            "StatusCode":200,
        }
        print(a)
        return Response(json.dumps(a), mimetype="application/json")

@app_redditmetis.route('/glog')
def glog():
    return "OK"
    username = request.args.get("username",default="undefined")
    tz = request.args.get("tz",default="UTC")
    t = datetime.now(pytz.utc)
    tlocal = datetime.now(tz=pytz.timezone(tz))
    utc8=datetime.now(tz=pytz.timezone("Asia/Singapore"))
    ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    ul=username.lower()
    us = request.user_agent.string
    pl = request.user_agent.platform
    br =  request.user_agent.browser
    v=request.user_agent.version
    l=request.user_agent.language
    write_log(
        t.strftime("%Y %m %d %H:%M:%S"),
        tlocal.strftime("%Y %m %d %H:%M:%S"),
        utc8.strftime("%Y %m %d %H:%M:%S"),ul,ip,us,tz,pl,br,v,l,
        request.args.get("cached",default=""),
        request.args.get("ms",default=""),
        request.args.get("error",default=""),
    )
    return Response("true")




@app_redditmetis.route('/api/about/<string:username>')
def about_user(username):
    url = f'https://www.reddit.com/user/{username}/about.json'
    resp = requests.get(url=url,headers = {'User-agent': 'Metis 3'})
    #print(resp.json())
    #return Response(resp.json(), mimetype="application/json")
    return Response(json.dumps(resp.json()), mimetype="application/json")

@app_redditmetis.route('/api/randomcomment')
def get_randomcomment():
    url = "https://www.reddit.com/r/random/comments.json?limit=1"
    resp = requests.get(url=url,headers = {'User-agent': 'Metis 3'})
    return Response(json.dumps(resp.json()), mimetype="application/json")

@app_redditmetis.route('/donate/cancel')
def dmes_cancel():
    return render_template("dmes_cancel.html")

@app_redditmetis.route('/donate/complete')
def dmes_complete():
    return render_template("dmes_cancel.html")

@app_redditmetis.route('/donate')
def donate_message():
    return render_template("donate.html")


@app_redditmetis.route('/user_query')
def user_query():
    
    if request.args.get("cached_json",default=False):
        json_response = open('sample_json/user_query.txt','r').read()
        return Response(json_response, mimetype='text/plain')
    else:
        username = request.args.get("uname", default="")
        tz = request.args.get("tz",default="UTC")
        user = User(username,tz)
        json_response = json.dumps(user.get_json())
        compressed = request.args.get("compressed",default="false").lower()
        if compressed=="true":
            return Response(compress_string(json_response), mimetype='text/plain')
        elif compressed=="false":
            return Response(json_response, mimetype='application/json') 
        else:
            return Response("Invalid value for parameter 'compressed' [true/false]", status_code=400)
    return Response('', status_code=400)


@app_redditmetis.route('/lambda', methods=['POST'])
def local_lambda():
    #print(request.json)
    user = User(None, None, request.json)
    return Response(json.dumps(user.get_json()), mimetype='application/json')
    

@app_redditmetis.route('/improve_data/sentiment', methods=['POST'])
def add_sentiment():
    if request.json["emotion"]!="trash":
        improve_emotion(request.json["text"],request.json["emotion"])
    return Response("thanks, you're awesome!")


@app_redditmetis.route('/cookies')
def cookie_policy_page():
    if (MAINTENANCE):
        return render_template('maintenance.html')
    return render_template("cookiepolicy.html")


@app_redditmetis.route('/about')
def about():
    if (MAINTENANCE):
        return render_template('maintenance.html')
    return render_template("about.html")


@app_redditmetis.route('/faq')
def faq():
    if (MAINTENANCE):
        return render_template('maintenance.html')
    return render_template("faq.html")
















