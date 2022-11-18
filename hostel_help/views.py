from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, ReportForm
# from .models import Report, Contact


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
    return render(request, 'profile.html')


def report(request):
    if request.method == "POST":
        form = ReportForm(request.POST, initial={'email': request.user.email})
        if form.is_valid():
            instance = form.save(commit=False)
            email = request.user.email
            instance.email = email
            instance.save()
            messages.success(request, f'Your report has been accepted.')
            return redirect('profile')
    else:
        form = ReportForm()

    context = {'form': form}
    return render(request, 'report-problem.html', context)

def reply(request):
    return render(request, 'reply.html')