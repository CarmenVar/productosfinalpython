from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def conectar():
    return sqlite3.connect("productos.db")


@app.route('/')
def index():
    # 1. Nos conectamos a la base de datos
    con = conectar()
    cursor = con.cursor()
    
    # 2. Consultamos todos los productos almacenados
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()  # Esto trae una lista con todos los productos
    con.close()
    
    # 3. Renderizamos el index.html pasándole la lista de productos
    return render_template('index.html', productos=productos)


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        try:
            con = conectar()
            cursor = con.cursor()
            cursor.execute("""
                INSERT INTO productos (nombre, categoria, cantidad, precio)
                VALUES (?, ?, ?, ?)
            """, (nombre, categoria, int(cantidad), float(precio)))
            con.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f"Error: {e}"
        finally:
            con.close()
    else:
        return render_template('registrar.html')
@app.route('/eliminar/<int:id>')
def eliminar(id):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
    con.commit()
    con.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
