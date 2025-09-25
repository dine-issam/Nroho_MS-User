from django.db import models

# Create your models here.
class User(models.Model):
    idUser = models.AutoField(primary_key=True)
    firebase_uid = models.CharField(max_length=128, unique=True, null=True, blank=True)
  # Link to Firebase
    name = models.CharField(max_length=25)
    email = models.EmailField(max_length=50, unique=True)
    plan = models.CharField(max_length=50, default="FREE")
    
    def __str__(self):
        return self.email
