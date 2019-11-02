from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class QualityCheckOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id,
                 tables,
                 *args, **kwargs):

        super(QualityCheckOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tables = tables

    def execute(self, context):
        self.log.info('QualityCheckOperator for {}'.format(self.tables))
        pg_hook = PostgresHook(self.redshift_conn_id)
        for table in self.tables:
            records = pg_hook.get_records(f"SELECT COUNT(*) FROM {table}")
            if len(records) < 1 or len(records[0]) < 1:
                raise ValueError(f"data quality check failed, {table} returns no results")
            num_records = records[0][0]
            if num_records < 1:
                raise ValueError(f"data quality check failed, {table} contains no records")
            self.log.info(f"data quality check on {table} check passed with {records[0][0]} records")