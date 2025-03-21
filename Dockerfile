# Usar una imagen base oficial de Python
FROM python:3.10

# Configurar el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar dlib
RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libx11-dev \
    libatlas-base-dev \
    libboost-python-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos del proyecto al contenedor
COPY . .

# Instalar pip y actualizar
RUN pip install --no-cache-dir --upgrade pip

# Instalar dlib desde el código fuente (para Linux)
RUN pip install --no-cache-dir dlib

# Instalar el resto de las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto 8000 para Django
EXPOSE 8000

# Comando para ejecutar el servidor de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
