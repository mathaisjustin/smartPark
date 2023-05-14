from django.db import models

# Create your models here.


class Subscriptions(models.Model):
    name = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)
    uid = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)
