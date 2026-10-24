from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import pandas as pd
import plotly.express as px

app = Flask(__name__)

def conectar():
    return sqlite3.connect("productos.db")

@app.route('/')
def index():
    con = conectar()
    cursor = con.cursor()
    
    # 1. Consultamos los productos para tu tabla
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    
    # 2. Consultamos la vista de rentabilidad para el gráfico con pandas y plotly
    df = pd.read_sql_query("SELECT * FROM vista_rentabilidad_neta", con)
    con.close()
    
    # 3. Creamos el gráfico interactivo de Plotly
    fig = px.bar(
        df, 
        x='producto', 
        y='ganancia_neta', 
        color='canal_venta', 
        title="Ganancia Neta por Producto y Canal de Venta",
        template="plotly_white"
    )
    graph_html = fig.to_html(full_html=False)
    
    # 4. Renderizamos el index pasándole AMBAS variables (productos y el gráfico)
    return render_template('index.html', productos=productos, graph_html=graph_html)

@app.route('/dashboard')
def dashboard():
    # Conectamos a tu base de datos SQLite
    conn = sqlite3.connect('productos.db')
    df = pd.read_sql_query("SELECT * FROM vista_rentabilidad_neta", conn)
    conn.close()

    # Creamos un gráfico interactivo de barras con Plotly
    fig = px.bar(
        df, 
        x='producto', 
        y='ganancia_neta', 
        color='canal_venta', 
        title="Ganancia Neta por Producto y Canal de Venta",
        template="plotly_white"
    )

    # Convertimos el gráfico a código HTML
    graph_html = fig.to_html(full_html=False)

    return render_template('dashboard.html', graph_html=graph_html)

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
