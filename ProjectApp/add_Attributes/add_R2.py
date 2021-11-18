import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from datetime import datetime

# !!! Requires 'time:timestamp'
# given an event log(sorted by timestamps!!!), add WorkloadTotalLeft(R2) attribute to each event and then return the log
# Definition R2: computes the number of events left after the event timestamp across the entire log for ALL resources, undefined is the placeholder
def add_R2(log):


    for trace in log:
        for event in trace:  
                event['WorkloadTotalLeft(R2)'] = workloadLeft(log, event)
            
    return log



# returns the activity time of a given Complete event
def workloadLeft(log, event):

    # denotes the number of events after an event
    workload_total = 0

    # check for ALL events are they after given event, then increment workload
    for trace in log:
        for ev in trace:
            if ev['time:timestamp'] > event['time:timestamp']:
                workload_total += 1


    return workload_total


