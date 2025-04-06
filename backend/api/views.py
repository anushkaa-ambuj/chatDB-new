import os
import mysql.connector
from dotenv import load_dotenv
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define prompt
# For class database
# PROMPT = [
#     """
#     You are an expert in converting English Questions to SQL Query!
#     The SQL database is named university and has the following tables: classroom, course, department, grade_points, instructor, prereq, section, student, takes, teaches, time_slot.
    
#     \n\n For Example,
#     \n Example 1 - How many records are present in the database?,
#     the SQL command will be something like SELECT COUNT(*) FROM STUDENT;
    
#     \n Example 2 - What is the total number of students in each year?,
#     the SQL command will be something like SELECT YEAR, COUNT(*) AS total_students
#                                             FROM STUDENT
#                                             GROUP BY YEAR;
    
#     \n Example 3 - How many students belong to each department?,
#     the SQL command will be something like SELECT DEPARTMENT, COUNT(*) AS total_students
#                                             FROM STUDENT
#                                             GROUP BY DEPARTMENT;
    
#     \n Example 4 - Tell me about all the students studying in the Computer Science department.,
#     the SQL command will be something like SELECT * FROM STUDENT
#                                             WHERE DEPARTMENT = 'Computer Science';
                                            
#     \n Example 5 - What is the average marks scored by students in each city?,
#     the SQL command will be something like SELECT CITY, AVG(MARKS) AS average_marks
#                                             FROM STUDENT
#                                             GROUP BY CITY;
                                            
#     \n Example 6 - Which students are from Bengaluru?,
#     the SQL command will be something like SELECT * FROM STUDENT
#                                             WHERE CITY = 'Bengaluru';

#     Also, the SQL code should not have ``` in the beginning or end and SQL word in the output.
#     """
# ]

# For 'institute' database

PROMPT = [
    """
    You are an expert in converting English questions to SQL queries!  
    The SQL database is named `institute` and has the following tables: `courses`, `instructor`, `student`, `takes`, `teaches`.
    The `courses` table has the following columns: `CID`, `Title`, `Credits`.
    The `instructor` table has the following columns: `IID`, `FName`, `LName`, `Department`.
    The `student` table has the following columns: `SID`, `FName`, `LName`, `Phone`, `GPA`, `Department`, `Joining_Year`, `Passing_Year`.
    The `takes` table has the following columns: `SID`, `CID`, `Semester`.
    The `teaches` table has the following columns: `IID`, `CID`, `Semester`.

    \n\n For Example,  
    \n Example 1 - How many records are present in the STUDENT table?,  
    the SQL command will be something like SELECT COUNT(*) FROM STUDENT;

    \n Example 2 - What is the average GPA of all students?,  
    the SQL command will be something like SELECT AVG(GPA) AS average_gpa FROM STUDENT;

    \n Example 3 - List all courses offered in the Fall 2025 semester.,  
    the SQL command will be something like SELECT CID, Title FROM COURSES  
                                            WHERE CID IN (SELECT CID FROM TEACHES WHERE Semester = 'Fall 2025');

    \n Example 4 - Retrieve all information about students enrolled in 'Data Structures' during Spring 2024.,  
    the SQL command will be something like SELECT S.*  
                                            FROM STUDENT S  
                                            JOIN TAKES T ON S.SID = T.SID  
                                            WHERE T.CID = (SELECT CID FROM COURSES WHERE Title = 'Data Structures')  
                                            AND T.Semester = 'Spring 2024';

    \n Example 5 - Find the names of instructors teaching 'Introduction to Programming'.,  
    the SQL command will be something like SELECT I.LName, I.FName  
                                            FROM INSTRUCTOR I  
                                            JOIN TEACHES T ON I.IID = T.IID  
                                            WHERE T.CID = (SELECT CID FROM COURSES WHERE Title = 'Introduction to Programming');

    \n Example 6 - Count the number of courses taught by each instructor in Fall 2025.,  
    the SQL command will be something like SELECT I.IID, I.LName, I.FName, COUNT(*) AS total_courses  
                                            FROM INSTRUCTOR I  
                                            JOIN TEACHES T ON I.IID = T.IID  
                                            WHERE T.Semester = 'Fall 2025'  
                                            GROUP BY I.IID, I.LName, I.FName;

    The SQL code should not have ``` in the beginning or end and must not include the word "SQL" in the output.
    """
]

# Function to load Google Gemini model and get SQL query
def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content([PROMPT[0], question])
    return response.text

# Function to retrieve query results from MySQL database
def get_sql_response(query):
    # Establish connection to the MySQL database
    connection = mysql.connector.connect(
        host='localhost',        # Replace with your MySQL server host
        user='root',    # Replace with your MySQL username
        password='Khushi!2005', # Replace with your MySQL password
        database='institute'         # Replace with your MySQL database name
    )
    cursor = connection.cursor()
    
    try:
        # Execute the query
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    finally:
        # Commit and close the connection
        connection.commit()
        cursor.close()
        connection.close()

# API view
class TextToSQLAPIView(APIView):
    def post(self, request):
        question = request.data.get('question')
        if not question:
            return JsonResponse({"error": "Question is required"}, status=400)
        
        # Generate SQL query from question
        sql_query = get_gemini_response(question)
        
        try:
            # Retrieve data from MySQL database
            result = get_sql_response(sql_query)
            return JsonResponse({"query": sql_query, "result": result}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# Home view for root URL
def home_view(request):
    return HttpResponse("Welcome to the Text-to-SQL API")
