import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from datetime import datetime

from ProjectApp import log_utils



# given an event log(sorted by timestamps!!!), add CaseTimeToEnd(T3) attribute to each event and then return the log
# Definition T3: computes the activity time of the trace left from time of an event
def add_T3(log):
    '''given an event log(sorted by timestamps!!!), add CaseTimeToEnd(T3) attribute to each event and then return the log
            Definition T3: computes the activity time of the trace left from time of an event(end time if there)'''

    for trace in log:
        for event in trace:  
            if log_utils.end_time_attr == 'NO END TIME ATTRIBUTE IN LOG':
                event['CaseTimeToEnd(T3)'] = caseTimeLeft(trace, event)
            else:
                event['CaseTimeToEnd(T3)'] = caseTimeFromEventstart(trace, event[log_utils.end_time_attr])

    return log

def caseTimeFromEventstart(trace, endtime):
    '''returns the trace time left after given end time'''

    # denotes the duration of activity
    case_dur = 0

    # get trace end time
    case_end = trace[len(trace) - 1][log_utils.end_time_attr]

    # compute case duration
    case_dur = case_end - endtime

    return case_dur

# returns the activity time left at event time
def caseTimeLeft(trace, event):
    '''returns the trace time left at event time'''

    # denotes the duration of activity
    case_dur = 0

    # get trace end time
    case_end = trace[len(trace) - 1][log_utils.timestamp_attr]

    # compute case duration
    case_dur = case_end - event[log_utils.timestamp_attr]

    return case_dur


