from django.db import models

# Create your models here.


class Image(models.Model):
    Nitrogen = models.FloatField()
    Fosfor = models.FloatField()
    Kalium = models.FloatField()
    image = models.ImageField(upload_to="images/")  # Kolom untuk gambar
    tanaman = models.CharField(max_length=100)
    perbaikan = models.BooleanField(default=False)

    def __str__(self):
        return f"Image - Tanaman: {self.tanaman}"
