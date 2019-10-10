from airflow.models import BaseOperator
from airflow.utils.decorators import apply_default

class StageToRedshiftOperator(BaseOperator):
    
    @apply_default
    def __init__(self):
        pass