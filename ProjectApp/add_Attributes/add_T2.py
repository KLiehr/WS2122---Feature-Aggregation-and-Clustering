import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from datetime import datetime

# !!! Requires 'time:timestamp'
# given an event log(sorted by timestamps!!!), add CaseTimeCurrent(T2) attribute to each event and then return the log
# Definition T2: computes the activity time of the trace at time of an event, undefined is the placeholder, if there were no prior Start of the event
def add_T2(log):

    for trace in log:
        for event in trace:  
                event['CaseTimeCurrent(T2)'] = caseTime(trace, event)
            
    return log



# returns the activity time of a given Complete event
def caseTime(trace, event):

    # denotes the duration of activity
    case_dur = 'undefined'
    # denotes starting time
    case_start = 0

    # get trace start time
    case_start = trace[0]['time:timestamp']

    # compute case duration
    case_dur = event['time:timestamp'] - case_start

    return case_dur


# FOR TESTING PURPOSES ONLY!!!

variant = xes_importer.Variants.ITERPARSE
parameters = {variant.value.Parameters.TIMESTAMP_SORT: True}
log = xes_importer.apply('C:\\Users\\kaili\\Desktop\\running-example.xes', variant=variant, parameters=parameters)


print(log[2])



log = add_T2(log)

print(log[2][2])
print(log[2][6])