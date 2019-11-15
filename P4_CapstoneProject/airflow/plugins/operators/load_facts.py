from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from helpers import SqlQueries

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id,
                 table,
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table

    def execute(self, context):
        self.log.info('LoadFactOperator for {}'.format(self.table))

        # get records using sql_queries.repository_table_insert
        pg_hook = PostgresHook(self.redshift_conn_id)
        records = pg_hook.get_records(SqlQueries.repository_table_select)
        self.log.info('get {} records from {}'.format(len(records), self.table))

        # insert records into repositories
        pg_hook.insert_rows(self.table, records)
        self.log.info('inserted into {}'.format(self.table))