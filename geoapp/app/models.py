from django.db import models
import datetime
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms import DateField
import geopandas as gpd
import os 
import glob
import zipfile
from sqlalchemy import *
from geoalchemy2 import *

# Create your models here.


# Modal to upload dzongkhags boundray shapefile


class dzongkhag(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='static/data/boundary/%Y/%m/%d')
    created_at = models.DateField(default=datetime.date.today, blank=True)

    def __str__(self):
        return self.name


@receiver(post_save,sender=dzongkhag)
def pusblish_boundary(sender, instance, created, **kwargs):
    file = instance.file.path
    file_format = os.path.basename(file).split('.')[-1]
    file_name = os.path.basename(file).split('.')[0]
    file_path = os.path.dirname(file)
    name = instance.name.lower()
    conn_str = 'postgresql://postgres:kali339456@localhost:5432/geo'

    # extract zipfile
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(file_path)

   # Get shapefile
    shp = glob.glob(r'{}/**/*.shp'.format(file_path),recursive=True)

    try:
        req_shp = shp[0]
        gdf = gpd.read_file(req_shp)  # make geodataframe
        engine = create_engine(conn_str)
        gdf.to_postgis(
            con=engine,
            schema='public',
            name=name,
            if_exists="replace")

        for s in shp:
            os.remove(s)

    except Exception as e:
        for s in shp:
            os.remove(s)
        instance.delete()
        print("There is problem during shp upload: ", e)

class plan(models.Model):
    DZONGKHAGS = (
        (1, 'Bumthang'),
        (2, 'Chhukha'),
        (3, 'Dagana'),
        (4, 'Gasa'),
        (5, 'Haa'),
        (6, 'Lhuentse'),
        (7, 'Mongar'),
        (8, 'Paro'),
        (9, 'Pema Gatshel'),
        (10, 'Punakha'),
        (11, 'Samdrup Jongkhar'),
        (12, 'Samtse'),
        (13, 'Sarpang'),
        (14, 'Thimphu'),
        (15, 'Trashigang'),
        (16, 'Trashi Yangtse'),
        (17, 'Tsirang'),
        (18, 'Trongsa'),
        (19, 'Wangdue Phodrang'),
        (20, 'Zhemgang'),
    )

    PLAN_TYPE =(
        ('National Plan','National Plan'),
        ('Regional Development Plan','Regional Development Plan'),
        ('Local Spatail Plan','Local Spatail Plan'),
        ('Action Area Plan','Action Area Plan'),
    )
    APPROVING =(
        ('PPCM','PPCM'),
        ('NCHS','NCHS'),
        ('NCCHS','NCCHS'),
    )

    name = models.CharField(max_length=100,blank=True)
    table = models.CharField(max_length=100,blank=True)
    image = models.FileField(upload_to='static/data/plan/cover', blank=True)
    dzongkhag = models.BigIntegerField(choices=DZONGKHAGS,blank=True)
    area = models.CharField(max_length=100,blank=True)
    plan_date = models.DateField(default=datetime.date.today,blank=True)
    approved_date = models.DateField(default=datetime.date.today,blank=True)
    approved_by = models.CharField(choices=APPROVING,blank=True,max_length=100)
    period_from = models.DateField(default=datetime.date.today,blank=True)
    period_till = models.DateField(default=datetime.date.today,blank=True)
    description= RichTextField(blank=True)
    dcr = models.FileField(upload_to='static/data/plan/dcr', blank=True)
    report = models.FileField(upload_to='static/data/plan/report', blank=True)
    type = models.CharField(choices=PLAN_TYPE,max_length=800,blank=True)

    def __str__(self):
        return self.name

class data(models.Model):

    plan = models.ForeignKey(plan,on_delete=models.CASCADE,blank=True)
    database = models.CharField(max_length=200,blank=True)
    boundary = models.FileField(upload_to='static/data/plan/boundary/%Y/%m/%d', blank=True)
    precient = models.FileField(upload_to='static/data/plan/precient/%Y/%m/%d', blank=True)
    plot = models.FileField(upload_to='static/data/plan/plot/%Y/%m/%d', blank=True)
    excel = models.FileField(upload_to='static/data/plan/excel', blank=True)
    created_at = models.DateField(default=datetime.date.today, blank=True)

    def __str__(self):
        return self.database
    
    def save(self, *args, **kwargs):
        plan_d = plan.objects.all().filter(id=self.plan.id).last()
        self.database = plan_d.table
        super(data, self).save(*args, **kwargs)

@receiver(post_save,sender=data)

def pusblish_plan_boundary(sender, instance, created, **kwargs):
    file = instance.boundary.path
    file_format = os.path.basename(file).split('.')[-1]
    file_name = os.path.basename(file).split('.')[0]
    file_path = os.path.dirname(file)
    name = instance.database.lower()
    conn_str = 'postgresql://postgres:kali339456@localhost:5432/geo'

    # extract zipfile
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(file_path)

   # Get shapefile
    shp = glob.glob(r'{}/**/*.shp'.format(file_path),recursive=True)

    try:
        req_shp = shp[0]
        gdf = gpd.read_file(req_shp)  # make geodataframe
        engine = create_engine(conn_str)
        gdf.to_postgis(
            con=engine,
            schema='public',
            name= name,
            if_exists="replace")

        for s in shp:
            os.remove(s)

    except Exception as e:
        for s in shp:
            os.remove(s)
        instance.delete()
        print("There is problem during shp upload: ", e)


@receiver(post_save,sender=data)
def pusblish_plan_precient(sender, instance, created, **kwargs):
    file = instance.precient.path
    file_format = os.path.basename(file).split('.')[-1]
    file_name = os.path.basename(file).split('.')[0]
    file_path = os.path.dirname(file)
    name = instance.database.lower() + "_" + "precient"
    conn_str = 'postgresql://postgres:kali339456@localhost:5432/geo'

    # extract zipfile
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(file_path)

   # Get shapefile
    shp = glob.glob(r'{}/**/*.shp'.format(file_path),recursive=True)

    try:
        req_shp = shp[0]
        gdf = gpd.read_file(req_shp)  # make geodataframe
        engine = create_engine(conn_str)
        gdf.to_postgis(
            con=engine,
            schema='public',
            name= name,
            if_exists="replace")

        for s in shp:
            os.remove(s)

    except Exception as e:
        for s in shp:
            os.remove(s)
        instance.delete()
        print("There is problem during shp upload: ", e)


@receiver(post_save,sender=data)
def pusblish_plan_plot(sender, instance, created, **kwargs):
    file = instance.plot.path
    file_format = os.path.basename(file).split('.')[-1]
    file_name = os.path.basename(file).split('.')[0]
    file_path = os.path.dirname(file)
    name = instance.database.lower() + "_" + "plot"
    conn_str = 'postgresql://postgres:kali339456@localhost:5432/geo'

    # extract zipfile
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(file_path)

   # Get shapefile
    shp = glob.glob(r'{}/**/*.shp'.format(file_path),recursive=True)

    try:
        req_shp = shp[0]
        gdf = gpd.read_file(req_shp)  # make geodataframe
        engine = create_engine(conn_str)
        gdf.to_postgis(
            con=engine,
            schema='public',
            name= name,
            if_exists="replace")

        for s in shp:
            os.remove(s)

    except Exception as e:
        for s in shp:
            os.remove(s)
        instance.delete()
        print("There is problem during shp upload: ", e)

