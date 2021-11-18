import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from datetime import datetime

# !!! Requires 'time:timestamp'
# given an event log(sorted by timestamps!!!), add CaseTimeToEnd(T3) attribute to each event and then return the log
# Definition T3: computes the activity time of the trace left from time of an event, undefined is the placeholder, if there were no prior Start of the event
def add_T3(log):

    for trace in log:
        for event in trace:  
                event['CaseTimeToEnd(T3)'] = caseTimeLeft(trace, event)
            
    return log



# returns the activity time of a given Complete event
def caseTimeLeft(trace, event):

    # denotes the duration of activity
    case_dur = 'undefined'

    # get trace end time
    case_end = trace[len(trace) - 1]['time:timestamp']

    # compute case duration
    case_dur = case_end - event['time:timestamp']

    return case_dur


# FOR TESTING PURPOSES ONLY!!!

variant = xes_importer.Variants.ITERPARSE
parameters = {variant.value.Parameters.TIMESTAMP_SORT: True}
log = xes_importer.apply('C:\\Users\\kaili\\Desktop\\running-example.xes', variant=variant, parameters=parameters)


print(log[2])



log = add_T3(log)

print(log[2][2])
print(log[2][6])