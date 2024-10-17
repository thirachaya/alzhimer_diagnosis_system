from django.db import models
from datetime import date

# Create your models here.

class Patient(models.Model):
    PREFIX_CHOICES = [
        ('Mr', 'นาย'),
        ('Ms', 'นางสาว'),
        ('Mrs', 'นาง'),
    ]

    patient_HN = models.AutoField(primary_key=True)
    patient_prefix = models.CharField(max_length=10, choices=PREFIX_CHOICES, default='Mr', null=False)
    patient_IDcard = models.CharField(max_length=13, unique=True)
    patient_firstName = models.CharField(max_length=255)
    patient_lastName = models.CharField(max_length=255)
    patient_birthdate = models.DateField()
    patient_UD = models.ManyToManyField('app_underlying_disease.UnderlyingDisease', blank=True)

    def __str__(self):
        return f"{self.patient_HN} - {self.patient_firstName} {self.patient_lastName}"
    
    @property
    def age(self):
        today = date.today()
        age = today.year - self.patient_birthdate.year - ((today.month, today.day) < (self.patient_birthdate.month, self.patient_birthdate.day))
        return age
    
    class Meta:
        verbose_name = 'ผู้ป่วย'
        verbose_name_plural = 'รายชื่อผู้ป่วย'