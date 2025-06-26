from django.db import models

class Pferd(models.Model):
    name = models.CharField(max_length=100)
    transponder_id = models.CharField(max_length=50, unique=True)
    paddock_nummer = models.CharField(max_length=10)
    bild = models.ImageField(upload_to='pferde/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.transponder_id})"

class Fuetterung(models.Model):
    pferd = models.ForeignKey(Pferd, related_name='fuetterungen', on_delete=models.CASCADE)
    start_zeit = models.TimeField()
    end_zeit = models.TimeField()

class ZugangHistorie(models.Model):
    pferd = models.ForeignKey(Pferd, on_delete=models.CASCADE)
    zeitpunkt = models.DateTimeField(auto_now_add=True)

    
class Zutritt(models.Model):
    pferd = models.ForeignKey(Pferd, on_delete=models.CASCADE, related_name="zutritte")
    zeit = models.DateTimeField(auto_now_add=True)


