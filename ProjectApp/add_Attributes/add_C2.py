import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer


# given an event log(sorted by timestamps!!!) and a set of activities, add NextActivity(C2) attribute to each event and then return the log
# Definition C2: for a given activity set, says which is the next activity of the set after the event, NoSetActNext is the placeholder, if there are no set activites executed subsequently
def add_C2(log, act_set):

    for trace in log:
        for event in trace:
            if not act_set:
                event['NextActivity(C2)'] = "NoSetActNext"
            else:
                event['NextActivity(C2)'] = nextSetAct(trace, event, act_set)



    return log

# returns as string the next set activity for a given trace,event and activity set
def nextSetAct(trace, event, act_set):

    # denotes if we have passed the given activity in the trace
    after = False

    for ev in trace:

        # check if ev's activity is in the set, if we are after the given event
        if after:
            if ev['Activity'] in act_set:
                return ev['Activity']

        # have we reached the event
        if event == ev:
            after = True

    # returns placeholder if there is no subsequent set activity
    return "NoSetActNext"








# FOR TESTING PURPOSES ONLY!!!

variant = xes_importer.Variants.ITERPARSE
parameters = {variant.value.Parameters.TIMESTAMP_SORT: True}
log = xes_importer.apply('C:\\Users\\kaili\\Desktop\\running-example.xes', variant=variant, parameters=parameters)


print(log[2])

ex_set_for_C2 = {'check ticket', 'pay compensation'}

log = add_C2(log, ex_set_for_C2)

print(log[2][2])
print(log[2][6])
