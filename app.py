from flask import Flask, request, render_template_string
import sqlite3
import bcrypt

app = Flask(__name__)

# Configuración de la base de datos
DATABASE = 'usuarios.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Inicializar la base de datos
init_db()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, password) VALUES (?, ?)", (nombre, hashed))
        conn.commit()
        conn.close()
        return 'Usuario registrado con éxito'
    
    return render_template_string('''
        <form method="post">
            Nombre: <input type="text" name="nombre"><br>
            Contraseña: <input type="password" name="password"><br>
            <input type="submit" value="Registrar">
        </form>
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM usuarios WHERE nombre=?", (nombre,))
        row = cursor.fetchone()
        conn.close()

        if row and bcrypt.checkpw(password.encode('utf-8'), row[0]):
            return 'Inicio de sesión exitoso'
        else:
            return 'Nombre de usuario o contraseña incorrectos'
    
    return render_template_string('''
        <form method="post">
            Nombre: <input type="text" name="nombre"><br>
            Contraseña: <input type="password" name="password"><br>
            <input type="submit" value="Iniciar sesión">
        </form>
    ''')

if __name__ == '__main__':
    app.run(port=5800)
