# Generated by Django 4.0.6 on 2022-08-31 03:27

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
                ('file', models.FileField(upload_to='static/data/dzongkhag/%Y/%m/%d')),
                ('created_at', models.DateField(blank=True, default=datetime.date.today)),
            ],
            options={
                'verbose_name_plural': '1. Dzongkhag Boundary',
            },
        ),
        migrations.CreateModel(
            name='plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('table', models.CharField(blank=True, max_length=100)),
                ('image', models.FileField(blank=True, upload_to='static/data/plan/cover')),
                ('dzongkhag', models.BigIntegerField(blank=True, choices=[(1, 'Bumthang'), (2, 'Chhukha'), (3, 'Dagana'), (4, 'Gasa'), (5, 'Haa'), (6, 'Lhuentse'), (7, 'Mongar'), (8, 'Paro'), (9, 'Pema Gatshel'), (10, 'Punakha'), (11, 'Samdrup Jongkhar'), (12, 'Samtse'), (13, 'Sarpang'), (14, 'Thimphu'), (15, 'Trashigang'), (16, 'Trashi Yangtse'), (17, 'Tsirang'), (18, 'Trongsa'), (19, 'Wangdue Phodrang'), (20, 'Zhemgang')])),
                ('area', models.CharField(blank=True, max_length=100)),
                ('plan_date', models.DateField(blank=True, default=datetime.date.today)),
                ('approved_date', models.DateField(blank=True, default=datetime.date.today)),
                ('approved_by', models.CharField(blank=True, choices=[('PPCM', 'PPCM'), ('NCHS', 'NCHS'), ('NCCHS', 'NCCHS'), ('UNKNOWN', 'UNKNOWN'), ('LG', 'LG')], max_length=100)),
                ('period_from', models.DateField(blank=True, default=datetime.date.today)),
                ('period_till', models.DateField(blank=True, default=datetime.date.today)),
                ('description', ckeditor.fields.RichTextField(blank=True)),
                ('dcr', models.FileField(blank=True, upload_to='static/data/plan/dcr')),
                ('report', models.FileField(blank=True, upload_to='static/data/plan/report')),
                ('type', models.CharField(blank=True, choices=[('National Plan', 'National Plan'), ('Regional Development Plan', 'Regional Development Plan'), ('Local Spatail Plan', 'Local Spatail Plan'), ('Action Area Plan', 'Action Area Plan')], max_length=800)),
            ],
            options={
                'verbose_name_plural': '2. Plans Detail',
            },
        ),
        migrations.CreateModel(
            name='data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('database', models.CharField(blank=True, max_length=200)),
                ('boundary', models.FileField(blank=True, upload_to='static/data/plan/boundary/%Y/%m/%d')),
                ('precient', models.FileField(blank=True, upload_to='static/data/plan/precient/%Y/%m/%d')),
                ('drawing', models.FileField(blank=True, upload_to='static/data/plan/cad/%Y/%m/%d')),
                ('updated_by', models.CharField(blank=True, max_length=100)),
                ('excel', models.FileField(blank=True, upload_to='static/data/plan/excel')),
                ('created_at', models.DateField(blank=True, default=datetime.date.today)),
                ('plan', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='app.plan')),
            ],
            options={
                'verbose_name_plural': '3. Plans Data',
            },
        ),
    ]
