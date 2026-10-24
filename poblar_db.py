import sqlite3

def poblar_datos():
    conexion = sqlite3.connect('productos.db')
    cursor = conexion.cursor()

    # 1. Insertar Productos de Ejemplo
    productos_ejemplo = [
        ('Smartwatch KronosBit', 'KB-01', 'Wearables', 25000.0, 55000.0),
        ('Afeitadora Eléctrica Pro', 'AF-02', 'Cuidado Personal', 18000.0, 38000.0),
        ('Set Pijama Urbano', 'PJ-03', 'Indumentaria', 12000.0, 28000.0),
        ('Auriculares Inalámbricos TWS', 'AU-04', 'Audio', 15000.0, 35000.0)
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO productos (nombre, sku, categoria, precio_costo_ars, precio_venta_sugerido)
        VALUES (?, ?, ?, ?, ?)
    ''', productos_ejemplo)

    # 2. Insertar Ventas de Ejemplo
    ventas_ejemplo = [
        ('2026-06-01', 1, 2, 55000.0, 'Mercado Libre'),
        ('2026-06-02', 2, 1, 38000.0, 'Tienda Propia'),
        ('2026-06-03', 3, 3, 28000.0, 'Mercado Libre'),
        ('2026-06-04', 4, 2, 35000.0, 'Tienda Propia')
    ]

    cursor.executemany('''
        INSERT INTO ventas (fecha, id_producto, cantidad_vendida, precio_venta_final, canal_venta)
        VALUES (?, ?, ?, ?, ?)
    ''', ventas_ejemplo)

    # 3. Insertar Gastos Operativos e Impuestos asociados a las ventas
    gastos_ejemplo = [
        (1, 'Comisión Plataforma', 14300.0, 'Comisión Mercado Libre (13%)'),
        (1, 'Impuestos', 3850.0, 'Ingresos Brutos (3.5%)'),
        (1, 'Logística / Envíos', 4500.0, 'Envío a domicilio'),
        
        (2, 'Comisión Pasarela', 1900.0, 'Comisión pagos online (5%)'),
        (2, 'Impuestos', 1330.0, 'Ingresos Brutos (3.5%)'),
        
        (3, 'Comisión Plataforma', 10920.0, 'Comisión Mercado Libre (13%)'),
        (3, 'Impuestos', 2940.0, 'Ingresos Brutos (3.5%)'),
        (3, 'Logística / Envíos', 4500.0, 'Envío a domicilio'),

        (4, 'Comisión Pasarela', 3500.0, 'Comisión pagos online (10%)'),
        (4, 'Impuestos', 2450.0, 'Ingresos Brutos (3.5%)')
    ]

    cursor.executemany('''
        INSERT INTO gastos_operativos (id_venta, tipo_gasto, monto, descripcion)
        VALUES (?, ?, ?, ?)
    ''', gastos_ejemplo)

    conexion.commit()
    conexion.close()
    print("¡Base de datos poblada con éxito con datos de ventas y costos!")

if __name__ == '__main__':
    poblar_datos()