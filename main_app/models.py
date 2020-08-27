from django.db import models

# Create your models here.

class Record(models.Model):
    name = models.CharField(max_length=50)
    record_label = models.CharField(max_length=50)
    release_year = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.name