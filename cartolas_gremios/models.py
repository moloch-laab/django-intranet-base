from django.db import models

class Cartola(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published',auto_now_add=True)
    path = models.CharField(null=True, max_length=200)
