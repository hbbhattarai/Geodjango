from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

from app.models import *


def BASE(request):
    return render(request, 'components/base.html')

def INDEX(request):
    return render(request,'main/index.html')

def plansByDzongkhag(request, dzoId):
    plans = plan.objects.all().filter(dzongkhag = dzoId)
    lastest_plan = plan.objects.filter(dzongkhag = dzoId).last()
    request.session['planTableName'] = lastest_plan.name
    context = {
        'plans': plans
    }

    return   render(request,'main/plan_list.html', context)

def planById(request, id):
    request.session['planId'] = id
    return render(request,'main/single_plan.html')



def downloadData(request, path):
    download_path = os.path.join(settings.STATIC_ROOT,path)
    if os.path.exists(download_path):
        with open(download_path, 'rb') as fh:
            response = HttpResponse(fh.read(),content_type="application/file")
            print(response)
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(download_path)
            return response
    response = HttpResponse(path, content_type='mime_type')
    return response

