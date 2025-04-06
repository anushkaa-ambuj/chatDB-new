import sqlite3

# Step 1: Connect to the SQLite database
conn = sqlite3.connect('student.db')  # Replace 'student.db' with your database file

# Step 2: Create a cursor object
cursor = conn.cursor()

# Step 3: Execute a SQL query
# For example, to select all records from the STUDENT table
cursor.execute("SELECT COUNT(*) FROM STUDENT")

# Step 4: Fetch all results
rows = cursor.fetchall()

# Step 5: Print the fetched data
for row in rows:
    print(row)

# Step 6: Close the cursor and connection
cursor.close()
conn.close()
