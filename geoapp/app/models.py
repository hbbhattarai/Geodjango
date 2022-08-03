from django.db import models
import datetime

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
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

    name = models.CharField(max_length=100)
    dzongkhag = models.BigIntegerField(choices=DZONGKHAGS)
    boundary = models.FileField(upload_to='static/data/plan/boundary/%Y/%m/%d', blank=True)
    precient = models.FileField(upload_to='static/data/plan/precient/%Y/%m/%d', blank=True)
    plot = models.FileField(upload_to='static/data/plan/plot/%Y/%m/%d', blank=True)
    created_at = models.DateField(default=datetime.date.today, blank=True)

    def __str__(self):
        return self.name

@receiver(post_save,sender=plan)

def pusblish_plan_boundary(sender, instance, created, **kwargs):
    file = instance.boundary.path
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
            name= name,
            if_exists="replace")

        for s in shp:
            os.remove(s)

    except Exception as e:
        for s in shp:
            os.remove(s)
        instance.delete()
        print("There is problem during shp upload: ", e)


@receiver(post_save,sender=plan)
def pusblish_plan_precient(sender, instance, created, **kwargs):
    file = instance.precient.path
    file_format = os.path.basename(file).split('.')[-1]
    file_name = os.path.basename(file).split('.')[0]
    file_path = os.path.dirname(file)
    name = instance.name.lower() + "_" + "precient"
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


@receiver(post_save,sender=plan)
def pusblish_plan_plot(sender, instance, created, **kwargs):
    file = instance.plot.path
    file_format = os.path.basename(file).split('.')[-1]
    file_name = os.path.basename(file).split('.')[0]
    file_path = os.path.dirname(file)
    name = instance.name.lower() + "_" + "plot"
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

