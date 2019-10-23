from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from helpers import SqlQueries

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id,
                 table,
                 replace=False,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.replace = replace

    def execute(self, context):
        self.log.info('LoadDimensionOperator for {}'.format(self.table))

        # load records using sql_queries
        lookup = {
            'versions': SqlQueries.version_table_insert,
            'projects': SqlQueries.project_table_insert,
            'dependencies': SqlQueries.dependency_table_insert,
            'time': SqlQueries.time_table_insert,
            'stars': SqlQueries.star_table_insert,
        }
        pg_hook = PostgresHook('redshift')
        records = pg_hook.get_records(lookup[self.table])
        self.log.info('get {} records from {}'.format(len(records), self.table))

        # insert them into corresponding tables
        if self.replace:
            pg_hook.run(f"DELETE FROM {self.table}")
        pg_hook.insert_rows(self.table, records)
        self.log.info('inserted into {}'.format(self.table))
