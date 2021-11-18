import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from datetime import datetime

# !!! Requires 'time:timestamp'
# given an event log(sorted by timestamps!!!), add WorkloadOfResourceLeft(R1) attribute to each event and then return the log
# Definition R1: computes the number of events left after the event timestamp across the entire log for THE event's resource, undefined is the placeholder
def add_R1(log):

    for trace in log:
        for event in trace:  
                event['WorkloadOfResourceLeft(R1)'] = workloadLeftForResource(log, event)
            
    return log



# returns the activity time of a given Complete event
def workloadLeftForResource(log, event):

    # denotes the number of events after an event
    workload_resource = 0

    # check for ALL events are they after given event AND feature the given event's resource, then increment workload
    for trace in log:
        for ev in trace:
            if  ev['Resource'] == event['Resource'] and ev['time:timestamp'] > event['time:timestamp']:
                workload_resource += 1


    return workload_resource


# FOR TESTING PURPOSES ONLY!!!

variant = xes_importer.Variants.ITERPARSE
parameters = {variant.value.Parameters.TIMESTAMP_SORT: True}
log = xes_importer.apply('C:\\Users\\kaili\\Desktop\\running-example.xes', variant=variant, parameters=parameters)


print(log[2])



log = add_R1(log)

print(log[2][2])
print(log[2][6])