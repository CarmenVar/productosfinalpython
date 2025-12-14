import sqlite3

conexion = sqlite3.connect("productos.db")
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    categoria TEXT NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad >= 0),
    precio REAL NOT NULL CHECK (precio >= 0)
)
""")

conexion.commit()
conexion.close()
print("Base de datos y tabla creadas correctamente.")
