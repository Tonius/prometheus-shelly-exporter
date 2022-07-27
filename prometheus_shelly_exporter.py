import os
import traceback
from time import sleep

import requests
from prometheus_client import Gauge, start_http_server


IS_VALID = Gauge(
    "shelly_is_valid",
    "Whether power metering self-checks OK",
)
POWER = Gauge(
    "shelly_power_watts",
    "Current real AC power being drawn, in Watts",
)
TOTAL = Gauge(
    "shelly_total_watt_minutes",
    "Total energy consumed by the attached electrical appliance in Watt-minute",
)


if __name__ == "__main__":
    port = int(os.environ.get("PROMETHEUS_SHELLY_EXPORTER_PORT", "9050"))
    interval = int(os.environ.get("PROMETHEUS_SHELLY_EXPORTER_INTERVAL", "1"))
    shelly_url = os.environ.get("PROMETHEUS_SHELLY_EXPORTER_SHELLY_URL")
    if shelly_url is None:
        raise Exception("No Shelly URL provided")

    start_http_server(port)

    while True:
        try:
            response = requests.get(f"{shelly_url}/meter/0")
            response.raise_for_status()

            data = response.json()

            IS_VALID.set(data["is_valid"])
            POWER.set(data["power"])
            TOTAL.set(data["total"])
        except Exception:
            traceback.print_exc()

        sleep(interval)
