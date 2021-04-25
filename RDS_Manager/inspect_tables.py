"""
Copyright (c) Rubikon Labs Team.

This file is used for making a SQL query to the selected RDS database
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

try:
    conn =  pymysql.connect(host=ENDPOINT, user=USR, passwd=password, database=DBNAME)
    cur = conn.cursor()
    cur.execute("""SHOW DATABASES""")
    print("Available Databases: ", cur.fetchall(), "\n")
    dbs = input("Enter the DB name: ")
    cur.execute(f"""USE {dbs}""")
    print("\n")
    print(f"Using database '{dbs}'...")
    cur.execute("""SHOW TABLES""")
    print(f"Tables present in {dbs}:", "\n")
    print(cur.fetchall())
    contin = "y"
    while(contin=="y"):
        print("\n")
        query = input("Enter SQL Query: ")
        print(f"Executing: {query}...")
        cur.execute(f"""{query}""")
        print("Output: \n")
        print(cur.fetchall())
        print("\n")
        contin=input("Continue? [y/n]")

except Exception as e:
    print("Database connection failed due to {}".format(e))