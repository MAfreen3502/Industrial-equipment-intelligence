from rest_framework.test import APITestCase
from equipment.models import Equipment
from predictions.models import Prediction


class PredictionAPITests(APITestCase):

    def setUp(self):
        Equipment.objects.create(engine_id=1)
    def test_missing_engine_id_returns_400(self):

        response = self.client.post(
            '/api/predictions/',
            {'features': {}},
            format='json'
        )

        self.assertEqual(response.status_code, 400)

    def test_unknown_engine_id_returns_404(self):

        response = self.client.post(
            '/api/predictions/',
            {
                'engine_id': 999,
                'features': {}
            },
            format='json'
        )

        self.assertEqual(response.status_code, 404)

    def test_invalid_sensor_value_returns_400(self):

        response = self.client.post(
            '/api/predictions/',
            {
                'engine_id': 1,
                'features': {
                    'sensor_2': 'hello'
                }
            },
            format='json'
        )

        self.assertEqual(response.status_code, 400)

    def test_valid_prediction_is_created(self):

        features = {
            'op_setting_1': 0.0,
            'op_setting_2': 0.0,
            'op_setting_3': 100.0,
            'sensor_2': 642.0,
            'sensor_3': 1589.7,
            'sensor_4': 1400.6,
            'sensor_6': 14.62,
            'sensor_7': 21.61,
            'sensor_8': 554.36,
            'sensor_9': 2388.06,
            'sensor_11': 9046.19,
            'sensor_12': 1.3,
            'sensor_13': 47.47,
            'sensor_14': 521.66,
            'sensor_15': 2388.02,
            'sensor_17': 392,
            'sensor_20': 39.06,
            'sensor_21': 23.419
        }

        response = self.client.post(
            '/api/predictions/',
            {
                'engine_id': 1,
                'features': features
            },
            format='json'
        )

        self.assertEqual(response.status_code, 201)

        self.assertEqual(Prediction.objects.count(), 1)

        prediction = Prediction.objects.first()

        self.assertEqual(prediction.equipment.engine_id, 1)

        self.assertGreater(prediction.predicted_rul, 0)

        self.assertEqual(prediction.input_features, features)

        self.assertEqual(len(prediction.input_features), 18)