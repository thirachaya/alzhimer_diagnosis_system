from django.contrib import admin
from app_general.admin import admin_site
from app_underlying_disease.models import UnderlyingDisease

# Register your models here.

class UnderlyingDiseaseAdmin(admin.ModelAdmin):
    list_display = ['UD_no', 'nameUD']
    search_fields = ['nameUD']


admin_site.register(UnderlyingDisease, UnderlyingDiseaseAdmin)