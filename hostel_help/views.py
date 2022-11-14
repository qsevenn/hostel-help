from django.shortcuts import render
from django.http import HttpResponse
from .models import Report
# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):
    return render(request, 'register.html')


def login(request):
    return render(request, 'login.html')


def profile(request):
    if request.method == "POST":
        if request.POST.get('title') and request.POST.get('problem_type') and request.POST.get('description'):
            new_report = Report()
            new_report.title = request.POST.get('title')
            new_report.problem_type = request.POST.get('problem_type')
            new_report.description = request.POST.get('description')
            new_report.save()
            return render(request, 'profile.html')
    return render(request, 'report-problem.html')

def report(request):
    return render(request, 'report-problem.html')