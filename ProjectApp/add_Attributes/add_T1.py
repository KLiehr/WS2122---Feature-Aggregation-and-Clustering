import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from datetime import datetime

from ProjectApp import log_utils





# given an event log(sorted by timestamps!!!), add ActivityTime(T1) attribute, return new log
# Definition T1: computes the activity time of an event through lifecycle:transition attribute, if not there or no Start event, compute timedifference between previous event
def add_T1(log):
    '''given an event log(sorted by timestamps!!!), add ActivityTime(T1) attribute, return new log
            Definition T1: computes the activity time of an event through lifecycle:transition attribute, 
                if not there or no Start event, compute timedifference between previous event'''

    # if a lifecycle transition attribute has not been designated, just substract time of current minus previous
    if not log_utils.lifecycle_transition_attr == 'NO LIFECYCLE ATTRIBUTE IN LOG':
        for trace in log:
            pre_time = 0
            for event in trace:
                if pre_time != 0:
                    event['ActivityTime(T1)'] = event[log_utils.timestamp_attr] - pre_time
                # if start event of trace set duration to 0
                else: 
                    event['ActivityTime(T1)'] = 0
                pre_time = event[log_utils.timestamp_attr]



    # if there is a lifecycle transition attribute
    else: 
        for trace in log:
            for event in trace:  
                # check if transition is there(should be a given, since it has been designated) and if so whether its complete
                if log_utils.lifecycle_transition_attr in event:
                    if event[log_utils.lifecycle_transition_attr] == 'Complete' or event[log_utils.lifecycle_transition_attr] == 'complete':
                        event['ActivityTime(T1)'] = actTime(trace, event)
                # should never be reached, as a lifecycle attribute has been designated
                else:
                    event['ActivityTime(T1)'] = 'No lifecycle attribute DESPITE designation'
                    print('!!!!!During adding of T1 there was an event without lifecycle transition despite its designation!!!!!')
                    print(event)
        
    return log












# returns the activity time of a given Complete event
def actTime(trace, event):
    '''returns the activity time of a given Complete event'''

    # denotes the duration of activity
    act_dur = 'undefined'
    # denotes starting time
    act_start = 0
    # denotes if we are before the event
    before = True


    for ev in trace:
        # check for same activity as event but with transition = Start
        if before:
            if ev[log_utils.activity_attr] == event[log_utils.activity_attr]:
                if ev[log_utils.lifecycle_transition_attr] == 'Start' or ev[log_utils.lifecycle_transition_attr] == 'start':
                    act_start = ev[log_utils.timestamp_attr]

        # update before
        if ev == event:
            before = False

    # compute activity duration and return it if start event has been found
    if act_start != 0:
        act_dur = event[log_utils.timestamp_attr] - act_start
        return act_dur
    # if no corresponding start event was found, use previous event timestamp to subtract with
    else: 
        previous_time = 0
        before = True

        for ev in trace:
            # update before
            if ev == event:
                before = False
            # update previous time
            if before:
                previous_time = ev[log_utils.timestamp_attr]

        act_dur = event[log_utils.timestamp_attr] - previous_time
        if previous_time != 0:
            return act_dur
        # if event without corresponding start event was the trace's first event, return 0
        else:
            return 0











