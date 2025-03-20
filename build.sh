# Instalar dependencias del sistema antes de instalar paquetes Python
# Agregarlo en "Build Command" en Render: chmod +x build.sh && ./build.sh
apt-get update && apt-get install -y \
    build-essential \
    cmake \
    python3-dev \
    python3-pip \
    libboost-all-dev \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libatlas-base-dev \
    libjpeg-dev

pip install --no-cache-dir -r requirements.txt
