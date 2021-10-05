import pymysql.cursors
from sshtunnel import SSHTunnelForwarder
import pandas as pd

sql_hostname = '127.0.0.1'
sql_username = 'root'
sql_password = ''
sql_main_database = 'test_db'
sql_port = 3306
ssh_host = '127.0.0.1'
ssh_password=''
ssh_user = 'root'
ssh_port = 22

with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_password=ssh_password,
        remote_bind_address=(sql_hostname, sql_port)) as tunnel:
    connection = pymysql.connect(host='127.0.0.1', user=sql_username,
            passwd=sql_password, db=sql_main_database,
            port=tunnel.local_bind_port)

    with connection:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"

            # Record to execute
            records = [
                ('hamid@anbidev.com', 'no-secret'),
                ('kohendru@anbidev.com', 'admin1234'),
                ('squid@game.com', 'redyellowgreen')
                ]

            cursor.executemany(sql, records)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            
            # Search
            search = ('hamid@anbidev.com')

            cursor.execute(sql, search)
            result = cursor.fetchone()

            print("Searching " + search + " : " + result + "\n")

        with connection.cursor() as cursor:
            # Read all record
            sql = "SELECT * FROM `users`"

            cursor.execute(sql)
            result = cursor.fetchall()
            print("Show all record : " + result)