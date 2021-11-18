import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer


# given an event log(sorted by timestamps!!!), add attribute ActivityCounter(C1) and then return it
# Definition: C1 gives the number of time an event activity has occured prior to the event in the trace 
def add_C1(log):

    for trace in log:
        for event in trace:
            event['ActivityCounter(C1)'] = count_occ(trace, event)

    return log


# counts how often the activity of an event occured prior in the trace
def count_occ(trace, event):

    counter = 0
    before = True

    for ev in trace:


        # checks if we have still not passed the given event
        if ev == event:
            before = False
        
        # if we are still in the prefix of the trace, check if the current event activity equals the given event's
        # if so increment the variable counter
        if before:
            if ev['Activity'] == event['Activity']:
                print(trace.attributes)
                counter += 1
        
    return counter



# FOR TESTING PURPOSES ONLY!!!

variant = xes_importer.Variants.ITERPARSE
parameters = {variant.value.Parameters.TIMESTAMP_SORT: True}
log = xes_importer.apply('C:\\Users\\kaili\\Desktop\\running-example.xes', variant=variant, parameters=parameters)


print(log[2])

log = add_C1(log)

print(log[2][2])
print(log[2][6])

