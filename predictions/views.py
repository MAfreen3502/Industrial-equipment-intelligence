from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ml.predictor import predict_rul
from equipment.models import Equipment
from .models import Prediction


@api_view(['POST'])
def predict_rul_api(request):
    engine_id = request.data.get('engine_id')
    input_data = request.data.get('features')

    if engine_id is None or input_data is None:
        return Response({
            'error': 'Both engine_id and features are required.'
        }, status=status.HTTP_400_BAD_REQUEST)


    try:
        equipment = Equipment.objects.get(engine_id=engine_id)
        prediction = predict_rul(input_data)
        prediction_record = Prediction.objects.create(
            equipment=equipment,
            predicted_rul=prediction,
            input_features=input_data
        )

        return Response({
            'prediction_id': prediction_record.id,
            'engine_id': equipment.engine_id,
            'predicted_rul': prediction,
            'unit': 'operating cycles'
        }, status=status.HTTP_201_CREATED)

    except Equipment.DoesNotExist:
        return Response({
            'error': 'Equipment with the provided engine ID was not found.'
        }, status=status.HTTP_404_NOT_FOUND)


    except (ValueError, TypeError) as error:
        return Response({
            'error': str(error)
        }, status=status.HTTP_400_BAD_REQUEST)
    except FileNotFoundError:
        return Response({
            'error': 'Prediction service is currently unavailable.'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    except Exception:
        return Response({
            'error': 'An unexpected error occurred while generating the prediction.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)