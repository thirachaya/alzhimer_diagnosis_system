from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.urls import reverse
from app_general.froms import AddPatient
from .models import Patient
from app_diagnostic.models import Diagnostic
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from PIL import Image
from django.db import IntegrityError
from django.http import JsonResponse
import json
import numpy as np
import os

model = load_model('app_general/model/model.h5')

# Create your views here.
def home(request):
    return render(request, 'app_general/home.html')

def add_patient(request):
    if request.method == 'POST':
        form = AddPatient(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('add_patient_success'))
    else:
        form = AddPatient()
    context = {'form': form}
    return render(request, 'app_general/add_patient.html', context)

def add_patient_success(request):
    return render(request, 'app_general/add_patient_success.html')

def show_patient(request):
    query = request.GET.get('q')
    if query:
        patients = Patient.objects.filter(patient_firstName__icontains=query) | Patient.objects.filter(patient_lastName__icontains=query)
    else:
        patients = Patient.objects.all()
    
    context = {'patients': patients}
    return render(request, 'app_general/show_patient.html', context)

# ส่วนของการทำนายผล ---------------------------------------------------------------------
class_labels = {0: 'ระดับรุนแรงน้อย', 1: 'ระดับรุนแรงปานกลาง', 2: 'ไม่มีอาการ', 3: 'ระดับรุนแรงมาก'}

def patient_detail(request, patient_HN):
    patient = get_object_or_404(Patient, patient_HN=patient_HN)

    latest_diagnostic = Diagnostic.objects.filter(patient_HN=patient).order_by('-date').first()
    diagnostics = Diagnostic.objects.filter(patient_HN=patient).order_by('-date')
    error_message = None

    if request.method == 'POST' and 'predict' in request.FILES:
        image_file = request.FILES['predict']

        if image_file.content_type not in ['image/jpeg', 'image/jpg', 'image/png']:
            error_message = 'โปรดอัปโหลดไฟล์รูปภาพที่มีนามสกุล jpeg, jpg หรือ png'
        else:
            # ตรวจสอบขนาดของไฟล์
            img = Image.open(image_file)
            if img.width < 180 or img.height < 180:
                error_message = 'ขนาดภาพต้องไม่น้อยกว่า 180x180 พิกเซล'
            else:
                diagnostic = Diagnostic(patient_HN=patient, Ddx="Pending", recommend="")
                diagnostic.MRI_pic.save(image_file.name, image_file)
                diagnostic.date = timezone.now()
                diagnostic.save()

                image_path = diagnostic.MRI_pic.path
                img = load_img(image_path, target_size=(180, 180), color_mode='grayscale')
                img_array = img_to_array(img)
                img_array = np.expand_dims(img_array, axis=0)

                prediction = model.predict(img_array)
                prediction_class = np.argmax(prediction)
                prediction_label = class_labels[prediction_class]

                diagnostic.Ddx = prediction_label
                diagnostic.save()

                return redirect('prediction_result', patient_HN=patient_HN, prediction=prediction_class, diagnostic_id=diagnostic.id)

            
    context = {
        'patient': patient,
        'latest_diagnostic': latest_diagnostic,
        'diagnostics': diagnostics,
        'error_message': error_message, 
    }
    return render(request, 'app_general/patient_detail.html', context)

def prediction_result(request, patient_HN, prediction, diagnostic_id):
    patient = get_object_or_404(Patient, patient_HN=patient_HN)
    diagnostic = get_object_or_404(Diagnostic, id=diagnostic_id)

    if request.method == 'POST':
        recommend = request.POST.get('recommend') 
        if recommend:
            diagnostic.recommend = recommend 
            diagnostic.save()

        return redirect('patient_detail', patient_HN=patient_HN)
    

    context = {
        'patient': patient,
        'prediction': prediction,
        'diagnostic': diagnostic,
    }
    return render(request, 'app_general/prediction_result.html', context)

