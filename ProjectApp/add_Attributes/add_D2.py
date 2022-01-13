import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer



# given an event log(sorted by timestamps!!!), add CurAttrValue(D2) attribute to each event and then return the log
# Definition D2: says which is the latest assigned value of a given attribute, NotAssigned is the placeholder, if there were no prior assignments of the attribute
def add_D2(log, attr):
    '''given an event log(sorted by timestamps!!!), add CurAttrValue(D2) attribute to each event and then return the log,
             Definition D2: says which is the latest assigned value of a given attribute, NotAssigned is the placeholder'''
    for trace in log:
        for event in trace:  
            # shortcut to save time, if attribute is assigned in given event
            if attr in event:
                event['Cur '+ attr + ' Value(D2)'] = event[attr]
            else:
                event['Cur '+ attr +' Value(D2)'] = curValue(trace, event, attr)


    return log



# returns the value of an attribute at time of a given event
def curValue(trace, event, attr):
    '''returns the value of an attribute at time of a given event'''
    # denotes the latest value of the attribute
    attr_Value = 'NotAssigned'
    # denotes if we are before the event
    before = True
    

    for ev in trace:

        if before:
            # if the current event has the attribute, update attr_Value
            if attr in ev:
                attr_Value = ev[attr]

        # update before
        if ev == event:
            before = False

        # return attr_Value if given event has been reached
        if not before:
            return attr_Value

    return attr_Value



