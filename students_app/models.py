from django.db import models

class Students(models.Model):
    roll_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.name