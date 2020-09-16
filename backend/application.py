# Standard Library
import sys
from pathlib import Path

# Third party imports
from flask import Flask
from diskcache import Cache

# Local application-specific imports
# Routes
from app_redditmetis import routes as app_redditmetis
from api.cacher import routes as api_cacher
from api.subdata import api_subdata
from api.mintgreen import api_mintgreen


DEVELOPMENT = True
APPLICATION_ROOT_PATH = str(Path(__file__).parent.absolute())
LIBRARIES = [
	"auth",
	"metis_core",
	"cacher",
	"glogger",
	"geoip",
	"mintgreen_core"
]


# SQLite Cache for storing user analysis
cache = Cache('cache/')


# Dynamically add local libraries in libraries/ folder
for library in LIBRARIES:
	sys.path.append(f"{APPLICATION_ROOT_PATH}\\libraries\\{library}")


# Flask Application
application = Flask(__name__, instance_relative_config=False)

application.url_map.strict_slashes = False

application.register_blueprint(app_redditmetis.app_redditmetis)
application.register_blueprint(api_cacher.api_cacher)
application.register_blueprint(api_mintgreen)
application.register_blueprint(api_subdata)


if __name__== "__main__":
	application.run(host="0.0.0.0")
