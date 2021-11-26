from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Doc
from django.http import FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import shutil
import os
from . import log_utils

from .add_Attributes import add_Attr
from .Apply_Filter import apply_all_filters

import sys




# Create your views here.

def home(request):
    return render(request, 'ProjectApp/home.html')


def importCSVXES(request):
    return render(request, 'ProjectApp/Import.html')


def attributes(request):
    return render(request, 'ProjectApp/Attributes.html')


def userguide(request):
    try:
        return FileResponse(open('Requirements_Specification- Feature Aggregation in Process Mining.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()

def file_upload_view(request):
    if request.method == 'POST':
        if os.path.exists("media\\eventlog"):
            print("removing old file")
            shutil.rmtree("media\\eventlog")

        my_file = request.FILES.get('file')
        my_file.name='our_file.'+ my_file.name[-3:]
        Doc.objects.create(upload=my_file)
        return HttpResponse('')
    return JsonResponse({'post':'false'})


# gets called after update event log button is clicked, gets a request with a string for derivable attributes and extraInfos
@csrf_exempt
def updateeventlog(request):
    if request.method == 'POST':
        AttributesToDerive = str(request.POST.get('ListAtr'))
        ExtraAttributes = str(request.POST.get('ExtraAtr'))
        UserAttrNames = str(request.POST.get('AttrNames'))
        print('Derive the following attributes: ' + AttributesToDerive)
        print('Extra Info: ' + ExtraAttributes)
        print('Relevant attribute names: ' + UserAttrNames)
        
        # get log
        log = log_utils.get_log()

        # call function to add all atributes 
        print('calling add_Attributes')
        log = add_Attr.callAllAttr(log, AttributesToDerive, ExtraAttributes)

        # update log
        log_utils.update_log(log)

    return JsonResponse({'post':'false'})

def download(request):
    if os.path.exists('media\eventlog\our_file.csv'):
        file = open('media\eventlog\our_file.csv', 'rb') #Open the specified file
        response = HttpResponse(file)   #Give file handle to HttpResponse object
        response['Content-Type'] = 'application/octet-stream' #Set the header to tell the browser that this is a file
        response['Content-Disposition'] = 'attachment;filename="our_file.csv"' #This is a simple description of the file. Note that the writing is the fixed one
        return response
    if os.path.exists('media\eventlog\our_file.xes'):
        file = open('media\eventlog\our_file.xes', 'rb') #Open the specified file 
        response = HttpResponse(file)   #Give file handle to HttpResponse object
        response['Content-Type'] = 'application/octet-stream' #Set the header to tell the browser that this is a file
        response['Content-Disposition'] = 'attachment;filename="our_file.xes"' #This is a simple description of the file. Note that the writing is the fixed one
        return response
    return Http404

