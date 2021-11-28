import json


class RDSConnection(object):
    config = {}

    @staticmethod
    def init(database):
      config_file = open('config.json')
      config_file = json.loads(config_file)

      if not config_file.get('rds'):
        raise Exception('Misconfigured rds config file')
      if not config_file['rds'].get(database):
        raise Exception(f'No database config for {database}')

      rds = config_file['rds'][database]
      RDSConnection.config[database]['database'] = rds.get('database')
      RDSConnection.config[database]['cluster_arn'] = rds.get('cluster_arn')
      RDSConnection.config[database]['secret_arn'] = rds.get('secret_arn')

    @staticmethod
    def execute(database, query):
        """Create a new connection to a host.

        Args:
            key: A host name that should match the .env config.

        Returns:
            A PyMySQL object.

        Raises:
            NameError: Could not find the host in the .env config.
        """
        print(f'Running query: {query}')

        if not RDS.config.get(database):
          RDS.init(database)

        response = RDS.execute_statement(
          database=RDS.config['database'],
          resourceArn=RDS.config['cluster_arn'],
          secretArn=RDS.config['secret_arn'],
          sql=query
        )
        print(f'Result of query: {response}')

        return response
