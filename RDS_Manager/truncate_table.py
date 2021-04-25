"""
Copyright (c) Rubikon Labs Team.

This file is used for drop a db from the RDS database and re-create the same database
"""

# Imports
import pymysql

# RDS DB Credentials
ENDPOINT="jupyter-hub-database.clvep70ziamx.us-east-1.rds.amazonaws.com"
PORT=3306
USR="admin"
REGION="us-east-1"
password="Bk5RIt2wiqzPH5rNqQhB"
DBNAME="jupyterhub_test"

# Try for catching errors if any
try:
    conn =  pymysql.connect(host=ENDPOINT, user=USR, passwd=password, database=DBNAME)
    cur = conn.cursor()
    cur.execute("""SHOW DATABASES""")
    print("Databases:", cur.fetchall(), "\n")
    dbs = input("Enter the DB name that you want to drop: ")
    print(f"Dropping database {dbs}... ", "\n")
    cur.execute(f"""DROP DATABASE IF EXISTS {dbs}""")
    cur.execute("""SHOW DATABASES""")
    print(f"Databases present after dropping {dbs}:", cur.fetchall(), "\n")
    print(f"Creating a new database {dbs}...")
    cur.execute(f"""CREATE DATABASE {dbs}""")
    cur.execute("""SHOW DATABASES""")
    print("Databases present:", cur.fetchall(), "\n")

except Exception as e:
    print("Database connection failed due to {}".format(e))