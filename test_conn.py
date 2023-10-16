from dotenv import load_dotenv
load_dotenv()
import os
import MySQLdb
import pandas as pd



connection = MySQLdb.connect(
  host= os.getenv("DB_HOST"),
  user=os.getenv("DB_USERNAME"),
  passwd= os.getenv("DB_PASSWORD"),
  db= os.getenv("DB_NAME"), 
  ssl = { 
    "rejectedUnauthorized": False
  }
)


# Crea un cursor para ejecutar consultas
cursor = connection.cursor()

# Ejecuta la consulta "USE meson;" para seleccionar la base de datos "meson"
cursor.execute("USE meson;")

# Ejecuta la consulta "SHOW TABLES;" para mostrar las tablas en la base de datos
cursor.execute("SHOW TABLES;") 

# Obtiene los resultados de la consulta "SHOW TABLES;"
tables = cursor.fetchall()

# Imprime la lista de tablas
print("Tablas en la base de datos 'meson':")
for tab in tables:
    print(tab[0])

# Cierra el cursor y la conexión
#cursor.close()
#onnection.close()



# Nombre de la tabla en la base de datos
table_name = "dolar_price"

# Reemplaza los valores NaN con 0
df = df.fillna(0)

# Convierte el DataFrame a una lista de tuplas
data = [tuple(row) for row in df.values]

# Define la sentencia SQL de inserción
insert_query = "INSERT INTO {} (Date, Blue_Sell, Oficial_Sell, Blue_Buy, Oficial_Buy) VALUES (%s, %s, %s, %s, %s)".format(table_name)

try:
    # Ejecuta la sentencia SQL de inserción
    with connection.cursor() as cursor:
        cursor.executemany(insert_query, data)

    # Confirma los cambios en la base de datos
    connection.commit()

    print("Datos insertados con éxito.")
except MySQLdb.Error as e:
    # En caso de error, deshace cualquier cambio pendiente y muestra un mensaje de error
    connection.rollback()
    print("Error al insertar datos:", e)

# Cierra la conexión
#connection.close()