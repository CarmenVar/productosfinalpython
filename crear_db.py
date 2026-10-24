import sqlite3

def crear_base_de_datos():
    conexion = sqlite3.connect('productos.db')
    cursor = conexion.cursor()

    # 1. Tabla de Productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            sku TEXT UNIQUE,
            categoria TEXT,
            precio_costo_ars REAL NOT NULL,
            precio_venta_sugerido REAL NOT NULL
        )
    ''')

    # 2. Tabla de Ventas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            id_producto INTEGER NOT NULL,
            cantidad_vendida INTEGER NOT NULL,
            precio_venta_final REAL NOT NULL,
            canal_venta TEXT NOT NULL,
            FOREIGN KEY (id_producto) REFERENCES productos (id_producto)
        )
    ''')

    # 3. Tabla de Gastos Operativos e Impuestos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos_operativos (
            id_gasto INTEGER PRIMARY KEY AUTOINCREMENT,
            id_venta INTEGER,
            tipo_gasto TEXT NOT NULL,
            monto REAL NOT NULL,
            descripcion TEXT,
            FOREIGN KEY (id_venta) REFERENCES ventas (id_venta)
        )
    ''')

    # 4. Vista SQL de Rentabilidad Neta para Power BI
    cursor.execute('DROP VIEW IF EXISTS vista_rentabilidad_neta')
    cursor.execute('''
        CREATE VIEW vista_rentabilidad_neta AS
        SELECT 
            v.id_venta,
            v.fecha,
            p.nombre AS producto,
            p.categoria,
            v.canal_venta,
            v.cantidad_vendida,
            (v.cantidad_vendida * v.precio_venta_final) AS ingreso_bruto,
            (v.cantidad_vendida * p.precio_costo_ars) AS costo_mercaderia,
            COALESCE(SUM(g.monto), 0) AS total_gastos_e_impuestos,
            ((v.cantidad_vendida * v.precio_venta_final) - (v.cantidad_vendida * p.precio_costo_ars) - COALESCE(SUM(g.monto), 0)) AS ganancia_neta
        FROM ventas v
        JOIN productos p ON v.id_producto = p.id_producto
        LEFT JOIN gastos_operativos g ON v.id_venta = g.id_venta
        GROUP BY v.id_venta;
    ''')

    conexion.commit()
    conexion.close()
    print("Base de datos estructurada con éxito.")

if __name__ == '__main__':
    crear_base_de_datos()
