from django.db import models

class Profile(models.Model):
    user_id=models.CharField(max_length=20, unique=True)
    age=models.CharField(max_length=3)
    height=models.CharField(max_length=3)
    weight=models.CharField(max_length=3)
    city=models.CharField(max_length=30)
    address=models.CharField(max_length=50)
    mobile=models.CharField(max_length=20)