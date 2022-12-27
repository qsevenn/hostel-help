from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.CustomLoginView.as_view(template_name='index.html'), name='index'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('password_reset/', views.reset_password, name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         views.reset_password_confirm, name='password_reset_confirm'),
    path('password-reset-complete/',
         views.reset_password_complete, name='password_reset_complete'),

    path('profile/', views.profile, name='profile'),

    path('profile/<int:dormitory>/', views.profile, name='profile'),
    path('folders/', views.folders, name='folders'),

    path('delete/<int:dormitory>/<int:report_id>/', views.delete_report, name='delete_report'),
    path('report/', views.report, name='report'),
    path('change_status/<int:dormitory>/<int:report_id>/', views.change_status, name='change_status'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         views.activate, name='activate'),
]
