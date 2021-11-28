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
from . import apply_filters

import pandas as pd
import pm4py
import json






# Create your views here.

def home(request):
    return render(request, 'ProjectApp/home.html')

def userguide(request):
    try:
        return FileResponse(open('Requirements_Specification- Feature Aggregation in Process Mining.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()


def importCSVXES(request):
    return render(request, 'ProjectApp/Import.html')

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


def attributes(request):
    return render(request, 'ProjectApp/Attributes.html')

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

        # print event attributes !!Just of first event!!
        print('Event attributes of log:')
        print(log_utils.get_log_attributes(log))

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
    return HttpResponse('No File')


def filters(request):
    return render(request, 'ProjectApp/Filters.html')

# gets called after Filter event log button is clicked, gets a request with a string for chosen filters and extra Input
@csrf_exempt
def filtereventlog(request):
    if request.method == 'POST':
        filters = str(request.POST.get('listFilters'))
        extra_input = str(request.POST.get('ExtraInput'))
        print('Filters: ' + filters)
        print('ExtraInput for filters: ' + extra_input)

        # get log
        log = log_utils.get_log()

        # call function to apply all filters
        print('calling apply_filters')
        log = apply_filters.callAllFilters(log, filters, extra_input)

        # update log
        log_utils.update_log(log)

    return JsonResponse({'post':'false'})

#we can delete this one and use the download function if we are just updating the same file
def downloadFilters(request):
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
    return HttpResponse('No File')


def useCase(request):
    #create array with attribute names for CSV file
    if os.path.exists('media\eventlog\our_file.csv'):
        ourFile=pd.read_csv('media\eventlog\our_file.csv', header=0)
        arrayAttrCSV=list(ourFile.columns)
        print(arrayAttrCSV)
        #add attribute names to UseCase.html
        context={}
        context['attributesNames']=json.dumps(arrayAttrCSV)
        return render(request, 'ProjectApp/UseCase.html', context)
    
    #create array with attribute names for XES file
    if os.path.exists('media\eventlog\our_file.xes'):
        ourFile=pm4py.read_xes('media\eventlog\our_file.xes')
        ourFile= pm4py.convert_to_dataframe(ourFile)
        arrayAttrCSV=list(ourFile.columns)
        print(arrayAttrCSV)
        #add attribute names to UseCase.html
        context={}
        context['attributesNames']=json.dumps(arrayAttrCSV)
        return render(request, 'ProjectApp/UseCase.html', context)

    return render(request, 'ProjectApp/UseCase.html')

@csrf_exempt
def decisionTree(request):
    if request.method == 'POST':
        dependent = str(request.POST.get('dependent'))
        independent = str(request.POST.get('independent'))
        print(dependent)
        print(independent)

    return JsonResponse({'post':'false'})
    
    
    


