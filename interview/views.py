import pytz
from datetime import datetime
from django.shortcuts import render, redirect

from .models import InterviewStudent
# Create your views here.

def interview_dashboard_view(request):
    sydney_tz = pytz.timezone('Australia/Sydney')
    sydney_time = datetime.now(sydney_tz)
    
    if 5 <= sydney_time.hour < 12:
        time_greeting = 'Good morning'
    elif 12 <= sydney_time.hour < 18:
        time_greeting = 'Good afternoon'
    else:
        time_greeting = 'Good evening'
    
    # Assuming there is a logged in user and the user has an associated InterviewStudent model
    user = request.user
    try:
        interview_student = InterviewStudent.objects.get(user = user)
    except:
        return redirect("/")

    interview_student = InterviewStudent.objects.get(user = user)
    title = 'Sir' if interview_student.gender == 'M' else 'Madam'
    
    return render(request, 'interview-dashboard.html', {'time_greeting': time_greeting, 'title': title})