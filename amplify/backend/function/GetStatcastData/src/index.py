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
  ab_events_exclude = [
    "walk",
    "hit_by_pitch",
    "sac_fly"
  ]
  hit_events = [
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

  return_data = {
    'day': {},
    'total': {},
    'hits': []
  }

  for row in result:
    event = row.get('events')
    day = row.get('game_date')

    if not event:
      continue

    # By day
    if day not in return_data['day']:
      return_data['day'][day] = {}
    if event not in return_data['day'][day]:
      return_data['day'][day][event] = 0
    if 'hit' not in return_data['day'][day]:
      return_data['day'][day]['hit'] = 0
    if 'pa' not in return_data['day'][day]:
      return_data['day'][day]['ab'] = 0
      return_data['day'][day]['pa'] = 0
    return_data['day'][day][event] += 1
    return_data['day'][day]['pa'] += 1

    # Total
    if event not in return_data['total']:
      return_data['total'][event] = 0
    if 'hit' not in return_data['total']:
      return_data['total']['hit'] = 0
    if 'pa' not in return_data['total']:
      return_data['total']['ab'] = 0
      return_data['total']['pa'] = 0
    return_data['total'][event] += 1
    return_data['total']['pa'] += 1

    # At bats
    if event not in ab_events_exclude:
      return_data['day'][day]['ab'] += 1
      return_data['total']['ab'] += 1

    # Hits
    if event in hit_events:
      return_data['day'][day]['hit'] += 1
      return_data['total']['hit'] += 1

      filtered = {}
      for key, val in row.items():
        if key in fields:
          filtered[key] = val
      return_data['hits'].append(filtered)

  # Total averages
  return_data['total']['g'] = compute_metric('g', return_data['days'])
  return_data['total']['avg'] = compute_metric('avg', return_data['total'])
  return_data['total']['slg'] = compute_metric('slg', return_data['total'])
  return_data['total']['obp'] = compute_metric('obp', return_data['total'])
  return_data['total']['ops'] = compute_metric('ops', return_data['total'])

  return return_data


def compute_metric(metric, stats):
  """

  """
  value = ''

  # https://www.mlb.com/glossary/standard-stats


  ab = stats.get('ab') or 0
  bb = stats.get('walk') or 0
  double = stats.get('double') or 0
  hbp = stats.get('hit_by_pitch') or 0
  hits = stats.get('hit') or 0
  hr = stats.get('home_run') or 0
  obp = stats.get('obp') or 0
  pa = stats.get('pa') or 0
  sf = stats.get('sac_fly') or 0
  slg = stats.get('slg') or 0
  single = stats.get('single') or 0
  triple = stats.get('triple') or 0

  if metric == 'avg':
    value = '0.000'
    if hits and ab:
      value = hits / ab
      value = '{:.3f}'.format(value)

  if metric == 'ab':
    value = 0
    if pa:
      value = pa - bb - hbp - sf

  if metric == 'g':
    value = len(stats.keys())

  if metric == 'obp':
    value = '0.000'
    if ab:
      value = (hits + bb + hbp) / (ab + bb + hbp + sf)
      value = '{:.3f}'.format(value)

  if metric == 'slg':
    value = '0.000'
    if ab:
      value = (single + (double * 2) + (triple * 3) + (hr * 4)) / ab
      value = '{:.3f}'.format(value)

  if metric == 'ops':
    value = float(obp) + float(slg)
    value = '{:.3f}'.format(value)

  return value

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