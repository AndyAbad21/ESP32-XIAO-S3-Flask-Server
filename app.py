from flask import Flask, render_template, send_file
import cv2
import os
import numpy as np

app = Flask(__name__)

# Rutas de las imágenes específicas
imagenes = [
    '/home/andy/Escritorio/vc/practica2/ESP32-XIAO-S3-Flask-Server/static/person1000_bacteria_2931.jpeg',
    '/home/andy/Escritorio/vc/practica2/ESP32-XIAO-S3-Flask-Server/static/person1003_virus_1685.jpeg',
    '/home/andy/Escritorio/vc/practica2/ESP32-XIAO-S3-Flask-Server/static/person1008_virus_1691.jpeg'
]

procesadas_carpeta = 'procesadas'  # Carpeta para guardar imágenes procesadas

# Asegúrate de que la carpeta para guardar imágenes procesadas exista
if not os.path.exists(procesadas_carpeta):
    os.makedirs(procesadas_carpeta)

# Parámetros para operaciones morfológicas
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# Ruta principal que procesa y muestra las imágenes
@app.route('/')
def index():
    imagenes_procesadas = []
    
    # Procesar cada imagen
    for ruta_imagen in imagenes:
        # Carga la imagen en escala de grises
        imagen = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
        
        # Guarda la imagen original en la lista
        nombre_imagen = os.path.basename(ruta_imagen)
        ruta_original = os.path.join(procesadas_carpeta, f'original_{nombre_imagen}')
        cv2.imwrite(ruta_original, imagen)
        
        # Erosión
        erosion = cv2.erode(imagen, kernel, iterations=1)
        ruta_erosion = os.path.join(procesadas_carpeta, f'erosion_{nombre_imagen}')
        cv2.imwrite(ruta_erosion, erosion)
        
        # Dilatación
        dilatacion = cv2.dilate(imagen, kernel, iterations=1)
        ruta_dilatacion = os.path.join(procesadas_carpeta, f'dilatacion_{nombre_imagen}')
        cv2.imwrite(ruta_dilatacion, dilatacion)
        
        # Top Hat
        top_hat = cv2.morphologyEx(imagen, cv2.MORPH_TOPHAT, kernel)
        ruta_top_hat = os.path.join(procesadas_carpeta, f'top_hat_{nombre_imagen}')
        cv2.imwrite(ruta_top_hat, top_hat)
        
        # Black Hat
        black_hat = cv2.morphologyEx(imagen, cv2.MORPH_BLACKHAT, kernel)
        ruta_black_hat = os.path.join(procesadas_carpeta, f'black_hat_{nombre_imagen}')
        cv2.imwrite(ruta_black_hat, black_hat)
        
        # Imagen Original + (Top Hat - Black Hat)
        resultado = cv2.add(imagen, cv2.subtract(top_hat, black_hat))
        ruta_resultado = os.path.join(procesadas_carpeta, f'resultado_{nombre_imagen}')
        cv2.imwrite(ruta_resultado, resultado)
        
        # Agrega las rutas de cada imagen procesada con su tipo para mostrarla en el HTML
        imagenes_procesadas.append({
            'original': ruta_original,
            'erosion': ruta_erosion,
            'dilatacion': ruta_dilatacion,
            'top_hat': ruta_top_hat,
            'black_hat': ruta_black_hat,
            'resultado': ruta_resultado
        })
    
    return render_template('index.html', imagenes=imagenes_procesadas)

# Ruta para mostrar una imagen procesada
@app.route('/imagen/<nombre>')
def mostrar_imagen(nombre):
    ruta_imagen = os.path.join(procesadas_carpeta, nombre)
    return send_file(ruta_imagen, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
