# Usar una imagen base de Python
FROM python:3.9

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de la aplicación al contenedor
COPY . /app

# Instalar las dependencias
RUN pip install -r requirements.txt

# Exponer el puerto en el que la aplicación Flask estará escuchando
EXPOSE 1337

# Comando para ejecutar la aplicación
CMD ["python", "server.py"]