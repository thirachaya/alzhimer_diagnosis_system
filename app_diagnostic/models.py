from django.db import models
from django.utils import timezone

# Create your models here.

class Diagnostic(models.Model):
    patient_HN = models.ForeignKey('app_general.Patient', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    Ddx = models.CharField(max_length=255)
    MRI_pic = models.ImageField(upload_to='uploaded_images/', null=True, blank=True, max_length=255)
    recommend = models.TextField(max_length=500)

    class Meta:
        unique_together = ('patient_HN', 'date')
        verbose_name = 'การวินิจฉัย'
        verbose_name_plural = 'ประวัติการวินิจฉัย'
