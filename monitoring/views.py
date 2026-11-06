
from django.shortcuts import render
from django.db.models import Count, Avg

from equipment.models import Equipment
from predictions.models import Prediction


def dashboard(request):
    feature_fields = [
    'op_setting_1',
    'op_setting_2',
    'op_setting_3',
    'sensor_2',
    'sensor_3',
    'sensor_4',
    'sensor_6',
    'sensor_7',
    'sensor_8',
    'sensor_9',
    'sensor_11',
    'sensor_12',
    'sensor_13',
    'sensor_14',
    'sensor_15',
    'sensor_17',
    'sensor_20',
    'sensor_21',
]

    equipment_list = Equipment.objects.all()
    prediction_list = Prediction.objects.select_related(
    'equipment'
    ).order_by('-created_at')

    chart_predictions = list(prediction_list)[::-1]

    chart_labels = [
    f"Prediction {prediction.id}"
    for prediction in chart_predictions
    ]

    chart_values = [
    prediction.predicted_rul
    for prediction in chart_predictions
    ]
    chart_dates = [
    prediction.created_at.strftime('%d %b %Y, %H:%M:%S')
    for prediction in chart_predictions
    ]

    total_equipment = Equipment.objects.count()

    prediction_stats = Prediction.objects.aggregate(
        total_predictions=Count('id'),
        average_rul=Avg('predicted_rul')
    )

    context = {
        'equipment_list': equipment_list,
        'total_equipment': total_equipment,
        'total_predictions': prediction_stats['total_predictions'],
        'average_rul': prediction_stats['average_rul'],
        'prediction_list': prediction_list,
        'chart_labels': chart_labels,
        'chart_values': chart_values,
        'chart_dates': chart_dates,
        'feature_fields': feature_fields,
    }

    return render(request, 'dashboard.html', context)


def new_prediction(request):
    feature_fields = [
        'op_setting_1',
        'op_setting_2',
        'op_setting_3',
        'sensor_2',
        'sensor_3',
        'sensor_4',
        'sensor_6',
        'sensor_7',
        'sensor_8',
        'sensor_9',
        'sensor_11',
        'sensor_12',
        'sensor_13',
        'sensor_14',
        'sensor_15',
        'sensor_17',
        'sensor_20',
        'sensor_21',
    ]

    equipment_list = Equipment.objects.all()

    context = {
        'equipment_list': equipment_list,
        'feature_fields': feature_fields,
    }

    return render(request, 'new_prediction.html', context)

def prediction_history(request):
    prediction_list = Prediction.objects.select_related(
        'equipment'
    ).order_by('-created_at')

    context = {
        'prediction_list': prediction_list,
    }

    return render(request, 'prediction_history.html', context)

def rul_chart(request):
    chart_predictions = list(
        Prediction.objects.order_by('created_at')
    )

    chart_labels = [
        f"Prediction {prediction.id}"
        for prediction in chart_predictions
    ]

    chart_values = [
        prediction.predicted_rul
        for prediction in chart_predictions
    ]

    chart_dates = [
        prediction.created_at.strftime('%d %b %Y, %H:%M:%S')
        for prediction in chart_predictions
    ]

    context = {
        'chart_labels': chart_labels,
        'chart_values': chart_values,
        'chart_dates': chart_dates,
    }

    return render(request, 'rul_chart.html', context)
