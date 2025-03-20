from django.urls import path
from .views import ReconocimientoFacialAPI

urlpatterns = [
    path('reconocimiento-facial/', ReconocimientoFacialAPI.as_view(), name="reconocimiento_facial"),
]

#http://127.0.0.1:8000/api/reconocimiento-facial/

#IMPORTANTE TRABAJAR CON ESTA VERSION DE NUMPY
#pip install numpy==1.25.1