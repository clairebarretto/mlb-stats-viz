import boto3
import csv
import json

RDS = boto3.client('rds-data')


def handler(event, context):
  print(event)

  # Init RDS config
  config_file = {}
  with open('../../connection/config.json') as file:
    config_file = json.loads(file.read())
  config = config_file['rds']['mlb']

  # DROP TABLE
  sql = """
    DROP TABLE IF EXISTS players;
  """
  print(f'Sending query: {sql}')

  RDS.execute_statement(
    database=config['database'],
    resourceArn=config['cluster_arn'],
    secretArn=config['secret_arn'],
    sql=sql
  )

  # CREATE TABLE
  sql = """
    CREATE TABLE players (
      `MLBID` int unsigned NOT NULL PRIMARY KEY,
      `LahmanID` varchar(30) DEFAULT NULL,
      `FullName` varchar(200) DEFAULT NULL,
      `Position` varchar(2) DEFAULT NULL,
      `TeamShort` varchar(3) DEFAULT NULL,
      `TeamLong` varchar(100) DEFAULT NULL,
      `Bats` varchar(1) DEFAULT NULL,
      `Throws` varchar(1) DEFAULT NULL,
      `Birthday` date DEFAULT NULL,
      `Debut` date DEFAULT NULL,
      `ActionPhotoUrl` text DEFAULT NULL,
      `HeadshotPhotoUrl` text DEFAULT NULL
    );
  """
  print(f'Sending query: {sql}')

  RDS.execute_statement(
    database=config['database'],
    resourceArn=config['cluster_arn'],
    secretArn=config['secret_arn'],
    sql=sql
  )

  # IMPORT DATA
  with open('players.csv') as file:
    reader = csv.reader(file, delimiter=',')

    header = None
    values = []
    for row in reader:
      if header is None:
        header = row
        continue

      birthday = '0000-00-00'
      if row[7]:
        bday_parts = row[7].split('/')
        birthday = '{}-{}-{}'.format(
          bday_parts[2],
          bday_parts[0],
          bday_parts[1])

      debut = '0000-00-00'
      if row[26]:
        debut_parts = row[26].split('/')
        debut = '{}-{}-{}'.format(
          debut_parts[2],
          debut_parts[0],
          debut_parts[1])

      values.append('("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(
        row[0] or 'NULL',
        row[20] or 'NULL',
        row[1] or 'NULL',
        row[2] or 'NULL',
        row[3] or 'NULL',
        row[4] or 'NULL',
        row[5] or 'NULL',
        row[6] or 'NULL',
        birthday,
        debut
      ))

    # looping till length l
    for i in range(0, len(values), 10):
        items = values[i:i + 10]

        sql = """
          INSERT INTO players (
            MLBID,
            LahmanID,
            FullName,
            Position,
            TeamShort,
            TeamLong,
            Bats,
            Throws,
            Birthday,
            Debut
          )
          VALUES {};
        """.format(','.join(items))
        print(f'Sending query: {sql}')

        RDS.execute_statement(
          database=config['database'],
          resourceArn=config['cluster_arn'],
          secretArn=config['secret_arn'],
          sql=sql
        )

  return {
    'statusCode': 200,
    'headers': {
      'Access-Control-Allow-Headers': '*',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    },
    'body': 'Finished importing players'
  }