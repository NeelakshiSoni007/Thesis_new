import os
import sys
import json
import logging
from datetime import datetime  # Added datetime import

import requests
from flask import make_response

# Disable console messages from Flask server
logging.getLogger('werkzeug').setLevel(logging.ERROR)

class Log:  # Changed class name to uppercase
    def __init__(self, service_name):
        self.service_name = service_name
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        # Create console handler
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(filename)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # Install service-wide exception handler
        # sys.excepthook = self.my_handler

    # Handle all uncaught exceptions
    def my_handler(self, type, value, tb):
        self.logger.exception("Uncaught exception:", exc_info=(type, value, tb))

def get_env_var(varName, defaultVal):
    """Resolve the environment variables if any.

    Translate string variables into boolean variables."""
    varVal = os.getenv(varName, defaultVal)
    if varVal == 'True':
        varVal = True
    elif varVal == 'False':
        varVal = False
    return varVal

def is_docker():
    """Determines if we are running inside Docker.

    The process's PID inside the container differs from it's PID on the host
    (a non-container system).
    """
    procList = ""
    if os.path.isfile('/proc/1/cgroup'):
        with open('/proc/1/cgroup', 'rt') as f:
            procList = f.read()
    procList = procList.lower()
    checks = [
        'docker' in procList,
        '/lxc/' in procList,
        procList and procList.split()[0] not in ('systemd', 'init',),
        os.path.exists('/.dockerenv'),
        os.path.exists('/.dockerinit'),
        os.getenv('container', None) is not None
    ]
    return any(checks)

def all_links(app):
    links = []
    for rule in app.url_map.iter_rules():
        links.append(str(rule))
    return links
def nice_json(jsonData, statusCode):
    """Form JSON responses."""
    response = make_response(json.dumps(jsonData, sort_keys=True, indent=4, default=json_serial), statusCode)
    response.headers['Content-type'] = "application/json"
    return response


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")

class Requests:
    """Requests+session."""
    def __init__(self):
        self.s = requests.Session()

    def get(self, *args, **kwargs):
        return self.s.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.s.post(*args, **kwargs)
