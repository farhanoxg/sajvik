from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import College

@api_view(['GET'])
def get_filtered_options(request):
    print(request)
    # durations = College.objects.values_list('duration', flat=True).distinct().order_by('duration')
    # seat_types = College.objects.values_list('seat_type', flat=True).distinct().order_by('seat_type')
    # genders = College.objects.values_list('gender', flat=True).distinct()

    return Response({
        # 'durations': (durations),
        # 'seat_types':(seat_types),
        # 'genders':(genders)
    })


@api_view(['POST'])
def get_filtered_colleges(request):
    try:
        rank = int(request.data.get('rank'))
    except (ValueError, TypeError):
        return Response({"msg": "Invalid rank provided. Please enter a valid number."}, status=400)

    duration = request.data.get('duration')
    course = request.data.get('course')
    seat_type = request.data.get('seat_type')
    gender = request.data.get('gender')
    pwd_checkbox = request.data.get('pwd_checkbox')

    if rank <= 0:
        return Response({"msg": "Rank must be a positive number."}, status=400)

    range_value = max(2, int(rank * 0.1)) #120*0.1=12
    lower_bound = rank - range_value #120-12=108
    upper_bound = rank + range_value #120+12=132

    if gender == 'female':
        gender_filter = ['Gender-Neutral', 'Female-only (including Supernumerary)'] 
    elif gender=='male':
        gender_filter = ['Gender-Neutral'] 
    else:
        return Response({"msg":"Invalid Gender input, plz give male or female"}, status=400) 

   

    if seat_type:
        if pwd_checkbox:
            seat_type += ' (PwD)' 
    else:
        return Response({"msg": "Seat type is required."}, status=400)

    if duration and course:
        duration = f"{duration} {course}"  
    else:
        return Response({"msg": "Duration and course are required."}, status=400)

    filtered_colleges = College.objects.filter(
        seat_type=seat_type,
        gender__in=gender_filter,  
        duration=duration,
        closing_rank__gte=lower_bound,
        # closing_rank__lte=upper_bound,
    ).order_by('closing_rank')

    if not filtered_colleges.exists():
        return Response({"msg": "No colleges found for the given rank."}, status=404)

    result = [{
         "number": index + 1,
        "institute_name": college.institute_name,
        "program_name": college.program_name,
        "duration": college.duration,
        "seat_type": college.seat_type,
        "gender": college.gender,
        "closing_rank": college.closing_rank
    } for index,college in enumerate(filtered_colleges)]

    return Response(result)
