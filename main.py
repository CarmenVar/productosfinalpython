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
    """Actualiza los datos de un producto existente usando su ID"""
    print(Fore.CYAN + "\n[Actualizar producto]")
    # TODO: Pedir ID, validar si existe
    # TODO: Pedir nuevos valores (uno o todos)
    # TODO: UPDATE productos SET ... WHERE id = ?
    pass


# ========================================
# 🗑️ Eliminar producto por ID
# ========================================
def eliminar_producto():
    """Elimina un producto por su ID, con confirmación"""
    print(Fore.CYAN + "\n[Eliminar producto]")
    # TODO: Mostrar productos, pedir ID, confirmar antes de borrar
    # TODO: DELETE FROM productos WHERE id = ?
    pass


# ========================================
# 🔍 Buscar producto por ID
# ========================================
def buscar_producto():
    """Busca y muestra un producto por su ID"""
    print(Fore.CYAN + "\n[Buscar producto por ID]")
    # TODO: Pedir ID, buscar en la base y mostrar si existe
    pass


# ========================================
# 📊 Reporte de productos con poca cantidad
# ========================================
def reporte_bajo_stock():
    """Muestra productos con cantidad igual o inferior al límite ingresado"""
    print(Fore.CYAN + "\n[Reporte de bajo stock]")
    # TODO: Pedir límite (ej: 5) y mostrar productos con cantidad <= ese valor
    pass


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
