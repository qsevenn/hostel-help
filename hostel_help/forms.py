from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Contact, Report


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=101, label='Ім\'я')
    last_name = forms.CharField(max_length=101, label='Прізвище')
    email = forms.EmailField(required=True, label='Електронна пошта')
    password1 = forms.CharField(label='Пароль', strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Підтвердження паролю', strip=False, widget=forms.PasswordInput)
    error_messages = {
        'password_mismatch': 'Паролі не співпадають.'
    }

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password1']
        labels = {
            'username': 'Псевдонім',
            'first_name': 'Ім`я',
            'last_name': 'Прізвище',
            'email': 'Email',
            'password1': 'Пароль',
            'password2': 'Повторно пароль'
        }

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error('email', "Електронна пошта занята.")
            raise forms.ValidationError("Електронна пошта занята.")

        return self.cleaned_data

    def clean_username(self):
        data = self.cleaned_data['username']
        user_model = get_user_model()
        if user_model.objects.filter(username=data).exists():
            raise ValidationError("Ім'я користувача заняте.")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254, label='Ім\'я користувача')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': 'Введіть коректне ім\'я користувача і пароль',
        'inactive': 'Цей аккаунт неактивний.',
        'invalid_password': 'Невірно введений пароль'
    }


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(required=True, label='Електронна пошта')


    def clean(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            self.add_error('email', "За даною електронною поштою не знайдено користувача.")
            raise forms.ValidationError("За даною електронною поштою не знайдено користувача.")


class SetPasswordResetForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Пароль',
        help_text=False,
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-reset',
                'placeholder': 'Введіть пароль',
                'type': 'password',
                'id': 'user_password',
            }
        ))

    new_password2 = forms.CharField(
        label='Підтвердіть пароль',
        help_text=False,
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-reset',
                'placeholder': 'Введіть пароль ще раз',
                'type': 'password',
                'id': 'user_password',
            }
        ))
        
    error_messages = {
        'password_mismatch': 'Паролі не співпадають.'
    }


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'problem_type', 'dormitory', 'exact_place',
                  'description']
        labels = {
            'title':  'Проблема',
            'problem_type': "Тип проблеми",
            'dormitory': "Номер гуртожитка",
            'exact_place': "Де саме потрібна допомога?",
            'description': "Опис"
        }

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['exact_place'].widget.attrs['placeholder'] = "Номер кімнати чи поверх"
        self.fields['description'].widget.attrs['placeholder'] = "Введіть короткий опис проблеми..."

    def clean(self):
        title = self.cleaned_data.get('title')
        problem_type = self.cleaned_data.get('problem_type')
        dormitory = self.cleaned_data.get('dormitory')
        exact_place = self.cleaned_data.get('exact_place')
        description = self.cleaned_data.get('description')
        if not title or not problem_type or not dormitory or not exact_place or not description:
            raise forms.ValidationError("Ви повинні заповнити всі поля!")
        return self.cleaned_data
        

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['message']
        labels = {'message': "Введіть своє повідомлення"}

    def clean(self):
        message = self.cleaned_data.get('message')
        if not message:
            raise forms.ValidationError("Ви повинні заповнити всі поля!")
        return self.cleaned_data
