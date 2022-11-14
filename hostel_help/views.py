from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    return HttpResponse("Hello, radyna!")


def register(request):
    return render(request, 'register.html')


def login(request):
    return render(request, 'login.html')


def profile(request):
    return render(request, 'profile.html')

def report(request):
    return render(request, 'report-problem.html')