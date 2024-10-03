import os
import logging
import requests
from google.transit import gtfs_realtime_pb2
from requests.auth import HTTPBasicAuth

import azure.functions as func

def main(timer: func.TimerRequest, blobout: func.Out[bytes]):
  feed = gtfs_realtime_pb2.FeedMessage()
  url = 'https://nysse.mattersoft.fi/api/gtfsrealtime/v1.0/feed/tripupdate'
  user_name = os.getenv('LMJ_USER')
  password = os.getenv('LMJ_PASSWORD')
  res = requests.get(url, verify=True, auth=HTTPBasicAuth(user_name, password))
  if res.status_code != 200:
    logging.error(f"----- lmj tripupdate download failed")
    raise Exception("Download Failed")
  feed.ParseFromString(res.content)    
  for entity in feed.entity:
    if entity.HasField('trip_update'):
      tu = entity.trip_update
      for stu in tu.stop_time_update:
        if stu.HasField('schedule_relationship'):
          if stu.schedule_relationship == 2:
            stu.schedule_relationship = 1
  blobout.set(feed.SerializeToString())
  logging.info(f"----- lmj blob updated")