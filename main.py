import datetime
from garafana_sdk import GrafanaSDK


def main():
    year, week, day = datetime.date.today().isocalendar()
    if day == 1:
        grafana = GrafanaSDK()
        dashboards = grafana.get_all_dashboards()
        models = grafana.get_all_dashboard_models(dashboards)
        snapshots = grafana.create_snapshots(models)
        print(snapshots)
