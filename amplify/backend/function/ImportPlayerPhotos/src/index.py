import boto3
import json
import os
import requests
import shutil
import time

S3 = boto3.resource('s3')
RDS = boto3.client('rds-data')

PHOTO_TYPE_ACTION_SHOT = 'action'
PHOTO_TYPE_HEAD_SHOT = 'head'

# Move to .env
CONFIG = {
  "database": "mlb",
  "cluster_arn": "arn:aws:rds:us-west-2:706698525731:cluster:mlb-stats-viz",
  "secret_arn": "arn:aws:secretsmanager:us-west-2:706698525731:secret:rds-db-credentials/cluster-NLZRMXYZHC3M4RSUC5AZDILPAY/admin-ZBaoIB"
}

def handler(event, context):
  print(event)

  sql = """
    SELECT
      MLBID,
      ActionPhotoUrl,
      HeadshotPhotoUrl
    FROM
      players
    WHERE
      Position != "P" -- Do batters only
      AND (ActionPhotoUrl IS NULL OR HeadshotPhotoUrl IS NULL)
    ;
  """
  print(f'Sending query: {sql}')

  response = RDS.execute_statement(
    database=CONFIG['database'],
    resourceArn=CONFIG['cluster_arn'],
    secretArn=CONFIG['secret_arn'],
    sql=sql,
    includeResultMetadata=True
  )

  rows = []
  if response['records']:
    # Get column names
    columns = []
    for column in response['columnMetadata']:
      columns.append(column['name'])

    # Map row values to column names
    for row in response['records']:
      data = {}
      for i, col in enumerate(row):
        data_type = list(col.keys())[0]
        if data_type == 'isNull':
          data[columns[i]] = None
        else:
          data[columns[i]] = col.get(data_type)
      rows.append(data)

    # Check if any photos need to be uploaded
    for row in rows:
      if not row.get('ActionPhotoUrl'):
        sync_photo(PHOTO_TYPE_ACTION_SHOT, row.get('MLBID'))
        pass

      if not row.get('HeadshotPhotoUrl'):
        sync_photo(PHOTO_TYPE_HEAD_SHOT, row.get('MLBID'))

  return {
    'statusCode': 200,
    'headers': {
      'Access-Control-Allow-Headers': '*',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    },
    'body': json.dumps(rows)
  }


def get_external_photo_url(photo_type: str, mlb_id: int) -> str:
  """Get an MLB Advanced Media photo url for the given player.

  Args:
    photo_type: One of the valid photo types. Currently supports "head"
      or "action".
    mlb_id: MLB Advanced Media ID.

  Returns:
    A string repesenting the full photo url.
  """
  if photo_type == PHOTO_TYPE_ACTION_SHOT:
    return f'https://img.mlbstatic.com/mlb-photos/image/upload/w_1500,q_100/v1/people/{mlb_id}/action/hero/current'
  elif photo_type == PHOTO_TYPE_HEAD_SHOT:
    return f'https://img.mlbstatic.com/mlb-photos/image/upload/w_213,q_100/v1/people/{mlb_id}/headshot/67/current'
  return ''


def get_local_photo_url(s3_bucket, s3_prefix):
  """Get
  """
  return f'http://{s3_bucket}.s3.us-west-2.amazonaws.com/{s3_prefix}'


def sync_photo(photo_type, mlb_id):
  """

  """
  s3_bucket = 'mlbviz92310-dev'
  s3_prefix = f'images/players/{mlb_id}/{photo_type}.jpg'

  # Check S3
  photo_url = None
  s3_obj = None
  try:
    s3_obj = S3.Object(s3_bucket, s3_prefix)
    s3_obj.get()

    photo_url = get_local_photo_url(s3_bucket, s3_prefix)
  except Exception as e:
    # No image on S3
    pass

  # Download photo via url
  if not photo_url:
    try:
        local_path = '/tmp/{}.jpg'.format(int(time.time()))

        url = get_external_photo_url(photo_type, mlb_id)
        print(f'Downloading photo: {url}')

        r = requests.get(url, stream=True)
        if r.status_code == 200:
          s3_obj.put(
              Body=r.raw.read(),
              ContentType='image/jpeg',
              CacheControl='max-age=25920000',
              ACL='public-read')
          photo_url = get_local_photo_url(s3_bucket, s3_prefix)
    except Exception as e:
        if local_path and os.path.exists(local_path):
            os.remove(local_path)
        print(f'Error: {e}')

  # Save locally
  if photo_url:
    key = None
    if photo_type == PHOTO_TYPE_ACTION_SHOT:
      key = 'ActionPhotoUrl'
    elif photo_type == PHOTO_TYPE_HEAD_SHOT:
      key = 'HeadshotPhotoUrl'

    sql = f"""
      UPDATE players
      SET `{key}` = "{photo_url}"
      WHERE MLBID = "{mlb_id}"
    """
    print(f'Sending query: {sql}')

    RDS.execute_statement(
      database=CONFIG['database'],
      resourceArn=CONFIG['cluster_arn'],
      secretArn=CONFIG['secret_arn'],
      sql=sql,
      includeResultMetadata=True
    )