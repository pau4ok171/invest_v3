from django.db import models
from django.contrib.auth.models import User

from apps.invest.models import Company


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='notes')
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='notes')
    body = models.TextField()
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
