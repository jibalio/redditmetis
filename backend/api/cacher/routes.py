# Standard library imports
import json

from flask import Blueprint, request, Response

from libraries.cacher.cacher import get_user_result, try_add_key
from libraries.constants import SETTINGS, LOADCACHE

api_cacher = Blueprint(
    'api_cacher', 
    __name__,
    template_folder='templates',
    static_folder='static',
)


@api_cacher.route('/api/check/<string:username>')
def check(username):
    result = get_user_result(username+SETTINGS["cacher"]["lambda_results_tag"])
    timestamps = get_user_result(username+SETTINGS["cacher"]["postTimestamps_tag"])
    result = {
        "username":username,
        "exists":bool(result) and LOADCACHE,
        "result":result,
        "postTimestamps":timestamps,
    }
    return Response(json.dumps(result), mimetype="application/json")

@api_cacher.route("/api/load/<string:username>")
def load_cache(username):
    return Response(json.dumps({"data":get_user_result(username+"$bin_v4")}), mimetype="application/json")

@api_cacher.route("/api/save", methods=['POST'])
def save_cache():
    username = request.json["u"]
    b = request.json["b"]
    ts = request.json["ts"]
    try_add_key(username+"$bin_v4", b)
    try_add_key(username+"$ts_v4", ts)
    return Response("true")