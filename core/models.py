from django.db import models

class Personaje(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    apellido = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True,null=True)
    edad = models.IntegerField()
    imagen_referencia = models.URLField()  # URL de Cloudinary
    cedula=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
