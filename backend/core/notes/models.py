from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    company = models.ForeignKey('invest.Company', on_delete=models.PROTECT)
    body = models.TextField()
    text = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']
