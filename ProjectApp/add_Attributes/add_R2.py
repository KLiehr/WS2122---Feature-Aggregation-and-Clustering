import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from datetime import datetime

from ProjectApp import log_utils

# given an event log(sorted by timestamps!!!), add WorkloadTotalLeft(R2) attribute to each event and then return the log
# Definition R2: computes the number of events left after the event timestamp across the entire log for ALL resources, undefined is the placeholder
def add_R2(log):
    '''given an event log(sorted by timestamps!!!), add WorkloadTotalLeft(R2) attribute to each event and then return the log
            Definition R2: computes the number of events left after the event timestamp across the entire log for ALL resources, undefined is the placeholder'''

    for trace in log:
        for event in trace:  
                event['WorkloadTotalLeft(R2)'] = workloadLeft(log, event)
            
    return log


# TODO lifecycle compatability
# returns the number of events across the log after a given one
def workloadLeft(log, event):
    '''returns the number of events across the log after a given one'''

    # denotes the number of events after an event
    workload_total = 0

    # check for ALL events are they after given event, then increment workload
    for trace in log:
        for ev in trace:
            if ev[log_utils.timestamp_attr] > event[log_utils.timestamp_attr]:
                workload_total += 1


    return workload_total


