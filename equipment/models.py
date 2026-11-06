from django.db import models


class Equipment(models.Model):

    engine_id = models.PositiveIntegerField(unique=True)

    equipment_type = models.CharField(
        max_length=100,
        default='Simulated Turbofan Engine'
    )

    dataset = models.CharField(
        max_length=100,
        default='NASA C-MAPSS FD001'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Engine {self.engine_id}"
