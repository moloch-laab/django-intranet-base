from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    path = models.CharField(null=True, max_length=200)
