from django.contrib import admin
from uber import models

@admin.register(models.ResultUber)
class UberAdmin(admin.ModelAdmin):
    list_display = 'id', 'gasto_por_km', 'gasto_com_comb', 'comb_com_desc', 'ganho_por_km', 'lucro', 'data_criacao','owner'
    ordering = '-data_criacao',
    list_filter = 'data_criacao',
    search_fields = 'gasto_por_km', 'gasto_com_comb', 'comb_com_desc', 'ganho_por_km', 'lucro',
    list_per_page = 20
    list_display_links = 'id',
    