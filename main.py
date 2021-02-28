import argparse
import mariadb
import random
import sys

parser = argparse.ArgumentParser(description='Generate erd diagram from sql database.')
parser.add_argument('--user',
        metavar='-u',
        type=str,
        default='root',
        help='user')

parser.add_argument('--password',
        metavar='-p',
        type=str,
        default='',
        help='password')

parser.add_argument('--host',
        metavar='-h',
        type=str,
        nargs=1,
        default='localhost',
        help='host')

parser.add_argument('--port',
        metavar='-P',
        type=int,
        default=3306,
        help='port')

parser.add_argument('--database',
        metavar='-db',
        required=True,
        type=str,
        help='database')

parser.add_argument('--color',
        metavar='-c',
        default='#ffffff',
        type=str,
        help='database')

args = parser.parse_args()

try:
    conn = mariadb.connect(
        user=args.user,
        password=args.password,
        host=args.host,
        port=args.port,
        database=args.database)
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()
cur.execute("SELECT * FROM information_schema.tables WHERE table_schema=?", (args.database,))

tables = list(map(lambda x: x[2], cur))

for table in tables:
    print(f'[{table}] {{bgcolor: "{args.color}"}}')
    cur.execute(f"DESCRIBE {table}")
    for (column_name, column_type, null, key_type, default, extra) in cur:
        key_type = '*' if key_type == 'PRI' else '' if not key_type else '+'
        if default is None:
            default = 'null'
        if extra == 'auto_increment': 
            default += ', auto increment'
        print(f'\t{key_type}{column_name} {{label: "[{column_type}, default {default}]"}}')

cur.execute("SELECT table_name, referenced_table_name, constraint_name FROM information_schema.KEY_COLUMN_USAGE WHERE table_schema=?;", (args.database,))

constraints = list(cur)

for (table_name, referenced_table_name, constraint_name) in constraints:
    if constraint_name != 'PRIMARY' and referenced_table_name != None:
        if random.random() > 0.5:
            print(table_name, '*--1', referenced_table_name)
        else:
            print(referenced_table_name, '1--*', table_name)
