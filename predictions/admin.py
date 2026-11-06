from django.contrib import admin
from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):

    list_display = (
        'equipment',
        'predicted_rul',
        'created_at'
    )

    search_fields = ('equipment__engine_id',)