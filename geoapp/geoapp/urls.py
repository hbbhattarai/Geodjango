
from django.contrib import admin
from django.urls import path, re_path
from django.http import HttpResponse
from . import views
from app.models import *
from django.conf import settings
import json
import psycopg2
from django.conf.urls.static import static
from django.views.static import serve

def query(table=None):
    return f"""
        SELECT jsonb_build_object(
            'type',     'FeatureCollection',
            'features', jsonb_agg(feature)
        )
        FROM (
            SELECT jsonb_build_object(
                'type',       'Feature',
                'geometry',   ST_AsGeoJSON(geometry)::jsonb,
                'properties', to_jsonb(inputs) - 'geometry'
            ) AS feature
            FROM (
                SELECT 
                    *
                FROM { table }
            ) inputs
        ) features;
    """
def queryById(table=None,dzoId= None):
    return f"""
        SELECT jsonb_build_object(
            'type',     'FeatureCollection',
            'features', jsonb_agg(feature)
        )
        FROM (
            SELECT jsonb_build_object(
                'type',       'Feature',
                'geometry',   ST_AsGeoJSON(geometry)::jsonb,
                'properties', to_jsonb(inputs) - 'geometry'
            ) AS feature
            FROM (
                SELECT 
                    *
                FROM { table }
                WHERE "dzoId" = {dzoId}
            ) inputs
        ) features;
    """



def boundary(request):
    """
    Fetch Plans data by dzongkhag from PostGIS in GeoJSON and return it in the response.
    """

    DB_CONNECT = settings.DATABASES["default"]

    connection = psycopg2.connect(
        database=DB_CONNECT["NAME"],
        user=DB_CONNECT["USER"],
        password=DB_CONNECT["PASSWORD"],
        host=DB_CONNECT["HOST"],
        port=DB_CONNECT["PORT"],
    )

    cursor = connection.cursor()
    planTableName = request.session['planTableName']
    data_query = query(table=planTableName)

    cursor.execute(data_query)

    result = cursor.fetchone()

    response = json.dumps(result[0], indent=2)

    return HttpResponse(response,content_type='json')



def precient(request):
    """
    Fetch Plans data by dzongkhag from PostGIS in GeoJSON and return it in the response.
    """

    DB_CONNECT = settings.DATABASES["default"]

    connection = psycopg2.connect(
        database=DB_CONNECT["NAME"],
        user=DB_CONNECT["USER"],
        password=DB_CONNECT["PASSWORD"],
        host=DB_CONNECT["HOST"],
        port=DB_CONNECT["PORT"],
    )

    cursor = connection.cursor()
    planTableName = request.session['planTableName'] + "_" + "precient"
    data_query = query(table=planTableName)

    cursor.execute(data_query)

    result = cursor.fetchone()

    response = json.dumps(result[0], indent=2)

    return HttpResponse(response,content_type='json')


def plot(request):
    """
    Fetch Plans data by dzongkhag from PostGIS in GeoJSON and return it in the response.
    """

    DB_CONNECT = settings.DATABASES["default"]

    connection = psycopg2.connect(
        database=DB_CONNECT["NAME"],
        user=DB_CONNECT["USER"],
        password=DB_CONNECT["PASSWORD"],
        host=DB_CONNECT["HOST"],
        port=DB_CONNECT["PORT"],
    )

    cursor = connection.cursor()
    planTableName = request.session['planTableName'] + "_" + "plot"
    data_query = query(table=planTableName)

    cursor.execute(data_query)

    result = cursor.fetchone()

    response = json.dumps(result[0], indent=2)

    return HttpResponse(response,content_type='json')


def dzongkhag(request):
    """
    Fetch Dzongkhags data from PostGIS in GeoJSON and return it in the response.
    """

    DB_CONNECT = settings.DATABASES["default"]

    connection = psycopg2.connect(
        database=DB_CONNECT["NAME"],
        user=DB_CONNECT["USER"],
        password=DB_CONNECT["PASSWORD"],
        host=DB_CONNECT["HOST"],
        port=DB_CONNECT["PORT"],
    )

    cursor = connection.cursor()

    data_query = query(table="dzongkhags")

    cursor.execute(data_query)

    result = cursor.fetchone()

    response = json.dumps(result[0], indent=2)

    return HttpResponse(response,content_type='json')

def dzongkhagById(request,dzoId):
    """
    Fetch Dzongkhags data from PostGIS in GeoJSON and return it in the response.
    """

    DB_CONNECT = settings.DATABASES["default"]

    connection = psycopg2.connect(
        database=DB_CONNECT["NAME"],
        user=DB_CONNECT["USER"],
        password=DB_CONNECT["PASSWORD"],
        host=DB_CONNECT["HOST"],
        port=DB_CONNECT["PORT"],
    )

    cursor = connection.cursor()

    data_query = queryById(table="dzongkhags",dzoId=dzoId)

    cursor.execute(data_query)

    result = cursor.fetchone()

    response = json.dumps(result[0], indent=2)

    return HttpResponse(response,content_type='json')



urlpatterns = [
    path('admin', admin.site.urls),
    path('base', views.BASE, name='base'),
    path('', views.INDEX, name='index'),


    # Dzongkhag Data Url
    path('dzongkhags',dzongkhag,name='dzongkhag_data'),

    # Dzongkhag Data Url
    path('dzongkhag/<int:dzoId>',dzongkhagById,name='dzongkhagId_data'),

    # Plan Boundary Data url
    path('boundary', boundary, name='boundary_data'),

    # Precient Boundary Data url
    path('precient',precient,name='precient_data'),

    # Plot Boundary Data url
    path('plot',plot,name='plot_data'),

    # Plans Url
    path('plans/<int:dzoId>', views.plansByDzongkhag, name='plans'),
    path('plan/history/<int:id>', views.plansById, name='plan_history'),
     path('plan/<int:id>', views.planById, name='plan'),
  

    # Plans Download Url
    re_path(r'(?P<path>.*)$',serve,{'document_root': settings.STATIC_ROOT}),
]


if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root= settings.STATIC_ROOT)