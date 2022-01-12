import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from datetime import datetime


from ProjectApp import log_utils



# given an event log(sorted by timestamps!!!), add CaseTimeTotal(T4) attribute to each event and then return the log
# Definition T4: computes the total case time
def add_T4(log):
    '''given an event log(sorted by timestamps!!!), add CaseTimeTotal(T4) attribute to each event and then return the log
        Definition T4: computes the total case time(if start and end time given, from start first event to complete last)'''

    for trace in log:
        # if either start or end time is missing, use timestamp of first and last event of a trace
        if log_utils.start_time_attr == 'NO START TIME ATTRIBUTE IN LOG' or log_utils.end_time_attr == 'NO END TIME ATTRIBUTE IN LOG':
            # get trace start time
            case_start = trace[0][log_utils.timestamp_attr]
            # get trace end time
            case_end = trace[len(trace) - 1][log_utils.timestamp_attr]

            # set all event attributes
            for event in trace:
                event['CaseTimeTotal(T4)'] = case_end - case_start
        else:
            # print('Use start and end times for T4')
            # get trace start time
            case_start = trace[0][log_utils.start_time_attr]
            # get trace end time
            case_end = trace[len(trace) - 1][log_utils.end_time_attr]

            # set all event attributes
            for event in trace:
                event['CaseTimeTotal(T4)'] = case_end - case_start
            
    return log





