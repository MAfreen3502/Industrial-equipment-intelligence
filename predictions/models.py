from django.db import models
from equipment.models import Equipment


class Prediction(models.Model):

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='predictions'
    )

    predicted_rul = models.FloatField()

    input_features = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Prediction for {self.equipment} "
            f"- RUL: {self.predicted_rul}"
        )