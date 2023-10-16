from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import os
import MySQLdb

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Database connection
db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

try:
    mysql_connection = MySQLdb.connect(
        host=db_host,
        user=db_username,
        passwd=db_password,
        db=db_name,
        ssl={"rejectedUnauthorized": False}
    )
except Exception as e:
    print(f"Error connecting to the database: {str(e)}")

# Route for displaying data
@app.route('/')
def index():
    try:
        with mysql_connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Gasto")
            gastos = cursor.fetchall()
        return render_template('index.html', gastos=gastos)
    except Exception as e:
        return f"Error fetching data from the database: {str(e)}"

# Route for adding new data
@app.route('/agregar_gasto', methods=['POST'])
def agregar_gasto():
    try:
        elemento = request.form['elemento']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])

        with mysql_connection.cursor() as cursor:
            insert_query = "INSERT INTO Gasto (elemento, cantidad, precio) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (elemento, cantidad, precio))
            mysql_connection.commit()

        return redirect(url_for('index'))
    except Exception as e:
        return f"Error adding data to the database: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
