from django.test import TestCase
from django.urls import reverse
from equipment.models import Equipment
from predictions.models import Prediction


class DashboardTests(TestCase):

    def test_dashboard_loads_successfully(self):
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)

    def test_dashboard_statistics(self):
        equipment = Equipment.objects.create(engine_id=101)

        Prediction.objects.create(
            equipment=equipment,
            predicted_rul=100.0,
            input_features={}
        )

        Prediction.objects.create(
            equipment=equipment,
            predicted_rul=200.0,
            input_features={}
        )

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.context['total_equipment'], 1)
        self.assertEqual(response.context['total_predictions'], 2)
        self.assertEqual(response.context['average_rul'], 150.0)

    def test_dashboard_chart_data(self):
        equipment = Equipment.objects.create(engine_id=101)

        Prediction.objects.create(
            equipment=equipment,
            predicted_rul=100.0,
            input_features={}
        )

        Prediction.objects.create(
            equipment=equipment,
            predicted_rul=200.0,
            input_features={}
        )

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(
            len(response.context['chart_labels']),
            2
        )

        self.assertEqual(
            response.context['chart_values'],
            [100.0, 200.0]
        )

        self.assertEqual(
            len(response.context['chart_dates']),
            2
        )

    def test_new_prediction_page_loads(self):
        response = self.client.get(reverse('new_prediction'))
        self.assertEqual(response.status_code, 200)

    def test_prediction_history_page_loads(self):
        response = self.client.get(reverse('prediction_history'))
        self.assertEqual(response.status_code, 200)

    def test_rul_chart_page_loads(self):
        response = self.client.get(reverse('rul_chart'))
        self.assertEqual(response.status_code, 200)