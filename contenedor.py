import os
import subprocess

# Configuración según el Ítem 3
DIR_TEMP = "temp_docker_item3"
PUERTO_WEB = 7529

# 1. Crear directorios temporales para el sitio web
print("Creando directorios temporales...")
os.makedirs(f"{DIR_TEMP}/templates", exist_ok=True)
os.makedirs(f"{DIR_TEMP}/static", exist_ok=True)

# 2. Crear archivo HTML de muestra (index.html)
html_content = """
<!DOCTYPE html>
<html>
<head><title>CCNA DevNet Item 3</title></head>
<body>
    <h1>Sitio Web en Docker - Puerto 7529</h1>
    <p>Desplegado por: Eduardo Vejar</p>
</body>
</html>
"""
with open(f"{DIR_TEMP}/templates/index.html", "w") as f:
    f.write(html_content)

# 3. Crear el archivo .py simplificado al máximo
app_py_content = """
from flask import Flask
import sys

app = Flask(__name__)

@app.route('/')
def main():
    return "<h1>Sitio Web en Docker - Puerto 7529</h1><p>Desplegado por: Eduardo Vejar</p>"

if __name__ == '__main__':
    # Usamos el puerto 7529 directamente
    app.run(host='0.0.0.0', port=7529, threaded=False)
"""
with open(f"{DIR_TEMP}/sample_app.py", "w") as f:
    f.write(app_py_content)

# 4. Crear el Dockerfile (Versión de compatibilidad total)
dockerfile_content = """
FROM python:3.8-slim
# Forzamos versiones específicas que sabemos que funcionan en esta VM
RUN pip install --no-cache-dir --progress-bar off flask==2.0.3 Werkzeug==2.0.3
WORKDIR /app
COPY sample_app.py /app/
EXPOSE 7529
CMD ["python3", "sample_app.py"]
"""

with open(f"{DIR_TEMP}/Dockerfile", "w") as f:
    f.write(dockerfile_content)

# 5. Construir el contenedor Docker
print("Construyendo la imagen Docker...")
subprocess.run(["docker", "build", "-t", "web_item3_img", DIR_TEMP])

# 6. Iniciar el contenedor Docker
print("Iniciando el contenedor...")
subprocess.run(["docker", "run", "-d", "-p", f"{PUERTO_WEB}:{PUERTO_WEB}", "--name", "web_item3_container", "web_item3_img"])

print(f"\nProceso finalizado. Compruebe en: http://localhost:{PUERTO_WEB}")
