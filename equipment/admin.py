from django.contrib import admin
from .models import Equipment


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):

    list_display = (
        'engine_id',
        'equipment_type',
        'dataset',
        'created_at'
    )

    search_fields = ('engine_id', 'dataset')
