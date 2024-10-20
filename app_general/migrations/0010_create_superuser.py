from django.db import migrations

def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.create_superuser(
        username='teerachaya',  # เปลี่ยนชื่อผู้ใช้
        email='chaya.fact@gmail.com',  # เปลี่ยนอีเมล
        password='20011226'  # เปลี่ยนรหัสผ่าน
    )

class Migration(migrations.Migration):

    dependencies = [
        ('app_general', '0009_remove_patient_patient_ud_patient_patient_ud'),  # อัปเดตให้ตรงกับ migration ล่าสุดของคุณ
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
