from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import College

@api_view(['GET'])
def get_filtered_options(request):
    durations = College.objects.values_list('duration', flat=True).distinct()
    seat_types = College.objects.values_list('seat_type', flat=True).distinct()
    genders = College.objects.values_list('gender', flat=True).distinct()

    return Response({
        'durations': (durations),
        'seat_types':(seat_types),
        'genders':(genders)
    })

@api_view(['POST'])
def get_filtered_colleges(request):
    try:
        rank = int(request.data.get('rank'))
    except (ValueError, TypeError):
        return Response({"msg": "Invalid rank provided. Please enter a valid number."}, status=400)

    duration = request.data.get('duration')
    seat_type = request.data.get('seat_type')
    gender = request.data.get('gender')

    if rank <= 0:
        return Response({"msg": "Rank must be a positive number."}, status=400)

    range_value = max(1, int(rank * 0.1)) 
    lower_bound = rank - range_value

    filtered_colleges = College.objects.filter(
        seat_type=seat_type,
        gender=gender,
        duration=duration,
        closing_rank__gte=lower_bound
    ).order_by('closing_rank')

    if not filtered_colleges.exists():
        return Response({"msg": "No colleges found for the given rank."}, status=404)

    result = [{
        # "number": index + 1,
        "institute_name": college.institute_name,
        "program_name": college.program_name,
        "duration": college.duration,
        "seat_type": college.seat_type,
        "gender": college.gender,
        "closing_rank": college.closing_rank
    } for index,college in enumerate(filtered_colleges)]

    return Response(result)