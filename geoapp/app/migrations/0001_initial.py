# Generated by Django 4.0.6 on 2022-08-04 04:53

import ckeditor.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='dzongkhag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to='static/data/boundary/%Y/%m/%d')),
                ('created_at', models.DateField(blank=True, default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('image', models.FileField(blank=True, upload_to='static/data/plan/cover/%Y/%m/%d')),
                ('dzongkhag', models.BigIntegerField(blank=True, choices=[(1, 'Bumthang'), (2, 'Chhukha'), (3, 'Dagana'), (4, 'Gasa'), (5, 'Haa'), (6, 'Lhuentse'), (7, 'Mongar'), (8, 'Paro'), (9, 'Pema Gatshel'), (10, 'Punakha'), (11, 'Samdrup Jongkhar'), (12, 'Samtse'), (13, 'Sarpang'), (14, 'Thimphu'), (15, 'Trashigang'), (16, 'Trashi Yangtse'), (17, 'Tsirang'), (18, 'Trongsa'), (19, 'Wangdue Phodrang'), (20, 'Zhemgang')])),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('plan_year', models.DateField(blank=True, default=datetime.date.today)),
                ('period_from', models.DateField(blank=True, default=datetime.date.today)),
                ('period_till', models.DateField(blank=True, default=datetime.date.today)),
                ('area', models.CharField(blank=True, max_length=100)),
                ('type', models.CharField(blank=True, choices=[('Structure Plan', 'Structure Plan'), ('Local Area Plan', 'Local Area Plan'), ('Regional Plan', 'Regional Plan'), ('Action Area Plan', 'Action Area Plan'), ('Valley Development Plan', 'Valley Development Plan')], max_length=800)),
            ],
        ),
        migrations.CreateModel(
            name='data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('database', models.CharField(blank=True, max_length=100)),
                ('boundary', models.FileField(blank=True, upload_to='static/data/plan/boundary/%Y/%m/%d')),
                ('precient', models.FileField(blank=True, upload_to='static/data/plan/precient/%Y/%m/%d')),
                ('plot', models.FileField(blank=True, upload_to='static/data/plan/plot/%Y/%m/%d')),
                ('created_at', models.DateField(blank=True, default=datetime.date.today)),
                ('plan', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='app.plan')),
            ],
        ),
    ]
