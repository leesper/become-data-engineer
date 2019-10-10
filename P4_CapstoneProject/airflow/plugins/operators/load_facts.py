from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):
    
    @apply_defaults
    def __init__(self):
        pass