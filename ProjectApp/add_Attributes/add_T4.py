import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from datetime import datetime

# !!! Requires 'time:timestamp'
# given an event log(sorted by timestamps!!!), add CaseTimeTotal(T4) attribute to each event and then return the log
# Definition T4: computes the total case time, undefined is the placeholder
def add_T4(log):

    for trace in log:

        # get trace start time
        case_start = trace[0]['time:timestamp']
        # get trace end time
        case_end = trace[len(trace) - 1]['time:timestamp']

        # set all event attributes
        for event in trace:
            event['CaseTimeTotal(T4)'] = case_end - case_start
            
    return log





# FOR TESTING PURPOSES ONLY!!!

variant = xes_importer.Variants.ITERPARSE
parameters = {variant.value.Parameters.TIMESTAMP_SORT: True}
log = xes_importer.apply('C:\\Users\\kaili\\Desktop\\running-example.xes', variant=variant, parameters=parameters)


print(log[2])



log = add_T4(log)

print(log[2][2])
print(log[2][6])