from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_hook import AwsHook

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self,
                 aws_conn_id,
                 redshift_conn_id,
                 table,
                 s3_addr,
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.aws_conn_id = aws_conn_id
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.s3_addr = s3_addr

    def execute(self, context):
        staging_copy = ("""
        COPY {} FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        REGION 'us-west-2'
        {};
        """)
        
        execution_date = context['execution_date']
        self.log.info('StageToRedshiftOperator for {} on {}'.format(self.table, execution_date))

        # load from S3 to redshift
        a_hook = AwsHook(self.aws_conn_id)
        credentials = a_hook.get_credentials()
        s3_addr = self.s3_addr
        
        copy_stmt = staging_copy.format(self.table, s3_addr, 
        credentials.access_key, credentials.secret_key, 
        "JSON 'auto'" if self.table == 'staging_versions' else "IGNOREHEADER 1 CSV")
        
        self.log.info('copy command {}'.format(copy_stmt))
        
        pg_hook = PostgresHook('redshift')
        pg_hook.run(copy_stmt)
        self.log.info('{} loaded'.format(self.table))
