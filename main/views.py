from django.shortcuts import render
from datetime import datetime
from django.contrib import messages

def overview(request):
    month = datetime.now().strftime('%B')
    if month == 'April':
        messages.info(request, 'Happy Autism Awareness Month!')
    return render(request, 'main/overview.html', {})

def changelog(request):
    return render(request, 'main/changelog.html', {})
