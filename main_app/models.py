from django.db import models
from django.urls import reverse

MEDIA = (
    ('V', 'Vinyl'),
    ('S', 'Streaming'),
    ('C', 'CD'),
    ('T', 'Cassette')
)

# Create your models here.

class Musician(models.Model):
    name = models.CharField(max_length=100)
    instrument = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('musicians_detail', kwargs={'pk': self.id})

class Record(models.Model):
    name = models.CharField(max_length=50)
    artist = models.CharField(max_length=100, default='')
    record_label = models.CharField(max_length=50)
    release_date = models.DateField(auto_now=False, auto_now_add=False)
    musicians = models.ManyToManyField(Musician)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('records_detail', kwargs={'record_id': self.id})

class Listening(models.Model):
    date = models.DateField()
    medium = models.CharField(max_length=1, choices=MEDIA, default=MEDIA[1][0])
    whole = models.BooleanField(default=False)

    record = models.ForeignKey(Record, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_medium_display()} on {self.date}"
