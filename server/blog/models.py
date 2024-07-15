from django.db import models
from security.models import Profile


class KeywordData(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    added = models.DateTimeField(auto_now_add=True)
    json = models.JSONField()
    profiles = models.ManyToManyField(Profile)

class Keyword(models.Model):
    name = models.CharField(max_length=200)
    profiles = models.ManyToManyField(Profile)
    