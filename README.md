# executor
What is executor?
It's a YAML Configuration style for ETL pipeline executor/generator build on top of Airflow.  All you need to do is to define column names for the table and business logic (no DML and DDL statements) and the Python framework will auto generate the DAG for different databases without rewriting all pipelines.  Current support is for Snowflake and Presto.

# how it works
Using the YAML configuration like this format:
```
database:
  type: snowflake

target_table:
  name: schema.table
  columns:
    skey: {type: bigint, pii: false, description: "surrogate key"}
    col1: {type: string, pii: false, description: "column 1"}
    col2: {type: string, pii: false, description: "column 2"}
  primary_key:
    - skey
  partition_key:
    - year
    - month
    - day

source_tables:
  name:
    - schema.table1
    - schema.table2

staging_tables:
  - name: stg_schema.stg_step2
    columns:
      col1: {type: bigint, pii: false, description: "column 1"}
      col2: {type: bigint, pii: false, description: "column 2"}
  - name: stg_schema.stg_step3
    columns:
      col1: {type: bigint, pii: false, description: "column 1"}
      col2: {type: bigint, pii: false, description: "column 2"}

wait_for:
  file: table-watcher.yaml

etl:
  tmp_step1:
    description: tmp = create tmp table or drop/create
    enabled: true
    sql: |
      select
        order_id,
        {% set payment_methods = ["bank_transfer", "credit_card", "gift_card"] %}
        {% for payment_method in payment_methods %}
        sum(case when payment_method = '{{payment_method}}' then amount end) as {{payment_method}}_amount,
        {% endfor %}
      from
        xxx

  stg_step2:
    description: stg = delete/insert
    delete: <where clause>
    sql: |
      select
      ...
      from
        {{ tmp_step1 }}

  stg_step3:
    description: stg = delete/insert
    delete: <where clause>
    sql: |
      select
      ...
      from
        {{ stg_step2 }}
        join {{ tmp_step1 }} using (col1)

  target_table:
    description: based on the mode
    #mode: overwrite | append | update
    mode: overwrite
    from: "{{ stg_step3 }}"

dq:
  file: table-DQ.yaml
```
Detail for execution:
- **target_table:** Defines the DDL for the table
- **source_tables:** List of source tables depend on (for generate lineage)
- **wait_for:** Another Python framework to wait for a list of tables to start ETL
- **etl:** ETL steps for the table but only the select statement, no INSERT/UPDATE/MERGE/DELETE and uses jinja2 syntax for even more dynamic coding

# how to run
```
python3 run_executor.py -f <file> [--dry_run] [--unit_test] [--setup] [--steps] [--variable k1=v1] [--variable k2=v2] ...
```

> **--file / -f:**	The YAML configuration file containing all the data quality checks
> 
> **--dry_run / -d:**	Print all SQLs without executing in the system
> 
> **--unit_test / -u:**	Enable data quality check without writing result to table
> 
> **--setup / -s:**	Run create tables only (target and staging)
> 
> **--variable / -v:**	A variable list for string substitution
