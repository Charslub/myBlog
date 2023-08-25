from django.db import models


# Create your models here.
class User(models.Model):
    id = models.BigAutoField(primary_key=True, unique=True)
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=15)
    is_admin = models.BooleanField()
    is_delete = models.BooleanField()
