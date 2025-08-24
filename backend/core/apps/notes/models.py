from django.db import models
from django.contrib.auth.models import User

from apps.invest.models import Instrument


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, related_name='notes')
    body = models.TextField()
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
