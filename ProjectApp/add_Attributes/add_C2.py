import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer

# Requires Activity
# given an event log(sorted by timestamps!!!), add NextActivity(C2) attribute to each event and then return the log
# Definition C2: says which is the next activity after the event, NoNextAct is the placeholder, if there are no activites executed subsequently
def add_C2(log):

    for trace in log:
        for event in trace:
            event['NextActivity(C2)'] = nextAct(trace, event)

    return log

# returns as string the next set activity for a given trace,event and activity set
def nextAct(trace, event):

    # denotes if we have passed the given activity in the trace
    after = False

    for ev in trace:

        # return events activity, if we are after the given event
        if after:
            return ev['Activity']

        # have we reached the event
        if event == ev:
            after = True

    # returns placeholder if there is no subsequent set activity
    return "NoNextAct"








