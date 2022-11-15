from django.contrib import admin

from hostel_help.models import Report

# Register your models here.
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    actions = ['delete', 'view']
    
    def has_change_permission(self, request, obj=None):
        return False
        # return super().has_change_permission(request, obj=obj)



