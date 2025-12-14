import sqlite3
from colorama import init, Fore

# Inicializamos colorama para usar colores en los mensajes
init(autoreset=True)

# ========================================
# 🔌 Conexión a la base de datos
# ========================================
def conectar():
    """Conecta a la base de datos productos.db y devuelve la conexión"""
    return sqlite3.connect("productos.db")


# ========================================
# 📥 Registrar producto
# ========================================
def registrar_producto():
    """Solicita datos al usuario, valida y guarda el producto"""
    print(Fore.CYAN + "\n[Registrar producto]")
    # TODO: Pedir nombre, categoría, cantidad y precio
    # TODO: Validar que cantidad y precio sean números positivos
    # TODO: Insertar en la tabla con parámetros seguros (?)
    pass
 # Solicitar datos al usuario
    nombre = input("Nombre del producto: ").strip()
    categoria = input("Categoría: ").strip()
    cantidad = input("Cantidad: ").strip()
    precio = input("Precio: ").strip()
        # Validar campos vacíos
    if not nombre or not categoria or not cantidad or not precio:
        print(Fore.RED + "Todos los campos son obligatorios.")
        return

    # Validar que cantidad y precio sean números válidos
    try:
        cantidad = int(cantidad)
        precio = float(precio)

        if cantidad < 0 or precio < 0:
            print(Fore.RED + "La cantidad y el precio deben ser mayores o iguales a cero.")
            return

    except ValueError:
        print(Fore.RED + "Cantidad debe ser un número entero y precio un número decimal.")
        return
    # Insertar en la base de datos
    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO productos (nombre, categoria, cantidad, precio)
            VALUES (?, ?, ?, ?)
        """, (nombre, categoria, cantidad, precio))

        con.commit()
        print(Fore.GREEN + "Producto registrado correctamente.")
    except Exception as e:
        print(Fore.RED + f"Ocurrió un error: {e}")
    finally:
        con.close()


# ========================================
# 👁️ Ver todos los productos
# ========================================
def ver_productos():
    print(Fore.CYAN + "\n[Lista de productos]")

    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()

        if productos:
            print(Fore.YELLOW + "\nID | Nombre | Categoría | Cantidad | Precio")
            print("-" * 50)
            for p in productos:
                print(Fore.GREEN + f"{p[0]} | {p[1]} | {p[2]} | {p[3]} | ${p[4]:.2f}")
        else:
            print(Fore.LIGHTRED_EX + "No hay productos registrados.")

    except Exception as e:
        print(Fore.RED + f"Error al mostrar productos: {e}")
    finally:
        con.close()


# ========================================
# ✏️ Actualizar producto por ID
# ========================================
def actualizar_producto():
    print(Fore.CYAN + "\n[Actualizar producto]")

    try:
        con = conectar()
        cursor = con.cursor()

        # Mostrar productos existentes
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()

        if not productos:
            print(Fore.LIGHTRED_EX + "No hay productos para actualizar.")
            return

        print(Fore.YELLOW + "\nProductos disponibles:")
        for p in productos:
            print(Fore.GREEN + f"{p[0]} | {p[1]} | {p[2]} | {p[3]} | ${p[4]:.2f}")

        # Pedir ID del producto a actualizar
        id_producto = input(Fore.CYAN + "\nIngrese el ID del producto a actualizar: ").strip()

        if not id_producto.isdigit():
            print(Fore.RED + "El ID debe ser un número.")
            return

        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
        producto = cursor.fetchone()

        if not producto:
            print(Fore.RED + "No se encontró un producto con ese ID.")
            return

        # Mostrar el producto actual
        print(Fore.YELLOW + f"\nProducto actual:")
        print(Fore.GREEN + f"{producto[0]} | {producto[1]} | {producto[2]} | {producto[3]} | ${producto[4]:.2f}")

        # Pedir nuevos valores (dejar vacío para no cambiar)
        nuevo_nombre = input("Nuevo nombre (dejar vacío para mantener): ").strip()
        nueva_categoria = input("Nueva categoría (dejar vacío para mantener): ").strip()
        nueva_cantidad = input("Nueva cantidad (dejar vacío para mantener): ").strip()
        nuevo_precio = input("Nuevo precio (dejar vacío para mantener): ").strip()

        # Si el campo está vacío, usamos el valor original
        nombre_final = nuevo_nombre if nuevo_nombre else producto[1]
        categoria_final = nueva_categoria if nueva_categoria else producto[2]

        try:
            cantidad_final = int(nueva_cantidad) if nueva_cantidad else producto[3]
            precio_final = float(nuevo_precio) if nuevo_precio else producto[4]
        except ValueError:
            print(Fore.RED + "Cantidad debe ser un número entero y precio un número decimal.")
            return

        if cantidad_final < 0 or precio_final < 0:
            print(Fore.RED + "Cantidad y precio deben ser ≥ 0.")
            return

        # Actualizar en la base
        cursor.execute("""
            UPDATE productos
            SET nombre = ?, categoria = ?, cantidad = ?, precio = ?
            WHERE id = ?
        """, (nombre_final, categoria_final, cantidad_final, precio_final, id_producto))

        con.commit()
        print(Fore.GREEN + "Producto actualizado correctamente.")

    except Exception as e:
        print(Fore.RED + f"Error: {e}")
    finally:
        con.close()


# ========================================
# 🗑️ Eliminar producto por ID
# ========================================
def eliminar_producto():
    print(Fore.CYAN + "\n[Eliminar producto]")

    try:
        con = conectar()
        cursor = con.cursor()

        # Mostrar todos los productos
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()

        if not productos:
            print(Fore.LIGHTRED_EX + "No hay productos para eliminar.")
            return

        print(Fore.YELLOW + "\nProductos disponibles:")
        for p in productos:
            print(Fore.GREEN + f"{p[0]} | {p[1]} | {p[2]} | {p[3]} | ${p[4]:.2f}")

        # Pedir ID del producto a eliminar
        id_eliminar = input(Fore.CYAN + "\nIngrese el ID del producto a eliminar: ").strip()

        if not id_eliminar.isdigit():
            print(Fore.RED + "El ID debe ser un número.")
            return

        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_eliminar,))
        producto = cursor.fetchone()

        if not producto:
            print(Fore.RED + "No se encontró un producto con ese ID.")
            return

        # Confirmación
        confirmacion = input(Fore.LIGHTYELLOW_EX + f"¿Está seguro que desea eliminar el producto '{producto[1]}'? (s/n): ").strip().lower()

        if confirmacion != 's':
            print(Fore.YELLOW + "Operación cancelada.")
            return

        # Eliminar
        cursor.execute("DELETE FROM productos WHERE id = ?", (id_eliminar,))
        con.commit()
        print(Fore.GREEN + "Producto eliminado correctamente.")

    except Exception as e:
        print(Fore.RED + f"Error al eliminar producto: {e}")
    finally:
        con.close()



# ========================================
# 🔍 Buscar producto por ID
# ========================================
def buscar_producto():
    print(Fore.CYAN + "\n[Buscar producto por ID]")

    id_buscar = input("Ingrese el ID del producto: ").strip()

    if not id_buscar.isdigit():
        print(Fore.RED + "El ID debe ser un número.")
        return

    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_buscar,))
        producto = cursor.fetchone()

        if producto:
            print(Fore.YELLOW + "\nProducto encontrado:")
            print(Fore.GREEN + f"{producto[0]} | {producto[1]} | {producto[2]} | {producto[3]} | ${producto[4]:.2f}")
        else:
            print(Fore.LIGHTRED_EX + "No se encontró un producto con ese ID.")

    except Exception as e:
        print(Fore.RED + f"Error al buscar el producto: {e}")
    finally:
        con.close()


# ========================================
# 📊 Reporte de productos con poca cantidad
# ========================================
def reporte_bajo_stock():
    print(Fore.CYAN + "\n[Reporte de productos con bajo stock]")

    limite = input("Mostrar productos con cantidad menor o igual a: ").strip()

    if not limite.isdigit():
        print(Fore.RED + "El valor debe ser un número entero.")
        return

    limite = int(limite)

    try:
        con = conectar()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
        productos = cursor.fetchall()

        if productos:
            print(Fore.YELLOW + f"\nProductos con stock ≤ {limite}:")
            for p in productos:
                print(Fore.GREEN + f"{p[0]} | {p[1]} | {p[2]} | {p[3]} | ${p[4]:.2f}")
        else:
            print(Fore.LIGHTRED_EX + "No hay productos con esa condición.")

    except Exception as e:
        print(Fore.RED + f"Error al generar el reporte: {e}")
    finally:
        con.close()


# ========================================
# 🧭 Menú principal
# ========================================
def menu():
    while True:
        print(Fore.YELLOW + "\n===== MENÚ PRINCIPAL =====")
        print("1. Registrar nuevo producto")
        print("2. Ver productos")
        print("3. Actualizar producto por ID")
        print("4. Eliminar producto por ID")
        print("5. Buscar producto por ID")
        print("6. Reporte de productos con bajo stock")
        print("7. Salir")

        opcion = input("Seleccioná una opción: ")

        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            ver_productos()
        elif opcion == "3":
            actualizar_producto()
        elif opcion == "4":
            eliminar_producto()
        elif opcion == "5":
            buscar_producto()
        elif opcion == "6":
            reporte_bajo_stock()
        elif opcion == "7":
            print(Fore.GREEN + "¡Gracias por usar el sistema!")
            break
        else:
            print(Fore.RED + "Opción inválida. Intentá de nuevo.")

# Ejecutamos el menú al iniciar el programa
menu()
