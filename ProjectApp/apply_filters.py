import pm4py
import pm4py
from pm4py.objects import log
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
import sys
import os
import pandas as pd
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.util import constants

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
  
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
  
# adding the parent directory to 
# the sys.path.
sys.path.append(parent)
  
# now we can import the module in the parent
# directory.
try: 
    import log_utils
except ModuleNotFoundError:
    from . import log_utils



def callAllFilters(log, chosen_filters, extra_input):
    '''For a given log, filters and extra input for certain filters apply them all and return filtered log'''

    # create actual list from attribute string via ,
    filter_list = chosen_filters.split(',')

    # create actual list from extra_input string via ,
    extra_info_list = extra_input.split(',')

    # list of filter abbreviations that require extra_input
    extra_input_needed = ['F6','F7']


    # call each chosen filter's function:
    for abbrv in filter_list:
        
        name_of_method = "apply_" + abbrv
        
        print("Applying filter: " + abbrv)

        # differentiate between those that need extra info
        if abbrv in extra_input_needed:

            # find fitting extra_info for an abbreviation info_element in form: 'F6:Pete'
            for info_element in extra_info_list:
                # split along : for access
                abbr_data = str(info_element).split('!')
                if  abbr_data[0] == abbrv:
                    print("Calling " + abbrv + " with extra data: " + abbr_data[1])
                    log = getattr(sys.modules[__name__], name_of_method)(log, abbr_data[1])
        else:
            log = getattr(sys.modules[__name__], name_of_method)(log)


    return log


def apply_F1(log):
    '''given a event log, apply filter f1: Keep all events, return filtered log'''
    return (log)



def apply_F2(log):
    '''given a event log, apply filter F2: Only keep first event of a case, return filtered log'''
    for i, trace in enumerate(log):
        first_event = trace[0]
        filtered_trace =  pm4py.filter_trace(lambda t: t == first_event, trace)
        log[i] = filtered_trace
    return log



def apply_F3(log):
    '''given a event log, apply filter F3: Only keep last event of a case, return filtered log'''
    for i, trace in enumerate(log):
        last_event = trace[-1]
        filtered_trace =  pm4py.filter_trace(lambda t: t == last_event, trace)
        log[i] = filtered_trace
    return log



def apply_F4(log):
    '''given a event log, apply filter F4: Only keep events marked as 'Complete', return filtered log'''
    if not log_utils.lifecycle_transition_attr == 'NO LIFECYCLE ATTRIBUTE IN LOG':
        for i, trace in enumerate(log):
            filtered_trace =  pm4py.filter_trace(lambda t: t[log_utils.lifecycle_transition_attr] == 'complete' or t[log_utils.lifecycle_transition_attr] == 'Complete', trace)
            log[i] = filtered_trace
    else:
        print('!!!!!F4 not applied due to no designation of lifecycle attribute in log_util.py!!!!!')
    return log

log_utils.lifecycle_transition_attr

def apply_F5(log):
    '''given a event log, apply filter F5: Only keep events marked as 'Start', return filtered log'''
    if not log_utils.lifecycle_transition_attr == 'NO LIFECYCLE ATTRIBUTE IN LOG':    
        for i, trace in enumerate(log):
            filtered_trace =  pm4py.filter_trace(lambda t: t[log_utils.lifecycle_transition_attr] == 'start' or t[log_utils.lifecycle_transition_attr] == 'Start', trace)
            log[i] = filtered_trace
    else:
        print('!!!!!F5 not applied due to no designation of lifecycle attribute in log_util.py!!!!!')
    return log



def apply_F6(log, activity):
    '''given a event log and an activity, apply filter F6: Only keep events with the given activity, return filtered log'''
    for i, trace in enumerate(log):
        filtered_trace =  pm4py.filter_trace(lambda t: t[log_utils.activity_attr] == activity, trace)
        log[i] = filtered_trace
    return log



def apply_F7(log, resource):
    '''given a event log and a resource, apply filter F7: Only keep events with the given resource, return filtered log'''
    for i, trace in enumerate(log):
        filtered_trace =  pm4py.filter_trace(lambda t: t[log_utils.resource_attr] == resource, trace)
        log[i] = filtered_trace
    return log


