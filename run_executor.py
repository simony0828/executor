import argparse
from ..common.lib.executor import Executor

def parse_args():
    parser = argparse.ArgumentParser(description='ETL framework by reading YAML configuration file')

    parser.add_argument('-f', '--file', action="store", required=True, dest='config_file',
        help="YAML file for running ETL for a single table")
    parser.add_argument('-d', '--dry_run', action="store_true", required=False, dest='dry_run', default=False,
        help="Print all SQLs only")
    parser.add_argument('-s', '--setup', action="store_true", default=False, dest='setup',
        help="Run create tables only (target and staging)")
    parser.add_argument('-p', '--steps', action="store", default=None, dest='steps',
        help="For executing specific steps (comma separated)")
    parser.add_argument('-u', '--unit_test', action="store_true", default=False, dest='unit_test',
        help="Enable data quality check without writing result to table")
    parser.add_argument('-v', '--variable', action="append", required=False, dest='variables', default=[],
        help="For SQL variables replacement")

    return parser.parse_args()

def __main__():
    # Parse command line arguments
    args = parse_args()

    e = Executor(
        yaml_file=args.config_file,
        run_setup=args.setup,
        steps=args.steps,
        is_dry_run=args.dry_run,
        is_unit_test=args.unit_test,
        variables=args.variables,
        )

    e.run_etl()


__main__()
