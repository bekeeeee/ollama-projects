# import sqlite3
# from langchain.tools import Tool

# conn = sqlite3.connect("db.sqlite")


# def run_sqlite_query(query):
#     print(f"Running query^^^^^^^^^^^^^^^^^^^^^^^: {query}")
#     c = conn.cursor()
#     c.execute(query)
#     return c.fetchall()


# run_query_tool = Tool.from_function(
#     name="run_sqlite_query", description="Run a sqlite query.", func=run_sqlite_query
# )


# def get_run_query_tool():
#     return Tool.from_function(
#         name="run_sqlite_query",
#         description="Run a SQLite query to retrieve data from the database. Use this tool for questions about user data, such as counting users or retrieving specific information.",
#         func=run_sqlite_query,
#     )


# def run_sqlite_query_2(action_input):
#     try:
#         print(f"Running query^^^^^^^^^^^^^^^^^^^^^^^: {action_input}")
#         # Handle both string and JSON input
#         if isinstance(action_input, str):
#             query = action_input
#         elif isinstance(action_input, dict):
#             query = action_input.get("query", "")
#         else:
#             return "Invalid input format"

#         c = conn.cursor()
#         c.execute(query)
#         print(
#             "trying to retrieve data from the database. Use this tool for questions about user data"
#         )
#         return str(c.fetchall())
#     except Exception as e:
#         return f"Error executing query: {str(e)}"


# def get_run_query_tool_2():
#     return Tool.from_function(
#         name="run_sqlite_query_2",
#         description="Run a SQLite query. Input should be a JSON object with 'query' key containing the SQL string.",
#         func=run_sqlite_query_2,
#     )



import sqlite3
from langchain.tools import Tool
import json

# Initialize database connection
conn = sqlite3.connect("db.sqlite")
conn.row_factory = sqlite3.Row  # For better result handling

def run_sqlite_query(action_input):
    print(f"\nDEBUG: Received input - {action_input} ({type(action_input)})")  # Debug
    
    try:
        # Handle both direct string and JSON input
        if isinstance(action_input, str):
            try:
                data = json.loads(action_input)
                query = data.get('query', action_input)
            except json.JSONDecodeError:
                query = action_input
        elif isinstance(action_input, dict):
            query = action_input.get('query', '')
        else:
            return "Error: Invalid input format"
        
        print(f"DEBUG: Executing query - {query}")  # Debug
        
        c = conn.cursor()
        c.execute(query)
        results = c.fetchall()
        
        # Convert results to a readable format
        if results:
            if len(results[0]) == 1:  # Single column result
                return str([row[0] for row in results])
            return str([dict(row) for row in results])
        return "No results found"
        
    except Exception as e:
        print(f"DEBUG: Error - {str(e)}")  # Debug
        return f"Error executing query: {str(e)}"

run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run SQL queries on the database. Input should be a JSON object with 'query' key or a SQL string.",
    func=run_sqlite_query
)