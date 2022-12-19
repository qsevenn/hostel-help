from django.contrib import admin

from hostel_help.models import Report

# from .management.commands.send_email import send_mail


# Register your models here.
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    actions = ['delete', 'view', 'send_email']
    search_fields = ['problem_type']
    list_filter = ['date']
    
    def has_change_permission(self, request, obj=None):
        return False
        # return super().has_change_permission(request, obj=obj)
    
    def has_add_permission(self, request, obj=None):
        return False

    # def send_mail(self, request, obj=None)
