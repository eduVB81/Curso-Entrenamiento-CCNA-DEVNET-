import sqlite3
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)
db_name = 'test.db'
PUERTO = 7890

# Función para inicializar la base de datos y la tabla
def init_db():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    # Creamos la tabla con el campo extra solicitado: 'registro_eleccion'
    c.execute('''CREATE TABLE IF NOT EXISTS USER_HASH 
                 (USERNAME TEXT PRIMARY KEY NOT NULL, 
                  HASH TEXT NOT NULL,
                  REGISTRO_ELECCION TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Ruta para registro con Hash (v2 según el documento de la escuela)
@app.route('/signup/v2', methods=['POST'])
def signup_v2():
    username = request.form.get('username')
    password = request.form.get('password')
    eleccion = request.form.get('eleccion') # Registro a elección (ej. Sede o Profesión)

    if not username or not password:
        return "Faltan datos requeridos", 400

    # Generación de Hash SHA-256
    hash_value = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute("INSERT INTO USER_HASH (USERNAME, HASH, REGISTRO_ELECCION) VALUES (?, ?, ?)", 
                  (username, hash_value, eleccion))
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        return "El usuario ya existe", 400
    
    return f"Registro exitoso. Hash almacenado: {hash_value}"

if __name__ == '__main__':
    init_db()
    print(f"Iniciando servidor en puerto {PUERTO}...")
    # Se usa ssl_context='adhoc' como sugiere el documento de la escuela
    app.run(host='0.0.0.0', port=PUERTO, ssl_context='adhoc')
