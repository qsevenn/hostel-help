from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from .forms import UserRegistrationForm, ReportForm, CustomAuthenticationForm, ContactForm
from .models import Report, Contact
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from verify_email.email_handler import send_verification_email
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token.token import account_activation_token  


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    extra_context = {'custom_login_error': 'Неправильно введені дані для логіну'}

def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)  
            mail_subject = 'Посилання для активації акаунту було надіслано на Ваш email.' 

            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  

            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Будь ласка підтвердіть вашу електронну адресу, щоб завершити реєстрацію.')  

            # messages.success(request, f'Your account has been created. You can log in now!')
            # return redirect('login')
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'register.html', context)


def activate(request, uidb64, token):  
    # users = User.objects.all()
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!')  


def login(request):
    # print(request.user.is_authenticated)
    # if request.user.is_authenticated:
    #     return render(request, 'profile.html', {'user': request.user})
    # else:
    return render(request, 'login.html')


def folders(request):
    if request.method == 'GET':
        if request.user.is_superuser:
            dormitories_available = list(Report.objects.order_by().values_list('dormitory').distinct())
            dormitories = []
            for d in dormitories_available:
                for val in d:
                    dormitories.append(val)
            print(dormitories)
            return render(request, 'folders.html', {'dormitories': dormitories})
        else:
            return HttpResponseNotFound("Сторінку не знайдено.")


def profile(request, dormitory=None):
    if request.method == 'POST':
        if request.user.is_superuser:
            reports = Report.objects.filter(dormitory=dormitory).order_by('-date')
            replies = Contact.objects.prefetch_related('report_id').filter(report_id__in=reports.values('id'))
            form = ContactForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                report_id = int(request.POST.get('report_id'))
                if report_id:
                    report = Report.objects.get(id=report_id)
                    instance.report_id = report
                instance.email = reports.get(id=report_id).email
                instance.date_report = Report.objects.get(id=report_id).date
                instance.save()
                subject = 'HOSTEL HELP KPI'
                message = instance.message
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [instance.email,]
                send_mail(subject, message, email_from, recipient_list, fail_silently=False)
                messages.success(request, f'Your message has been sent.')
                return redirect(reverse('profile', args=[dormitory]))
        # if request.user.is_authenticated:
        #     reports = Report.objects.filter(email=request.user.email).order_by('-date')
        #     replies = Contact.objects.filter(email=request.user.email)
    else:
        if request.user.is_superuser:
            # reports = Report.objects.filter(dormitory=dormitory).order_by('-date')
            reports = Report.objects.filter(dormitory=dormitory).order_by('-date')
            replies = Contact.objects.prefetch_related('report_id').filter(report_id__in=reports.values('id'))
            page = request.GET.get('page', 1)
            paginator = Paginator(reports, 8)
            try:
                reports = paginator.page(page)
            except PageNotAnInteger:
                reports = paginator.page(1)
            except EmptyPage:
                reports = paginator.page(paginator.num_pages)
            form = ContactForm()
            return render(request, 'profile.html', {'user': request.user,'form': form, 'reports': reports, 'replies': replies, 'dormitory': dormitory})
        if request.user.is_authenticated:
            reports = Report.objects.filter(email=request.user.email).order_by('-date')
            page = request.GET.get('page', 1)
            paginator = Paginator(reports, 8)
            try:
                reports = paginator.page(page)
            except PageNotAnInteger:
                reports = paginator.page(1)
            except EmptyPage:
                reports = paginator.page(paginator.num_pages)
            replies = Contact.objects.filter(email=request.user.email)
            return render(request, 'profile.html', {'user': request.user, 'reports': reports, 'replies': replies})



# def profile(request):
#     if request.method == 'POST':
#         if request.user.is_superuser:
#             replies = Contact.objects.all()
#             reports = Report.objects.all().order_by('-date')
#             form = ContactForm(request.POST)
#             if form.is_valid():
#                 instance = form.save(commit=False)
#                 report_id = int(request.POST.get('report_id'))
#                 if report_id:
#                     report = Report.objects.get(id=report_id)
#                     instance.report_id = report
#                 instance.email = reports.get(id=report_id).email
#                 instance.date_report = Report.objects.get(id=report_id).date
#                 instance.save()
#                 subject = 'HOSTEL HELP KPI'
#                 message = instance.message
#                 email_from = settings.EMAIL_HOST_USER
#                 recipient_list = [instance.email,]
#                 send_mail(subject, message, email_from, recipient_list, fail_silently=False)
#                 messages.success(request, f'Your message has been sent.')
#                 return redirect('profile')
#         # if request.user.is_authenticated:
#         #     reports = Report.objects.filter(email=request.user.email).order_by('-date')
#         #     replies = Contact.objects.filter(email=request.user.email)
#     else:
#         if request.user.is_superuser:
#             reports = Report.objects.all().order_by('-date')
#             page = request.GET.get('page', 1)
#             paginator = Paginator(reports, 8)
#             try:
#                 reports = paginator.page(page)
#             except PageNotAnInteger:
#                 reports = paginator.page(1)
#             except EmptyPage:
#                 reports = paginator.page(paginator.num_pages)

#             replies = Contact.objects.all()
#             form = ContactForm()
#             return render(request, 'profile.html', {'user': request.user,'form': form, 'reports': reports, 'replies': replies})
#         if request.user.is_authenticated:
#             reports = Report.objects.filter(email=request.user.email).order_by('-date')
#             page = request.GET.get('page', 1)
#             paginator = Paginator(reports, 8)
#             try:
#                 reports = paginator.page(page)
#             except PageNotAnInteger:
#                 reports = paginator.page(1)
#             except EmptyPage:
#                 reports = paginator.page(paginator.num_pages)
#             replies = Contact.objects.filter(email=request.user.email)
#             return render(request, 'profile.html', {'user': request.user, 'reports': reports, 'replies': replies})


def report(request):
    if request.user.is_authenticated:
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
    else:
        return HttpResponseBadRequest("Для повідомлення про проблему необхідно авторизуватись")


def delete_report(request, report_id, dormitory):
    # print(report_id)
    report_to_delete=Report.objects.get(id=report_id)
    report_to_delete.delete()
    return HttpResponseRedirect(reverse('profile', args=[dormitory]))


def change_status(request, report_id, dormitory):
    report_to_change = Report.objects.get(id=report_id)
    if report_to_change.status == "Неактивна":
        report_to_change.status = "Активна"
    elif report_to_change.status == "Активна":
        report_to_change.status = "Закрита"
    report_to_change.save()
    return HttpResponseRedirect(reverse('profile', args=[dormitory]))


def reply(request):
    return render(request, 'reply.html')