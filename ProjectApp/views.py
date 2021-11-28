from math import log10
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
from . import use_case_analysis

import sys

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

def attrType(request):
    return render(request, 'ProjectApp/AttrType.html')


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

        # print(log_utils.get_log_attributes(log))

        # TODO: DELETE TEST OF USE CASE ANALYSIS
        # log = use_case_analysis.analyze_log(log, 'Resource', ['Activity','case:concept:name'])

    return JsonResponse({'post':'false'})

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
    '''Gets called upon visiting UseCase, returns the attributes of the log per json'''
    

    all_log_attr = log_utils.get_log_attributes()

    #add attribute names to UseCase.html
    context={}
    context['attributesNames']=json.dumps(all_log_attr)
    return render(request, 'ProjectApp/UseCase.html', context)


@csrf_exempt
def decisionTree(request):
    '''Gets called when clicking Decision Tree on UseCase page'''

    if request.method == 'POST':
        dependent_attr = str(request.POST.get('dependent'))
        independent_attr = str(request.POST.get('independent'))
        print('Dependent Attribute:' + dependent_attr)
        print('Independent Attributes:' + independent_attr)

    # get log
    log = log_utils.get_log()

    # call function to apply all filters
    print('Creating a Decision/Regression tree!')
    log = use_case_analysis.analyze_log(log, dependent_attr, independent_attr.split(','))

    # update log(NOT NECESSARY; LOG UNCHANGED)
    # log_utils.update_log(log)

    return JsonResponse({'post':'false'})