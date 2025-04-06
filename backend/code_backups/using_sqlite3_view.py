import os
import sqlite3
from dotenv import load_dotenv
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define prompt
PROMPT = [
    """
    You are an expert in converting English Questions to SQL Query!
    The SQL database has the name of the STUDENT and has the following columns - NAME, CLASS, SECTION and MARKS.
    \n\n For Example,
    \n Example 1 - How many entries of records are present?,
    the SQL command will be something like SELECT COUNT(*) FROM STUDENT;
    \n Example 2 - What is the total number of students in each class?,
    the SQL command will be something like SELECT COUNT(*) FROM STUDENT;
    \n Example 3 - What is the total number of students in each section?,
    The SQL query will be something like SELECT section, COUNT(*) AS total_students
                                         FROM STUDENT
                                         GROUP BY section;
    \n Example 4 - Tell me about all the students studying in Data Science Class.
    The SQL command will be something like this SELECT * FROM STUDENT
                                                WHERE CLASS = 'Data Science';   
    \n Example 5 - What is the average marks of students in each class?,
    the SQL command will be something like SELECT AVG(MARKS) FROM STUDENT;

    Also, the SQL code should not have ``` in beginning or end and SQL word in the output.
    """
]

# Function to load Google Gemini model and get SQL query
def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([PROMPT[0], question])
    return response.text

# Function to retrieve query results from SQLite database
def get_sql_response(query, db_name='student.db'):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    data = cursor.execute(query)
    rows = data.fetchall()
    connection.commit()
    connection.close()
    return rows

# API view
class TextToSQLAPIView(APIView):
    def post(self, request):
        question = request.data.get('question')
        if not question:
            return JsonResponse({"error": "Question is required"}, status=400)
        
        # Generate SQL query from question
        sql_query = get_gemini_response(question)
        
        try:
            # Retrieve data from SQLite database
            result = get_sql_response(sql_query)
            return JsonResponse({"query": sql_query, "result": result}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# Home view for root URL
def home_view(request):
    return HttpResponse("Welcome to the Text-to-SQL API")
