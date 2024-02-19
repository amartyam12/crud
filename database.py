import psycopg2

hostname = 'localhost'
database = 'database'
username = 'postgres'
pwd = 'qwerty'
port_id = '5432'

try:
    conn = psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id
    )
    conn.close()
    print("not okey+")
except Exception as error:
    print("okey")