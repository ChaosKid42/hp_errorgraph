#!/usr/bin/env python
import os
import requests
from datetime import datetime
from dateutil import tz

HA_BASEURL = os.environ['WPEG_HA_BASEURL']
HA_ACCESS_TOKEN = os.environ['WPEG_HA_ACCESS_TOKEN']
HA_TIMESTAMP_FROM = os.environ['WPEG_HA_TIMESTAMP_FROM']
HA_TIMESTAMP_TO = os.environ['WPEG_HA_TIMESTAMP_TO']
HA_ENTITY_ID = os.environ['WPEG_HA_ENTITY_ID']
HA_TEMPERATURE_ENTITY_ID = os.environ['WPEG_HA_TEMPERATURE_ENTITY_ID']

with requests.Session() as s:
    s.headers = {
        'Authorization': f'Bearer {HA_ACCESS_TOKEN}',
        'content-type': 'application/json',
    }

    response = s.get(f'{HA_BASEURL}/api/logbook/{HA_TIMESTAMP_FROM}',
                     params={
                         'entity': HA_ENTITY_ID,
                         'end_time': HA_TIMESTAMP_TO
                         }).json()
    for entry in response:
        if entry['state'] != 'unknown' and entry['state'] != 'unavailable':
            temp = s.get(f'{HA_BASEURL}/api/history/period/{entry['when']}',
                        params={
                         'filter_entity_id': HA_TEMPERATURE_ENTITY_ID,
                        }).json()
            when = datetime.fromisoformat(entry['when']).astimezone(tz.tzlocal())
            print(f'{when} {entry['state']} {temp[0][0]['state']}')
