from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('add_patient', views.add_patient, name='add_patient'),
    path('add_patient/success', views.add_patient_success, name='add_patient_success'),
    path('show_patient', views.show_patient, name='show_patient'),
    path('show_patient/<int:patient_HN>', views.patient_detail, name='patient_detail'),
    path('show_patient/<str:patient_HN>/prediction/<int:prediction>/<int:diagnostic_id>/', views.prediction_result, name='prediction_result'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)