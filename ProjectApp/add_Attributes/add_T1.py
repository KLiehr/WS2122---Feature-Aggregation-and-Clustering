import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from datetime import datetime

# TODO Maybe implement alternative definition without start and Complete transition
# !!! Requires Complete and Start event values under lifecycle:transition AND No simultaneous same activities in same trace AND 'time:timestamp'
# given an event log(sorted by timestamps!!!), add ActivityTime(T1) attribute to each Complete event and then return the log
# Definition T1: computes the activity time of an event, undefined is the placeholder, if there were no prior Start of the attribute
def add_T1(log):

    for trace in log:
        for event in trace:  
            # check if transition is there and if so whether its complete
            if 'lifecycle:transition' in event:
                if event['lifecycle:transition'] == 'Complete':
                    event['ActivityTime(T1)'] = actTime(trace, event)
            else:
                event['ActivityTime(T1)'] = 'NoTransitionAttr'
            


    return log



# returns the activity time of a given Complete event
def actTime(trace, event):

    # denotes the duration of activity
    act_dur = 'undefined'
    # denotes starting time
    act_start = 0
    # denotes if we are before the event
    before = True


    for ev in trace:
        # check for same activity as event but with transition = Start
        if before:
            if ev['Activity'] == event['Activity'] and ev['lifecycle:transition'] == 'Start':
                act_start = ev['time:timestamp']

        # update before
        if ev == event:
            before = False

    # compute activity duration and return it if start event has been found
    if act_start != 0:
        act_dur = event['time:timestamp'] - act_start
        return act_dur

    return 'undefined'


# TODO HAS NOT BEEN TESTED DUE TO LACK OF LOG WITH TRANSITION
