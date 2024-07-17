from django.db import models
from security.models import Profile


class KeywordData(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    json = models.JSONField()
    filters = models.JSONField(null=True)  

class KeywordCluster(models.Model):
    name = models.CharField(max_length=200)
    keywords = models.ManyToManyField('Keyword', blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

class Keyword(models.Model):
    name = models.CharField(max_length=200, primary_key=True) 

class APIUsed(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    
class APICostRecord(models.Model):
    cost = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    api_used = models.ForeignKey(APIUsed, on_delete=models.CASCADE)