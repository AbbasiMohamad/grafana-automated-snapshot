import os


APP_NAME = "Grafana Automated Snapshot"
PKG_VERSION = "1.0.0"
USER_HOME = ""
TOKEN = "eyJrIjoiRGxDUHVlM1I5ekc1aFJNdzEwZ2cwTjlMU0xWdnFCVzEiLCJuIjoiYmFja3VwIiwiaWQiOjF9"
GRAFANA_USER = "admin"
GRAFANA_PASSWORD = "grafana"
GRAFANA_ADDRESS = "http://localhost:3000"

if os.name == "nt":
    USER_HOME = os.environ["HOMEPATH"]
else:
    USER_HOME = os.environ["HOME"]
