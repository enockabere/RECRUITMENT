from django.db import models

# Create your models here.


class Users(models.Model):
    firstname = models.CharField(max_length=200, blank=True)
    lastname = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.firstname
