from django.db import models

class Plug(models.Model):
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField()
