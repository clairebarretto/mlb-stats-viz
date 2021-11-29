import boto3
import csv
import json
import io
import os
import requests
import time

S3 = boto3.resource('s3')

def handler(event, context):
  print(event)

  mlb_id = event['pathParameters']['player-id']
  yyyymm = 2019

  s3_bucket = 'mlbviz92310-dev'
  s3_prefix = f'statcast/players/{mlb_id}/{yyyymm}/stats.json'

  # Check S3
  s3_obj = None
  result = []
  try:
    s3_obj = S3.Object(s3_bucket, s3_prefix)
    contents = s3_obj.get()['Body'].read().decode('utf-8')
    contents = json.loads(contents)
    if contents:
      result = contents
  except Exception as e:
    # No data on S3
    pass

  # Download data via Baseball Savant
  if not result:
    try:
      local_path = '/tmp/{}.jpg'.format(int(time.time()))

      url = get_external_stats_url(mlb_id, yyyymm)
      url = f'https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7CPO%7CS%7C=&hfSea=&hfSit=&player_type=batter&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=2019-01-01&game_date_lt=2019-12-31&batters_lookup%5B%5D={mlb_id}&team=&position=&hfRO=&home_road=&hfFlag=&metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=pitches&player_event_sort=game_date&sort_order=asc&min_abs=0&type=details'
      print(f'Downloading from url: {url}')

      with requests.get(url, stream=True) as r:
        lines = (line.decode('utf-8') for line in r.iter_lines())

        for row in csv.DictReader(lines):
          result.append(row)

        s3_obj.put(
          Body=json.dumps(result),
          ContentType='application/json',
          CacheControl='max-age=25920000')
    except Exception as e:
      if local_path and os.path.exists(local_path):
          os.remove(local_path)
      print(f'Error: {e}')

  result = filter_results(result)

  return {
    'statusCode': 200,
    'headers': {
      'Access-Control-Allow-Headers': '*',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    },
    'body': json.dumps(result)
  }

def filter_results(result):
  events = [
    "single",
    "double",
    "triple",
    "home_run"
  ]
  fields = [
    "game_date",
    "release_speed",
    "pitcher",
    "events",
    "description",
    "zone",
    "des",
    "stand",
    "p_throws",
    "hit_location",
    "bb_type",
    "hc_x",
    "hc_y",
    "hit_distance_sc",
    "launch_speed",
    "launch_angle",
    "effective_speed",
    "launch_speed_angle",
    "pitch_name"
  ]

  final = []

  for row in result:
    if row.get('events') not in events:
      continue

    temp = {}
    for key, val in row.items():
      if key in fields:
        temp[key] = val
    final.append(temp)

  return final

def get_external_stats_url(mlb_id, yyyymm):
  start_date = '2019-01-01'
  end_date = '2019-12-31'
  return f"""
    https://baseballsavant.mlb.com/statcast_search/csv?all=true
      &hfPT=
      &hfAB=
      &hfBBT=
      &hfPR=
      &hfZ=
      &stadium=
      &hfBBL=
      &hfNewZones=
      &hfGT=R%7CPO%7CS%7C=
      &hfSea=
      &hfSit=
      &player_type=batter
      &hfOuts=
      &opponent=
      &pitcher_throws=
      &batter_stands=
      &hfSA=
      &game_date_gt={start_date}
      &game_date_lt={end_date}
      &batters_lookup%5B%5D={mlb_id}
      &team=
      &position=
      &hfRO=
      &home_road=
      &hfFlag=
      &metric_1=
      &hfInn=
      &min_pitches=0
      &min_results=0
      &group_by=name
      &sort_col=pitches
      &player_event_sort=game_date
      &sort_order=asc
      &min_abs=0
      &type=details
  """