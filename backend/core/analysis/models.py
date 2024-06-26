from django.db import models


class CompanyAnalysis(models.Model):
    company = models.ForeignKey('invest.Company', on_delete=models.CASCADE)
    report = models.ForeignKey('invest.Report', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # AnalysisFields
    entreprise_value = models.FloatField()
    ebitda = models.FloatField()
    peg = models.FloatField()

    class Meta:
        verbose_name = 'Analysis'
        verbose_name_plural = 'Analysis'

