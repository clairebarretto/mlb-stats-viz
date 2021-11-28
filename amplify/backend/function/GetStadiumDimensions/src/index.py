import boto3
import csv
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

  team = event['pathParameters']['team'].upper()

  sql = f"""
    SELECT
      Name,
      Location,
      Segment,
      X,
      Y
    FROM
      stadium_dimensions
    WHERE
      TeamShort = "{team}"
  """
  print(f'Sending query: {sql}')

  response = RDS.execute_statement(
    database=config['database'],
    resourceArn=config['cluster_arn'],
    secretArn=config['secret_arn'],
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
        data[columns[i]] = col.get('stringValue')
      rows.append(data)

  print(f'Returning {len(rows)} rows')

  return {
    'statusCode': 200,
    'headers': {
      'Access-Control-Allow-Headers': '*',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    },
    'body': json.dumps(rows)
  }