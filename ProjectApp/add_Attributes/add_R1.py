import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from datetime import datetime
from ProjectApp import log_utils


# given an event log(sorted by timestamps!!!), add WorkloadOfResourceLeft(R1) attribute to each event and then return the log
# Definition R1: computes the number of events left after the event timestamp across the entire log for THE event's resource, undefined is the placeholder
def add_R1(log):
    '''given an event log(sorted by timestamps!!!), add WorkloadOfResourceLeft(R1) attribute to each event and then return the log
            Definition R1: computes the number of events left after the event timestamp across the entire log for THE event's resource, undefined is the placeholder'''
    for trace in log:
        for event in trace:  
                event['WorkloadOfResourceLeft(R1)'] = workloadLeftForResource(log, event)
            
    return log


# TODO add lifecycle compatibility
# returns the number of events of the same resource after a given one for all traces 
def workloadLeftForResource(log, event):
    '''returns the number of events of the same resource after a given one for all traces '''

    # denotes the number of events after an event
    workload_resource = 0

    # check for ALL events are they after given event AND feature the given event's resource, then increment workload
    for trace in log:
        for ev in trace:
            if  ev[log_utils.resource_attr] == event[log_utils.resource_attr] and ev[log_utils.timestamp_attr] > event[log_utils.timestamp_attr]:
                workload_resource += 1


    return workload_resource


