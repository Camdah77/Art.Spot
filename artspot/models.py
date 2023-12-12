from django.db import models

class Artwork(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    artist = models.CharField(max_length=50, null=False, blank=False)
    length = models.PositiveIntegerField(db_column='length')
    width = models.PositiveIntegerField(db_column='widht')
    depth = models.PositiveIntegerField()
    category = models.CharField(max_length=50, null=False, blank=False)
    medium = models.CharField(max_length=50, null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name
