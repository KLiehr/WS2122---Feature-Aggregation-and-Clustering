import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from ProjectApp import log_utils





def add_C3(log):
    '''given an event log(sorted by timestamps!!!), add PrevActivity(C3) attribute to each event and then return the log
        Definition C3: says which was the previous activity in the trace, NoPrevAct is the placeholder, if there were no prior activities'''
    for trace in log:
        for event in trace:  
            event['PrevActivity(C3)'] = prevAct(trace, event)


    return log


def prevAct(trace, event):
    '''returns as string the next set activity for a given trace,event and activity set'''

    # denotes the previous activity
    prev_Act = 'NoPrevAct'

    for ev in trace:

        # have we reached the event? if so, return prevAct
        if event == ev:
            return prev_Act

        prev_Act = ev[log_utils.activity_attr]

    # Should not be reached
    return "ERROR: Event not in trace"





