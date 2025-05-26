FROM public.ecr.aws/lambda/python:3.10

# ✅ Instala tar, xz y ffmpeg (estático) + imprime rutas y tamaño
RUN yum -y install tar xz && \
    echo "📦 Descargando ffmpeg..." && \
    curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz -o ffmpeg.tar.xz && \
    echo "📂 Contenido descargado:" && ls -lh ffmpeg.tar.xz && \
    tar -xf ffmpeg.tar.xz && \
    echo "📁 Contenido de la carpeta ffmpeg-*-static:" && ls -lh ffmpeg-*-static && \
    cp ffmpeg-*-static/ffmpeg /usr/bin/ffmpeg && \
    chmod +x /usr/bin/ffmpeg && \
    ffmpeg -version && \
    echo "✅ FFmpeg instalado correctamente" && \
    rm -rf ffmpeg.tar.xz ffmpeg-*-static

# ✅ Cambiar a directorio de Lambda
WORKDIR /var/task

# ✅ Copiar código fuente
COPY app/ app/
COPY app/lambda_main.py .
COPY requirements.txt .

# ✅ Mostrar contenido copiado
RUN echo "📂 Contenido en /var/task:" && ls -lh /var/task && \
    echo "📂 Contenido en /var/task/app:" && ls -lh /var/task/app

# ✅ Instalar dependencias
RUN echo "📦 Instalando dependencias..." && \
    pip install --no-cache-dir -r requirements.txt && \
    echo "✅ Dependencias instaladas"

# ✅ Definir punto de entrada
CMD ["lambda_main.handler"]
