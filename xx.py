import mysql.connector

db = mysql.connector.connect(
    host='localhost',
    database='Operations',
    user='root',
    password='06021999')
cursor = db.cursor()
#cursor.execute("CREATE DATABASE Operations")
cursor.execute("CREATE TABLE testing (ID INT PRIMARY KEY, NVDA_Value float)")