import sqlite3
from tabulate import tabulate

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect("db/image_descriptions.db")

    # Create a cursor object to execute queries
    cursor = conn.cursor()

    # Execute a SELECT query
    cursor.execute("SELECT DISTINCT image_name, description FROM descriptions")

    # Fetch all the rows from the result of the query
    rows = cursor.fetchall()

    # Create a table using the tabulate module
    print(tabulate(rows, headers=["Image Name", "Description"], tablefmt="grid"))

    # Close the connection to the database
    conn.close()

if __name__ == "__main__":
    main()