import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from datetime import datetime

from ProjectApp import log_utils



# given an event log(sorted by timestamps!!!), add CaseTimeCurrent(T2) attribute to each event and then return the log
# Definition T2: computes the activity time of the trace at time of an event
def add_T2(log):
    '''given an event log(sorted by timestamps!!!), add CaseTimeCurrent(T2) attribute to each event and then return the log
            Definition T2: computes the activity time of the trace at time of an event, undefined is the placeholder,'''
    for trace in log:
        for event in trace:  
                event['CaseTimeCurrent(T2)'] = caseTime(trace, event)
            
    return log



# returns the activity time of a trace at time of event
def caseTime(trace, event):
    '''returns the activity time of a trace at time of event'''

    # denotes the duration of activity
    case_dur = 'undefined'
    # denotes starting time
    case_start = 0

    # get trace start time
    case_start = trace[0][log_utils.timestamp_attr]

    # compute case duration
    case_dur = event[log_utils.timestamp_attr] - case_start

