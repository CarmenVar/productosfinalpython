import sqlite3
import pandas as pd

# Conectar a la base de datos
conexion = sqlite3.connect('productos.db')

# Exportar cada tabla y vista a CSV
tablas = ['productos', 'ventas', 'gastos_operativos', 'vista_rentabilidad_neta']

for tabla in tablas:
    try:
        df = pd.read_sql_query(f"SELECT * FROM {tabla}", conexion)
        df.to_csv(f"{tabla}.csv", index=False, encoding='utf-8-sig')
        print(f"Exportado con éxito: {tabla}.csv")
    except Exception as e:
        print(f"No se pudo exportar {tabla}: {e}")

conexion.close()