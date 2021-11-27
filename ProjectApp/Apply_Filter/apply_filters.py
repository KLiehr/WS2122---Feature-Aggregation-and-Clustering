import pm4py

#REQUIRES event attribute named 'lifecycle:transistion' for apply_F4 and apply_F5
#REQUIRES event attribute named 'Activity' for apply_F6
#REQUIRES event attribute named 'Resource' for apply_F7



#given a event log, apply filter f1: Keep all events, return filtered log
def apply_F1(log):

    return (log)


#given a event log, apply filter F2: Only keep first event of a case, return filtered log
def apply_F2(log):

    for i, trace in enumerate(log):
        first_event = trace[0]
        filtered_trace =  pm4py.filter_trace(lambda t: t == first_event, trace)
        log[i] = filtered_trace
    return log


#given a event log, apply filter F3: Only keep last event of a case, return filtered log
def apply_F3(log):

    for i, trace in enumerate(log):
        last_event = trace[-1]
        filtered_trace =  pm4py.filter_trace(lambda t: t == last_event, trace)
        log[i] = filtered_trace
    return log


#given a event log, apply filter F4: Only keep events marked as 'Complete', return filtered log
def apply_F4(log):
    
    for i, trace in enumerate(log):
        filtered_trace =  pm4py.filter_trace(lambda t: t['lifecycle:transition'] == 'complete' or t['lifecycle:transition'] == 'Complete', trace)
        log[i] = filtered_trace
    return log


#given a event log, apply filter F5: Only keep events marked as 'Start', return filtered log
def apply_F5(log):
    
    for i, trace in enumerate(log):
        filtered_trace =  pm4py.filter_trace(lambda t: t['lifecycle:transition'] == 'start' or t['lifecycle:transition'] == 'Start', trace)
        log[i] = filtered_trace
    return log


#given a event log and an activity, apply filter F6: Only keep events with the given activity, return filtered log
def apply_F6(log, activity):

    for i, trace in enumerate(log):
        filtered_trace =  pm4py.filter_trace(lambda t: t['Activity'] == activity, trace)
        log[i] = filtered_trace
    return log


#given a event log and a resource, apply filter F7: Only keep events with the given resource, return filtered log
def apply_F7(log, resource):

    for i, trace in enumerate(log):
        filtered_trace =  pm4py.filter_trace(lambda t: t['Resource'] == resource, trace)
        log[i] = filtered_trace
    return log


