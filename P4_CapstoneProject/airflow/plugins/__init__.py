from airflow.plugins_manager import AirflowPlugin

import operators

# Defining the plugin class
class CapstonePlugin(AirflowPlugin):
    name = "capstone_plugin"
    operators = [
        operators.StageToRedshiftOperator,
        operators.LoadFactOperator,
        operators.LoadDimensionOperator,
        operators.QualityCheckOperator,
    ]
