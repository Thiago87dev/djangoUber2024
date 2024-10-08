from django.db import models
from django.contrib.auth.models import User


class ResultUber(models.Model):
    class Meta:
        verbose_name = 'Resultado uber'
        verbose_name_plural = 'Resultados uber'

    gasto_por_km = models.FloatField()
    gasto_com_comb = models.FloatField()
    comb_com_desc = models.FloatField()
    ganho_por_km = models.FloatField()
    lucro = models.FloatField()
    data_criacao = models.DateField()
    preco_comb = models.FloatField()
    km_rodado = models.FloatField()
    horas_trab = models.TimeField(blank=True, null=True)
    faturamento = models.FloatField()
    km_por_litro = models.FloatField()
    ganho_hora = models.FloatField()
    observacao = models.TextField()
    desc_comb = models.FloatField()
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return 'Resultados'
