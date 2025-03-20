#IMPORTANTE TRABAJAR CON ESTA VERSION DE NUMPY
#pip install numpy==1.25.1
from PIL import Image, ExifTags
import cv2
import cloudinary
import cloudinary.api
import requests
import numpy as np
import face_recognition
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from PIL import Image
import io
from .models import Personaje  # Importa el modelo


# 📥 Función para cargar rostros desde Cloudinary
def cargar_rostros():
    encodings_conocidos = []
    nombres_conocidos = []
    personajes_info = {}

    personajes = Personaje.objects.all()  # Obtener personajes desde la base de datos

    for personaje in personajes:
        url_imagen = personaje.imagen_referencia  # Obtener URL desde la BD
        nombre = personaje.nombre

        response = requests.get(url_imagen, stream=True)
        if response.status_code != 200:
            print(f"[ERROR] No se pudo descargar la imagen: {url_imagen}")
            continue

        imagen_pil = Image.open(io.BytesIO(response.content))
        imagen_rgb = imagen_pil.convert("RGB")
        imagen_np = np.array(imagen_rgb, dtype=np.uint8)

        ubicaciones_caras = face_recognition.face_locations(imagen_np, model="hog")
        encoding = face_recognition.face_encodings(imagen_np, ubicaciones_caras)

        if encoding:
            encodings_conocidos.append(encoding[0])
            nombres_conocidos.append(nombre)
            personajes_info[nombre] = {
                "nombre": personaje.nombre,
                "apellido": personaje.apellido,
                "descripcion": personaje.descripcion,
                "cargo": personaje.cargo,
                "edad": personaje.edad,
                "imagen": personaje.imagen_referencia
            }

    return encodings_conocidos, nombres_conocidos, personajes_info
# Mostrar el resultado final
#print("\n✅ Resultado Final:")
#print(f"🔹 Rostros cargados: {len(nombre)}")
#print(f"🔹 Nombres: {nombres}")



class ReconocimientoFacialAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('imagen')

        if not file:
            return Response({"error": "No se recibió ninguna imagen."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            encodings_conocidos, nombres_conocidos, personajes_info = cargar_rostros()

            if not encodings_conocidos:
                return Response({"error": "No hay rostros registrados en la base de datos."}, status=status.HTTP_400_BAD_REQUEST)

            imagen_pil = Image.open(file)
            imagen_rgb = imagen_pil.convert("RGB")
            imagen_np = np.array(imagen_rgb, dtype=np.uint8)

            ubicaciones_caras = face_recognition.face_locations(imagen_np, model="hog")
            encodings_caras = face_recognition.face_encodings(imagen_np, ubicaciones_caras)

            if not encodings_caras:
                return Response({"error": "No se detectó ningún rostro en la imagen."}, status=status.HTTP_400_BAD_REQUEST)

            coincidencias = face_recognition.compare_faces(encodings_conocidos, encodings_caras[0])
            nombre_reconocido = "Desconocido"

            if True in coincidencias:
                indice_coincidencia = coincidencias.index(True)
                nombre_reconocido = nombres_conocidos[indice_coincidencia]
                info_personaje = personajes_info[nombre_reconocido]

                return Response({"mensaje": "Rostro detectado correctamente.", "personaje": info_personaje}, status=status.HTTP_200_OK)

            return Response({"mensaje": "Rostro detectado, pero no coincide con ninguno registrado.", "nombre": nombre_reconocido}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#IMPORTANTE TRABAJAR CON ESTA VERSION DE NUMPY
#pip install numpy==1.25.1