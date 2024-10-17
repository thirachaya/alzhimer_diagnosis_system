from django.contrib import admin
from app_diagnostic.models import Diagnostic
from app_general.models import Patient
from app_general.admin import admin_site

# Register your models here.

class DiagnosticAdmin(admin.ModelAdmin):
    list_display = ['patient_HN', 'patient_full_name', 'date', 'Ddx', 'MRI_pic', 'recommend']
    search_fields = ['patient_HN__patient_firstName', 'patient_HN__patient_lastName']

    def patient_full_name(self, obj):
        return f"{obj.patient_HN.patient_firstName} {obj.patient_HN.patient_lastName}"
    patient_full_name.short_description = 'ชื่อผู้ป่วย'


admin_site.register(Diagnostic, DiagnosticAdmin)
