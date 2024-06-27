from django.db import models
from django.utils import timezone

class ResultUber(models.Model):
    class Meta:
        verbose_name = 'Resultado uber'
        verbose_name_plural = 'Resultados uber'
        
    gasto_por_km = models.FloatField()
    gasto_com_comb = models.FloatField()
    comb_com_desc = models.FloatField()
    ganho_por_km = models.FloatField()
    lucro = models.FloatField()
    data_criacao = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return 'Resultados'
    
