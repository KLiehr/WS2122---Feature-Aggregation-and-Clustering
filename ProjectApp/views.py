from math import log10
import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
from re import sub
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Doc
from django.http import FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import shutil
import os
from . import log_utils

from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter, variants
from pm4py.util import constants

from .add_Attributes import add_Attr
from . import apply_filters
from . import use_case_analysis
from . import cluster_log

import sys

import pandas as pd
import pm4py
import json

from os import listdir
from os.path import isfile, join
from wsgiref.util import FileWrapper
from os import walk

# Create your views here.

def home(request):
    return render(request, 'ProjectApp/home.html')

def userguide(request):
    try:
        return FileResponse(open('Requirements_Specification- Feature Aggregation in Process Mining.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()


def importCSVXES(request):
    '''Gets files names and opens Import page'''
    
    #when clicking download button downloads the choosen file
    if "downloadButton" in request.POST:
        if "log_list" in request.POST:
            filename = request.POST["log_list"]
            file_dir = os.path.join("media\\eventlog", filename)
            try:
                wrapper = FileWrapper(open(file_dir, 'rb'))
                response = HttpResponse(wrapper, content_type='application/force-download')
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_dir)
                return response
            except Exception as e:
                return None

    # set new log as current one
    elif "setButton" in request.POST:
        if "log_list" in request.POST and (request.POST["log_list"][-3:]=='xes' or request.POST["log_list"][-3:]=='csv'):
            filename = request.POST["log_list"]
            # SetEventLog= filename
            log_utils.cur_log = filename

            # call to set the attributes: TODO maybe save attributes once new log is chosen?
            print('Event Log In Use:', log_utils.cur_log)

            return attrType(request)

        else:
            print('Tried to set a non log object as log, request rejected!!!')

    # delete a log
    elif "deleteButton" in request.POST:
        if "log_list" in request.POST:
            filename = request.POST["log_list"]
            # reset cur_log var if its value gets deleted
            if filename == log_utils.cur_log:
                log_utils.cur_log = ''
            file_dir = os.path.join("media\\eventlog", filename)

            os.remove(file_dir)
    
    #saves the file imported by the user in the eventlog folder
    elif "uploadButton" in request.POST:
        print('olé')
        try:
            if request.FILES['file']:
                print('buba')
                my_file = request.FILES['file']
                Doc.objects.create(upload=my_file)
        except Exception as e:
            None

    #gets files names
    arrayFiles = []
    if os.path.exists("media\\eventlog"):
        arrayFiles = [f for f in listdir("media\\eventlog") if isfile(join("media\\eventlog", f))]
    print(arrayFiles)
    context={}
    context['fileNames']=arrayFiles

    return render(request, 'ProjectApp/Import.html', context)

def attrType(request):
    '''Gets called when clicking Upload EventLog on Import page
    Opens the attribute type page and gets the attributes in the file'''
    arrayAttr = log_utils.get_log_attributes()
    print(arrayAttr)
    #add attribute names to UseCase.html
    context={}
    context['attributesNames']=json.dumps(arrayAttr)
    return render(request, 'ProjectApp/AttrType.html', context)

@csrf_exempt
def saveAttrNames(request):
    '''Gets called when clicking Save on AttrType page'''

    if request.method == 'POST':
        log_utils.case_id_attr = str(request.POST.get('caseID'))
        log_utils.activity_attr = str(request.POST.get('activity'))
        log_utils.resource_attr = str(request.POST.get('resource'))
        log_utils.timestamp_attr = str(request.POST.get('timestamp'))
        log_utils.lifecycle_transition_attr = str(request.POST.get('lifecycle'))

        print('CaseID Attribute:' + log_utils.case_id_attr)
        print('Activity Attributes:' + log_utils.activity_attr)
        print('Resource Attributes:' + log_utils.resource_attr)
        print('Timestamp Attributes:' + log_utils.timestamp_attr)
        print('Lifecycle Attributes:' + log_utils.lifecycle_transition_attr)

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
        print(log_utils.get_log_attributes())

        # call function to add all atributes 
        print('calling add_Attributes')
        log = add_Attr.callAllAttr(log, AttributesToDerive, ExtraAttributes)

        # update log
        log_utils.create_log_without_time(log, 'Added ' + AttributesToDerive + ' to ')

        # with timestamps as names, OLD VERSION
        # log_utils.create_log(log, 'augmented')

    return JsonResponse({'post':'false'})


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

        log_utils.create_log_without_time(log, 'Applied ' + filters + ' to ')


        # update log OLD VERSION WITH TIMESTAMPS
        # log_utils.create_log(log, 'filtered')

        # print(log_utils.get_log_attributes(log))

        # TODO: DELETE TEST OF USE CASE ANALYSIS
        # log = use_case_analysis.analyze_log(log, 'Resource', ['Activity','case:concept:name'])

    return JsonResponse({'post':'false'})


def useCase(request):
    '''Gets called upon visiting UseCase, returns the attributes of the log per json'''
    
    all_log_attr = log_utils.get_log_attributes()

    #add attribute names to UseCase.html
    context={}
    context['attributesNames']=json.dumps(all_log_attr)
    return render(request, 'ProjectApp/UseCase.html', context)




UseCaseName=''
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
        log_utils.last_pred = use_case_analysis.analyze_log(log, dependent_attr, independent_attr.split(','))

        global UseCaseName
        # move decision tree image to eventlog and rename it
        UseCaseName=log_utils.cur_log +'_'+ dependent_attr +'_'+ independent_attr[0:3]
        for i in range(len(independent_attr)):
            if independent_attr[i]==',':
                UseCaseName = UseCaseName + '_' + independent_attr[i+1:i+4]

        if os.path.exists("media\\eventlog\\decTree_"+UseCaseName+'.png'):
            os.remove("media\\eventlog\\decTree_"+UseCaseName+'.png')
        shutil.copy("media\\images\\decTree.png","media\\eventlog\\decTree_"+UseCaseName+'.png')
        
    else:
        print('Called tree without variables')

    # update log(NOT NECESSARY; LOG UNCHANGED)
    # log_utils.update_log(log)
    
    return render(request, 'ProjectApp/DecisionTree.html')




def clustering(request):
    '''Called upon clicking on clustering button, sets last_sublogs variable, which is a list of'''

    #clustering
    log_utils.last_sublogs = cluster_log.split_log(log_utils.get_log(), log_utils.last_pred)

    # creating/clearing folder for sublog xes files
    try:
        os.mkdir(log_utils.get_sublog_xes_path())
    except FileExistsError:
        shutil.rmtree(log_utils.get_sublog_xes_path())
        os.makedirs(log_utils.get_sublog_xes_path())
    
    # saving the xes files
    sublog_nr = 0
    for sublog in log_utils.last_sublogs:
        xes_exporter.apply(sublog, os.path.join(log_utils.get_sublog_xes_path(), 'sublog_nr' + str(sublog_nr) + '.xes'))
        sublog_nr += 1

    global UseCaseName
    # Delete previous clusters.zip if it is the same
    if os.path.exists("media\\eventlog\\clusters_"+UseCaseName+'.zip'):
            os.remove("media\\eventlog\\clusters_"+UseCaseName+'.zip')
    
    #creates new clusters xes zip in eventlog folder
    shutil.make_archive('media\\eventlog\\clusters_'+UseCaseName,'zip','media\\images\\sublog xes files')

    return render(request, 'ProjectApp/Clustering.html')





def processModel(request):
    '''Gets called by Process Model button and creates pictures of process model for sublogs'''

    #Deletes previous sublog images folder
    if os.path.exists(log_utils.get_sublog_image_path()):
        shutil.rmtree(log_utils.get_sublog_image_path())

    #Creates new sublog images folder
    os.makedirs(os.path.join(log_utils.get_image_path(), 'sublog images'))

    #process model
    tree_visual = False
    sublog_nr = 0
    for sublog in log_utils.last_sublogs:
        if tree_visual:
            tree_of_sublog = cluster_log.get_process_tree(sublog)
            cluster_log.visualize_process_tree(tree_of_sublog)
        else:
            sublog_nr += 1
            net, initial_marking, final_marking = cluster_log.get_petri_net(sublog)
            cluster_log.visualize_petri_net(net, initial_marking, final_marking, sublog_nr)
            print('Create sublog number: ')
            print(sublog_nr)

    #gets files names from sublog images
    arrayFiles = []
    if os.path.exists("media\\images\\sublog images"):
        arrayFiles = [f for f in listdir("media\\images\\sublog images") if isfile(join("media\\images\\sublog images", f))]
    print(arrayFiles)
    context={}
    context['fileNames']=json.dumps(arrayFiles)

    global UseCaseName
    # Delete previous clusters.zip if it is the same
    if os.path.exists("media\\eventlog\\processModels_"+UseCaseName+'.zip'):
            os.remove("media\\eventlog\\processModels_"+UseCaseName+'.zip')
    
    #creates new clusters xes zip in eventlog folder
    shutil.make_archive('media\\eventlog\\processModels_'+UseCaseName,'zip','media\\images\\sublog images')

    return render(request, 'ProjectApp/ProcessModel.html', context)
