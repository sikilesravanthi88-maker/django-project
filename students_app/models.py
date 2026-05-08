from django.db import models

class Students(models.Model):
    name = models.CharField(max_length=100)
