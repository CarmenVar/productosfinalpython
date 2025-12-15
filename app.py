from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def conectar():
    return sqlite3.connect("productos.db")

@app.route('/')
def index():
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    con.close()
    return render_template('index.html', productos=productos)

if __name__ == '__main__':
    app.run(debug=True)
