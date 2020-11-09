from django.db import models


class Deal(models.Model):
    customer = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    total = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    date = models.DateTimeField()
