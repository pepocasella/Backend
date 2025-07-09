from django.db import models
from django.conf import settings
from est_accounts.models import User


class EstBase(models.Model):
    criado_em = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    modificado_em = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        abstract = True


class Estacao(EstBase):
    nome = models.CharField("Identificador da Estação", max_length=100)
    localizacao = models.CharField("Localização", max_length=255)
    criado_por = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.nome} - {self.localizacao}"


class Sensor(EstBase):
    estacao = models.ForeignKey(
        Estacao,
        on_delete=models.CASCADE,
        related_name="leituras"
    )
    timestamp = models.DateTimeField("Data/Hora da Medição", auto_now_add=True)
    sensor = models.CharField("Tipo de Sensor", max_length=50)  
    medida = models.CharField("Medida", max_length=50)  
    valor = models.FloatField("Valor Medido")
    unidade = models.CharField("Unidade", max_length=20) 

    def __str__(self):
        return f"{self.sensor} | {self.valor} {self.unidade} @ {self.timestamp}"
