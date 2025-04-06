import mysql.connector

# Connect to MySQL (create a connection without specifying a database)
connection = mysql.connector.connect(
    host='localhost',        # Replace with your MySQL server host
    user='root',    # Replace with your MySQL username
    password='Khushi!2005'  # Replace with your MySQL password
)

# Create a cursor object
cursor = connection.cursor()

# Create the database named 'class'
cursor.execute("CREATE DATABASE IF NOT EXISTS class")

# Select the newly created database
cursor.execute("USE class")

# Create the STUDENT table
table_info = """
CREATE TABLE STUDENT (
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
);
"""

cursor.execute(table_info)

# Insert data
# cursor.execute("INSERT INTO STUDENT VALUES('John', 'X', 'A', 90)")
# cursor.execute("INSERT INTO STUDENT VALUES('Jane', 'X', 'B', 80)")
# cursor.execute("INSERT INTO STUDENT VALUES('Doe', 'X', 'C', 75)")
# cursor.execute("INSERT INTO STUDENT VALUES('Smith', 'X', 'A', 90)")
# cursor.execute("INSERT INTO STUDENT VALUES('Johnson', 'X', 'B', 40)")
# cursor.execute("INSERT INTO STUDENT VALUES('Williams', 'X', 'A', 60)")
# cursor.execute("INSERT INTO STUDENT VALUES('Brown', 'X', 'C', 30)")

# Retrieve data
# print("The inserted records are:")

data = cursor.execute("SELECT * FROM STUDENT")
for row in cursor.fetchall():
    print(row)

# Commit the transaction
connection.commit()

# Close the connection
cursor.close()
connection.close()
