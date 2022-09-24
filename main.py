import time
import IServUserAPI
import IServUserAPI.modules
import paho.mqtt.client as mqtt
from datetime import datetime, timedelta
from env import Env


class Client:
    def __init__(self) -> None:
        self.env = Env()
        self.mqtt = mqtt.Client("tt")
        self.iserv = IServUserAPI.Client(self.env.ISERV_URL)


client = Client()


def main():
    client.mqtt.enable_logger()
    client.mqtt.connect("smartalarm.local")
    client.mqtt.loop_start()
    regular_school_start = 28200
    new_school_start = int(datetime.today().strftime("%s"))
    while True:
        if time.time() > new_school_start:
            client.iserv.login(
                username=client.env.ISERV_USERNAME, password=client.env.ISERV_PASSWORD
            )
            # get the timestamp from the start of tomorrow
            date = datetime.today() + timedelta(days=3)
            date = date.replace(hour=0, minute=0, second=0, microsecond=0)

            tt = IServUserAPI.modules.Timetable(
                client=client.iserv,
                startDate=date.strftime("%d.%m.%Y"),
                endDate=date.strftime("%d.%m.%Y"),
            )

            canceled = []
            for change in tt.changes:
                if change["chgdow"] == "0":
                    canceled += change
            print(date.timestamp())
            new_school_start = (
                sort_canceled(canceled) * 2700 + regular_school_start + date.timestamp()
            )
            print(new_school_start)
            client.mqtt.publish(
                topic="timetable/posix", payload=int(new_school_start), retain=True
            )
            client.mqtt.publish(
                topic="timetable/datetime",
                payload=datetime.fromtimestamp(new_school_start).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                retain=True,
            )
            client.iserv.logout()
        else:
            time.sleep(10)


def sort_canceled(c: dict):
    c = sorted(c, key=lambda d: d["period"])
    for i in range(len(c)):
        if c[i]["period"] != i + 1:
            return i
    return 0


if __name__ == "__main__":
    try:
        main()
    finally:
        client.iserv.logout()
        client.mqtt.disconnect()
        client.mqtt.loop_stop()
