from django.contrib import admin
from django.contrib.admin import AdminSite
from app_general.models import Patient
from django.contrib.auth.models import User
from django.utils.html import format_html

# Register your models here.

class CustomAdminSite(AdminSite):
    site_header = 'การจัดการข้อมูลของ ระบบวินิจฉัยและประเมินอาการผู้ป่วยโรคอัลไซเมอร์'
    site_title = 'Alzheimer Diagnosis System'
    index_title = 'การจัดการข้อมูล'

    def get_urls(self):
        urls = super().get_urls()
        return urls

admin_site = CustomAdminSite(name='custom_admin')

admin_site.register(User)

class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_HN', 'patient_IDcard', 'patient_firstName', 'patient_lastName', 
                  'patient_birthdate', 'display_underlying_diseases']
    search_fields = ['patient_HN', 'patient_firstName', 'patient_lastName']

    @admin.display(description='โรคประจำตัว')
    def display_underlying_diseases(self, obj):
        diseases = obj.patient_UD.all()
        if diseases:
            return format_html('<br>'.join([d.nameUD for d in diseases]))
        return 'ไม่มี'

    class Media:
        css = {
            'all': ('app_general/css/admin_custom.css',),
        }

admin_site.register(Patient, PatientAdmin)

