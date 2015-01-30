from django.db import models


class RequestLogV1(models.Model):
    project = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)