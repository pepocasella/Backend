from django.contrib import admin
from .models import Estacao, Sensor

@admin.register(Estacao)
class EstacaoAdmin(admin.ModelAdmin):
    list_display = ["nome", "localizacao"]

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ["sensor", "valor", "unidade", "timestamp", "estacao"]
    list_filter = ["sensor", "timestamp"]
    search_fields = ["sensor", "estacao__nome"]