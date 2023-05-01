import datetime
from constants import (TOKEN, GRAFANA_USER, GRAFANA_PASSWORD, GRAFANA_ADDRESS)
import requests
import json
import logging as logger
import sys


class GrafanaSDK:
    def __init__(self):
        logger.basicConfig(filename='app.log', filemode='a',
                           format='%(levelname)s - %(asctime)s - %(message)s')
        logger.warning('This will get logged to a file')
        self.api_key = "Bearer {0}".format(TOKEN)
        self.grafana_address = self.make_grafana_url(
            GRAFANA_ADDRESS, GRAFANA_USER, GRAFANA_PASSWORD)
        # if self.check_grafana_is_available():
        #     logger.info("all things about grafana is okay!")
        # else:
        #     logger.critical(
        #         "Grafana is not available, make sure about url and credential")
        #     sys.exit(1)

    def make_grafana_url(self, url, username, password):
        if url.startswith("https:"):
            address = url[7:]
            return "https://{0}:{1}@{2}".format(username, password, address)
        elif url.startswith("http:"):
            address = url[7:]
            return "http://{0}:{1}@{2}".format(username, password, address)
        else:
            print("nothing")

    def get_all_dashboards(self):
        search_dashboard_url = "/api/search?folderIds=0&query=&starred=false"
        payload = {}
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': self.api_key
        }
        try:
            result = requests.request(
                "GET", self.grafana_address + search_dashboard_url,
                headers=headers, data=payload)
        except:
            result = []
        return json.loads(result.content)

    def get_all_dashboard_models(self, dashboards):
        dashboard_model_url = "/api/dashboards/uid/"  # + dashboard uid
        payload = {}
        dashboard_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': self.api_key
        }
        list_of_dashboard_model = []
        for i in dashboards:
            dashboard_model = requests.request(
                "GET", self.grafana_address + dashboard_model_url + i["uid"], headers=dashboard_headers, data=payload)
            list_of_dashboard_model.append(json.loads(dashboard_model.content))
        return list_of_dashboard_model

    def create_snapshots(self, models):
        snapshot_url = "/api/snapshots"
        snapshot_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': self.api_key
        }
        created_snapshot = []
        for i in models:
            dashboard_model = i["dashboard"]
            dashboard_model["time"] = {
                "from": "now-7d",
                "to": "now"
            }
            snapshot_name = self.make_snapshot_name(dashboard_model["title"])
            if self.check_if_snapshots_is_not_exists(snapshot_name):
                snapshot_payload = json.dumps(
                    {"dashboard":  dashboard_model, "name": snapshot_name})
                response = requests.request(
                    "POST", self.grafana_address + snapshot_url, headers=snapshot_headers, data=snapshot_payload)
                if (response.status_code == 200):
                    created_snapshot.append(response.content)

        return created_snapshot

    def check_if_snapshots_is_not_exists(self, snapshot_name):
        search_dashboard_url = "/api/dashboard/snapshots"
        payload = {}
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': self.api_key
        }
        result = requests.request(
            "GET", self.grafana_address + search_dashboard_url,
            headers=headers, data=payload)
        snapshots = json.loads(result.content)
        for i in snapshots:
            if snapshot_name == i["name"]:
                return False
        return True

    def make_snapshot_name(self, dashboard_name):
        year, week, day = datetime.date.today().isocalendar()
        return dashboard_name + "-" + str(year) + "-" + str(week)

    def check_grafana_is_available(self):
        pass


grafana = GrafanaSDK()
dashboards = grafana.get_all_dashboards()
models = grafana.get_all_dashboard_models(dashboards)
snapshots = grafana.create_snapshots(models)
print(snapshots)
