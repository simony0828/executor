# executor
What is executor?
It's a YAML Configuration style for ETL pipeline executor/generator build on top of Airflow.  All you need to do is to define column names for the table and business logic (no DML and DDL statements) and the Python framework will auto generate the DAG for different databases without rewriting all pipelines.  Current support is for Snowflake and Presto.
