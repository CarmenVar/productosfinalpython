import sqlite3
import csv

def conectar():
    return sqlite3.connect("productos.db")

def importar_desde_csv(nombre_archivo):
    con = conectar()
    cursor = con.cursor()

    with open(nombre_archivo, newline='', encoding='utf-8') as archivo_csv:
        lector = csv.reader(archivo_csv)
        next(lector)  # Salta el encabezado

        for fila in lector:
            nombre, categoria, cantidad, precio = fila

            try:
                cantidad = int(cantidad)
                precio = float(precio)

                if cantidad < 0 or precio < 0:
                    print(f"⚠️ Producto inválido (valores negativos): {fila}")
                    continue

                cursor.execute("""
                    INSERT INTO productos (nombre, categoria, cantidad, precio)
                    VALUES (?, ?, ?, ?)
                """, (nombre.strip(), categoria.strip(), cantidad, precio))
            except Exception as e:
                print(f"❌ Error en fila {fila}: {e}")

    con.commit()
    con.close()
    print("📥 Importación finalizada.")

# Ejecutar importación
importar_desde_csv("productos.csv")  # Cambiar si el nombre del archivo es distinto
