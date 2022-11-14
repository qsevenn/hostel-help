from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from .models import Report


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():

            form.save()

            messages.success(request, f'Your account has been created. You can log in now!')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'register.html', context)


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