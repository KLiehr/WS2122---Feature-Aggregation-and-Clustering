import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from datetime import datetime


from ProjectApp import log_utils



# given an event log(sorted by timestamps!!!), add CaseTimeTotal(T4) attribute to each event and then return the log
# Definition T4: computes the total case time
def add_T4(log):
    '''given an event log(sorted by timestamps!!!), add CaseTimeTotal(T4) attribute to each event and then return the log
        Definition T4: computes the total case time'''

    for trace in log:

        # get trace start time
        case_start = trace[0][log_utils.timestamp_attr]
        # get trace end time
        case_end = trace[len(trace) - 1][log_utils.timestamp_attr]

        # set all event attributes
        for event in trace:
            event['CaseTimeTotal(T4)'] = case_end - case_start
            
    return log





