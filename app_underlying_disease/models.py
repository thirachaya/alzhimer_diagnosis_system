from django.db import models

# Create your models here.

class UnderlyingDisease(models.Model):
    UD_no = models.AutoField(primary_key=True)
    nameUD = models.CharField(max_length=255)

    def __str__(self) -> str:
        return '{}'.format(self.nameUD, self.UD_no)
    
    class Meta:
        verbose_name = 'โรคประจำตัว'
        verbose_name_plural = 'ชื่อโรคประจำตัว'