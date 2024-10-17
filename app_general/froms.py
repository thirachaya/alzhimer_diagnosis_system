from django import forms
from django.forms.widgets import Select
from django.forms.widgets import SelectMultiple
from django.db.models.base import Model
from .models import Patient
from app_underlying_disease.models import UnderlyingDisease
from django_select2.forms import Select2MultipleWidget
import re
from django.core.exceptions import ValidationError

class AddPatient(forms.ModelForm):
    PREFIX_CHOICES = [
        ('Mr', 'นาย'),
        ('Ms', 'นางสาว'),
        ('Mrs', 'นาง'),
    ]

    patient_prefix = forms.ChoiceField(
        choices=PREFIX_CHOICES, 
        label='คำนำหน้า',
        required=True
    )

    patient_UD = forms.ModelMultipleChoiceField(
        queryset=UnderlyingDisease.objects.all(),
        widget=SelectMultiple(attrs={'class': 'form-select', 'size': '4'}),
        label='โรคประจำตัว',
        required=False,
    )

    patient_birthdate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='วัน/เดือน/ปีเกิด',
        required=True
    )
    class Meta:
        model = Patient
        fields = ['patient_prefix', 'patient_IDcard', 'patient_firstName', 'patient_lastName', 
                  'patient_birthdate', 'patient_UD']
        labels = {
            'patient_prefix': 'คำนำหน้า',
            'patient_IDcard': 'เลขประจำตัวประชาชน 13 หลัก (เฉพาะตัวเลข)',
            'patient_firstName': 'ชื่อ',
            'patient_lastName': 'นามสกุล',
            'patient_birthdate': 'วัน/เดือน/ปีเกิด',
            'patient_UD': 'โรคประจำตัว'
        }

    def clean_patient_IDcard(self):
        data = self.cleaned_data['patient_IDcard']
    # ตรวจสอบว่ามี 13 หลักหรือไม่
        if not re.match(r'^\d{13}$', data):
            raise ValidationError('เลขประจำตัวประชาชนต้องเป็นตัวเลข 13 หลักเท่านั้น')
    # ตรวจสอบว่ามีอยู่ในระบบหรือไม่
        if Patient.objects.filter(patient_IDcard=data).exists():
            raise ValidationError('มีข้อมูลเลขประจำตัวประชาชนนี้อยู่แล้วในระบบ')
    # ตรวจสอบตามสูตรการคำนวณ
        def check_thai_id(id_number):
            digits = list(map(int, id_number))
            checksum = sum([(13-i) * digits[i] for i in range(12)]) % 11
            check_digit = (11 - checksum) % 10
            return check_digit == digits[12]
        if not check_thai_id(data):
            raise ValidationError('เลขประจำตัวประชาชนไม่ถูกต้องตามรูปแบบที่กำหนด')
        return data

    def clean_patient_firstName(self):
        data = self.cleaned_data['patient_firstName']
        if not re.match(r'^[ก-๙a-zA-Z]+$', data):
            raise ValidationError('ชื่อควรเป็นตัวอักษรเท่านั้น ห้ามมีตัวเลขหรือตัวอักษรพิเศษ')
        return data

    def clean_patient_lastName(self):
        data = self.cleaned_data['patient_lastName']
        if not re.match(r'^[ก-๙a-zA-Z]+$', data):
            raise ValidationError('นามสกุลควรเป็นตัวอักษรเท่านั้น ห้ามมีตัวเลขหรือตัวอักษรพิเศษ')
        return data