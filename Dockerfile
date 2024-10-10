# Cambia la versión de Python a una compatible con numpy 2.1.1
FROM python:3.10-slim

# Configura el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de tu aplicación
COPY . .

# Comando para iniciar tu aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
