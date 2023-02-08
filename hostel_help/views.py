from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from .forms import UserRegistrationForm, ReportForm, CustomAuthenticationForm, ContactForm,\
    PasswordResetForm, SetPasswordResetForm
from .models import Report, Contact
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token.token import account_activation_token, password_reset_token
from django.db.models.query_utils import Q
from .models import Report


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
            mail_subject = 'Посилання для активації акаунта було надіслано на Ваш email.'

            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })  

            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse('Будь ласка, підтвердіть вашу електронну адресу, щоб завершити реєстрацію.')

    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'register.html', context)


def reset_password(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    user.is_active = False
                    user.save()

                    subject = "HOSTELHELP Скидання паролю"
                    email_template_name = "password_reset_email.html"
                    current_site = get_current_site(request) 
                    email_message = {
                        'user': user,  
                        'domain': current_site.domain,  
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': password_reset_token.make_token(user),
                    }
                    email = EmailMessage(  
                        subject, render_to_string(email_template_name, email_message), to=[user.email]
                    )  
                    email.send()  
                    user.is_active = False
                    return redirect("index")
    password_reset_form = PasswordResetForm()
    return render(request, "password_reset.html", context={"password_reset_form": password_reset_form})


def reset_password_confirm(request, uidb64, token):
    if request.method == 'POST':
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            messages.add_message(request, messages.WARNING, str(e))
            user = None

        if user is not None and password_reset_token.check_token(user, token):
            form = SetPasswordResetForm(user=user, data=request.POST)
            print(form.is_valid())
            if form.is_valid():

                form.save()
                update_session_auth_hash(request, form.user)
                user.is_active = True
                user.save()

                messages.add_message(request, messages.SUCCESS, 'Password reset successfully.')
                return redirect("password_reset_complete")
            else:
                context = {
                    'form': form,
                    'uid': uidb64,
                    'token': token
                }
                messages.add_message(request, messages.WARNING, 'Пароль не може бути змінений')
                return render(request, 'password_reset_confirm.html', context)
        else:
            messages.add_message(request, messages.WARNING, 'Посилання для скидання паролю не активне.')
            messages.add_message(request, messages.WARNING, 'Будь ласка, спробуйте отримати його ще раз')

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        messages.add_message(request, messages.WARNING, str(e))
        user = None

    if user is not None and password_reset_token.check_token(user, token):
        context = {
            'form': SetPasswordResetForm(user),
            'uid': uidb64,
            'token': token
        }
        return render(request, 'password_reset_confirm.html', context)
    else:
        messages.add_message(request, messages.WARNING, 'Посилання для скидання паролю не активне.')
        messages.add_message(request, messages.WARNING, 'Будь ласка, спробуйте отримати його ще раз.')

    return redirect('home')
            

def reset_password_complete(request):
    return render(request, 'password_reset_complete.html')


def activate(request, uidb64, token):  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()
        return redirect('index')
    else:  
        return HttpResponse('Посилання неактивне')


def folders(request):
    if request.method == 'GET':
        if request.user.is_superuser:
            dormitories_available = Report.DORMITORIES_CHOICES
            dormitories = []
            for d in dormitories_available:
                dormitories.append(d[0])
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
                print(report_id)
                if report_id:
                    report = Report.objects.get(id=report_id)
                    instance.report_id = report
                instance.email = reports.get(id=report_id).email
                instance.date_report = Report.objects.get(id=report_id).date
                instance.save()
                subject = 'HOSTEL HELP KPI'
                message = instance.message
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [instance.email, ]
                send_mail(subject, message, email_from, recipient_list, fail_silently=False)
                messages.success(request, f'Your message has been sent.')
                return redirect(reverse('profile', args=[dormitory]))
    else:
        if request.user.is_superuser:
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
            return render(request, 'profile.html', {'user': request.user,
                                                    'form': form,
                                                    'reports': reports,
                                                    'replies': replies,
                                                    'dormitory': dormitory})
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


def report(request):
    if request.user.is_authenticated and not request.user.is_superuser and not request.user.is_staff:
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
        return HttpResponseBadRequest("Сторінка недоступна")


def delete_report(request, report_id, dormitory):
    # print(report_id)
    report_to_delete = Report.objects.get(id=report_id)
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
