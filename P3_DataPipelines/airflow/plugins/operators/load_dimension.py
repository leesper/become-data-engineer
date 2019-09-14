from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

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
            'users': SqlQueries.user_table_insert,
            'songs': SqlQueries.song_table_insert,
            'artists': SqlQueries.artist_table_insert,
            'time': SqlQueries.time_table_insert,
        }
        pg_hook = PostgresHook('redshift')
        records = pg_hook.get_records(lookup[self.table])
        self.log.info('get {} records from {}'.format(len(records), self.table))

        # insert them into corresponding tables
        pg_hook.insert_rows(self.table, records, replace=self.replace)
        self.log.info('inserted into {}'.format(self.table))
