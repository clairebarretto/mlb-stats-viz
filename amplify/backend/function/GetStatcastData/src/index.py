import boto3
import calendar
import csv
import datetime
import json
import requests
import urllib

S3 = boto3.resource('s3')

def handler(event, context):
  print(event)

  result = []

  mlb_id = event.get('pathParameters', {}).get('player-id')
  year = event.get('queryStringParameters', {}).get('year') or 2019

  # TODO: Move to .env
  s3_bucket = 'mlbviz92310-dev'
  s3_prefix = f'statcast/players/{mlb_id}/{year}/stats.json'

  # Check S3
  s3_obj = None
  try:
    s3_obj = S3.Object(s3_bucket, s3_prefix)
    contents = s3_obj.get()['Body'].read().decode('utf-8')
    contents = json.loads(contents)
    if contents:
      result = contents
  except Exception as e:
    # No data on S3 - fetch externally
    pass

  # Download data via Baseball Savant
  if not result:
    try:
      # Get stats url
      url = generate_external_stats_url(mlb_id, year)
      print(f'Downloading stats from url: {url}')

      # Query!
      with requests.get(url, stream=True) as r:
        lines = (line.decode('utf-8') for line in r.iter_lines())

        # Convert CSV rows to JSON
        for row in csv.DictReader(lines):
          result.append(row)

        # Cache on S3
        # TODO: Move this to SNS later
        s3_obj.put(
          Body=json.dumps(result),
          ContentType='application/json',
          CacheControl='max-age=25920000')
    except Exception as e:
      print(f'Error: {e}')

  # Filter results down to reduce payload
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


def compute_metric(metric, stats):
  """Compute custom metrics not returned by the Baseball Savant call.

  Calculations: https://www.mlb.com/glossary/standard-stats

  Args:
    metric: The metric to compute.
    stats: A dict containing stats.

  Returns:
    A string representing the computed value.
  """
  value = ''

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

  # AT BATS
  if metric == 'ab':
    value = 0
    if pa:
      value = pa - bb - hbp - sf

  # AVERAGE
  if metric == 'avg':
    value = '0.000'
    if hits and ab:
      value = hits / ab
      value = '{:.3f}'.format(value)

  # GAMES
  if metric == 'g':
    value = len(stats.keys())

  # ON BASE PERCENTAGE
  if metric == 'obp':
    value = '0.000'
    if ab:
      value = (hits + bb + hbp) / (ab + bb + hbp + sf)
      value = '{:.3f}'.format(value)

  # SLUGGING PERCENTAGE
  if metric == 'slg':
    value = '0.000'
    if ab:
      value = (single + (double * 2) + (triple * 3) + (hr * 4)) / ab
      value = '{:.3f}'.format(value)

  # ON BASE + SLUGGING PERCENTAGE
  if metric == 'ops':
    value = float(obp) + float(slg)
    value = '{:.3f}'.format(value)

  return value


def filter_results(result: list) -> dict:
  """Filter the raw response from a Baseball Savant call.

  Args:
    result: The result of a Baseball Savant call.

  Returns:
    A dict containing:
      days: A dict of stats by day.
      total: A dict of total stats by month.
      hits: A list of hits for the month.
  """

  return_data = {
    'day': {},
    'total': {},
    'hits': []
  }

  # A list of events to exclude to sum ABs
  ab_events_exclude = [
    "walk",
    "hit_by_pitch",
    "sac_fly"
  ]

  # A list of events to include to sum Hits
  hit_events_include = [
    "single",
    "double",
    "triple",
    "home_run"
  ]

  # A list of fields to include as part of every hit
  hit_fields_include = [
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

    # By month
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
    if event in hit_events_include:
      return_data['day'][day]['hit'] += 1
      return_data['total']['hit'] += 1

      filtered = {}
      for key, val in row.items():
        if key in hit_fields_include:
          filtered[key] = val
      return_data['hits'].append(filtered)

  # Total averages
  return_data['total']['g'] = compute_metric('g', return_data['day'])
  return_data['total']['avg'] = compute_metric('avg', return_data['total'])
  return_data['total']['slg'] = compute_metric('slg', return_data['total'])
  return_data['total']['obp'] = compute_metric('obp', return_data['total'])
  return_data['total']['ops'] = compute_metric('ops', return_data['total'])

  return return_data


def generate_external_stats_url(mlb_id, year):
  """Generate the Baseball Savant stats url to fetch stats for the given year.

  Args:
    mlb_id: The MLBID of the player to fetch stats for.
    year: 4 digit year.

  Returns:
    A string representing the full url to query.
  """

  print(f'Getting stats for year: {year}')

  if not year:
    raise ValueError('Missing year.')

  year = int(year)

  start_date = datetime.datetime.today().replace(
    year=year, month=1, day=calendar.monthrange(year, 1)[0])
  end_date = datetime.datetime.today().replace(
    year=year, month=10, day=calendar.monthrange(year, 9)[1])

  params = {
    'all': 'true',
    'hfPT': '',
    'hfAB': '',
    'hfBBT': '',
    'hfPR': '',
    'hfZ': '',
    'stadium': '',
    'hfBBL': '',
    'hfNewZones': '',
    'hfGTR|PO|S|': '',
    'hfSea': '',
    'hfSit': '',
    'player_typebatter': '',
    'hfOuts': '',
    'opponent': '',
    'pitcher_throws': '',
    'batter_stands': '',
    'hfSA': '',
    'game_date_gt': start_date,
    'game_date_lt': end_date,
    'batters_lookup[]': mlb_id,
    'team': '',
    'position': '',
    'hfRO': '',
    'home_road': '',
    'hfFlag': '',
    'metric_1': '',
    'hfInn': '',
    'min_pitches': 0,
    'min_results': 0,
    'group_by': 'name',
    'sort_col': 'pitches',
    'player_event_sort': 'game_date',
    'sort_order': 'asc',
    'min_abs': 0,
    'type': 'details',
  }
  query_str = urllib.parse.urlencode(params)

  return f'https://baseballsavant.mlb.com/statcast_search/csv?{query_str}'
