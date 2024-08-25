import requests
from requests.exceptions import ConnectionError
import json
import os
import time
import math
import datetime


def clear():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

api = "https://vl.se/api/realtimeapi/NextDeparturesTrafficInfoByStopCode/"
stop_code = "360107"

def fetchData():
    res = json.loads(requests.get(api + stop_code).text)['Realtime']
    bus_times = {}
    for index, direction in enumerate(res):
        bus_times[direction['results'][0]['stop_name']] = direction['results'][0]
    return bus_times

def time_string(time_code: int, time: str):
    if time_code == 1:
        return time.lower()
    elif time_code == 2:
        return f"om {time.replace('min', '')} minuter"
    elif time_code == 3:
        return f"klockan {time}"
    else:
        return "Kontakta Dennis C i 220S ifall detta meddelande visas."

def problemmeddelande(bus: dict):
    print(f"Oj, oj, det här problemet har kommit upp med bussen ovan: {bus['deviation_message']}") if bus['deviation_message'] else ""

def choose_sleep(bus: dict):
    if bus['time_type'] == 3:
        bus_time = bus['departure_time']
        hour = bus_time[0:2]
        minute = bus_time[3:5]
        time_delta =  datetime.datetime.combine(datetime.datetime.now(), datetime.time(hour=int(hour), minute=int(minute))) - datetime.datetime.now()
        return (math.floor(time_delta.total_seconds() / 60)-10)*60 if math.floor(time_delta.total_seconds() / 60) > 10 else 60
    else:
        return 60

def main():
    clear()
    while True:
        current_data = fetchData()["Brottberga via Centrum"]
        next_bus = current_data['next']
        following_bus = current_data['following']
        clear()
        print(f"Nästa buss mot stan kommer {time_string(next_bus['time_type'], next_bus['departure_time'])}")
        problemmeddelande(next_bus)
        print(f"Bussen efter kommer {time_string(following_bus['time_type'], following_bus['departure_time'])}")
        problemmeddelande(following_bus)
        time.sleep(choose_sleep(next_bus))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        clear()
        exit()
    except ConnectionError as e:
        clear()
        print("Error connecting:", e)