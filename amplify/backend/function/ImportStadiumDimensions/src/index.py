import csv
import boto3
import json

RDS = boto3.client('rds-data')


def handler(event, context):
  print(event)

  # DROP TABLE
  sql = """
    DROP TABLE IF EXISTS stadium_dimensions;
  """
  print(f'Sending query: {sql}')

  RDS.execute_statement(
    database='mlb',
    resourceArn='arn:aws:rds:us-west-2:706698525731:cluster:mlb-stats-viz',
    secretArn='arn:aws:secretsmanager:us-west-2:706698525731:secret:rds-db-credentials/cluster-NLZRMXYZHC3M4RSUC5AZDILPAY/admin-ZBaoIB',
    sql=sql
  )

  # CREATE TABLE
  sql = """
    CREATE TABLE stadium_dimensions (
      ID int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
      Team varchar(30) NOT NULL,
      X DECIMAL(15, 2) NOT NULL,
      Y DECIMAL(15, 2) NOT NULL,
      Segment varchar(50) NOT NULL,
      Name varchar(100) NOT NULL,
      Location varchar(100) NOT NULL
    );
  """
  print(f'Sending query: {sql}')

  RDS.execute_statement(
    database='mlb',
    resourceArn='arn:aws:rds:us-west-2:706698525731:cluster:mlb-stats-viz',
    secretArn='arn:aws:secretsmanager:us-west-2:706698525731:secret:rds-db-credentials/cluster-NLZRMXYZHC3M4RSUC5AZDILPAY/admin-ZBaoIB',
    sql=sql
  )

  # IMPORT DATA
  with open('mlbstadiums.csv') as file:
    reader = csv.reader(file, delimiter=',')

    header = None
    values = []
    for row in reader:
      if header is None:
        header = row
        continue

      values.append('("{}", "{}", "{}", "{}", "{}", "{}")'.format(
        row[1],
        row[2],
        row[3],
        row[4],
        row[5],
        row[6]
      ))

    # looping till length l
    for i in range(0, len(values), 10):
        items = values[i:i + 10]

        sql = """
          INSERT INTO stadium_dimensions (Team, X, Y, Segment, Name, Location)
          VALUES {};
        """.format(','.join(items))
        print(f'Sending query: {sql}')

        RDS.execute_statement(
          database='mlb',
          resourceArn='arn:aws:rds:us-west-2:706698525731:cluster:mlb-stats-viz',
          secretArn='arn:aws:secretsmanager:us-west-2:706698525731:secret:rds-db-credentials/cluster-NLZRMXYZHC3M4RSUC5AZDILPAY/admin-ZBaoIB',
          sql=sql
        )

  return {
    'statusCode': 200,
    'headers': {
      'Access-Control-Allow-Headers': '*',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    },
    'body': json.dumps('Hello from your new Amplify Python lambda!')
  }