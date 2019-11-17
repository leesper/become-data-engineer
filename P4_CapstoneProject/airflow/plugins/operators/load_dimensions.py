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
            'version_dim': SqlQueries.version_table_select,
            'project_dim': SqlQueries.project_table_select,
            'dependency_dim ': SqlQueries.dependency_table_select,
            'time_dim': SqlQueries.time_table_select,
        }
        pg_hook = PostgresHook('redshift')
        # records = pg_hook.get_records(lookup[self.table])
        # self.log.info('get {} records from {}'.format(len(records), self.table))

        # insert them into corresponding tables
        if self.replace:
            pg_hook.run(f"DELETE FROM {self.table}")
        # pg_hook.insert_rows(self.table, records)
        pg_hook.run(lookup[self.table])
        self.log.info('inserted into {}'.format(self.table))
