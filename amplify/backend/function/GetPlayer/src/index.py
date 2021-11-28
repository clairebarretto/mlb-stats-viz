import boto3
import json

RDS = boto3.client('rds-data')


def handler(event, context):
  print(event)
  print(context)

  # Move to .env
  config = {
    "database": "mlb",
    "cluster_arn": "arn:aws:rds:us-west-2:706698525731:cluster:mlb-stats-viz",
    "secret_arn": "arn:aws:secretsmanager:us-west-2:706698525731:secret:rds-db-credentials/cluster-NLZRMXYZHC3M4RSUC5AZDILPAY/admin-ZBaoIB"
  }

  player_id = event['pathParameters']['player-id'].upper()

  sql = f"""
    SELECT
      MLBID,
      LahmanID,
      FullName,
      Position,
      TeamShort,
      TeamLong,
      Bats,
      Throws,
      Birthday,
      Debut,
      ActionPhotoUrl,
      HeadshotPhotoUrl
    FROM
      players
    WHERE
      MLBID = "{player_id}"
  """
  print(f'Sending query: {sql}')

  response = RDS.execute_statement(
    database=config['database'],
    resourceArn=config['cluster_arn'],
    secretArn=config['secret_arn'],
    sql=sql,
    includeResultMetadata=True
  )
  print(json.dumps(response, indent=4))

  data = {}
  if response['records']:
    # Get column names
    columns = []
    for column in response['columnMetadata']:
      columns.append(column['name'])

    # Map row values to column names
    for i, col in enumerate(response['records'][0]):
      data_type = list(col.keys())[0]
      if data_type == 'isNull':
        data[columns[i]] = None
      else:
        data[columns[i]] = col.get(data_type)

  print(f'Returning data: {data}')

  return {
    'statusCode': 200,
    'headers': {
      'Access-Control-Allow-Headers': '*',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    },
    'body': json.dumps(data)
  }