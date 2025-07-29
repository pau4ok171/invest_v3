from apps.invest.models import Company
from django.db import models
from apps.statements.types import Level, Type, Area, Status, Severity

LEVEL_CHOICES = Level.as_dict()
AREA_CHOICES = Area.as_dict()
TYPE_CHOICES = Type.as_dict()
STATUS_CHOICES = Status.as_dict()
SEVERITY_CHOICES = Severity.as_dict()


class Statement(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='statement')
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    question = models.CharField(max_length=255)
    level = models.CharField(choices=LEVEL_CHOICES, max_length=255)
    area = models.CharField(choices=AREA_CHOICES, max_length=255)
    type = models.CharField(choices=TYPE_CHOICES, max_length=255)
    status = models.CharField(choices=STATUS_CHOICES, max_length=255)
    severity = models.CharField(choices=SEVERITY_CHOICES, max_length=255)
    outcome = models.IntegerField()
