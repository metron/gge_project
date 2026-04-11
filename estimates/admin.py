from django.contrib import admin
from .models import Estimate

@admin.register(Estimate)
class EstimateAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at')  # Что видим в списке
    list_filter = ('status',)  # Фильтр справа

