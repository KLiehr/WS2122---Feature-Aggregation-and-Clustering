import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer



# given an event log(sorted by timestamps!!!), add PrevAttrValue(D1) attribute to each event and then return the log
# Definition D1: says which is the latest assigned value of a given attribute excluding the current event, NotAssigned is the placeholder, if there were no prior assignments of the attribute
def add_D1(log, attr):
    '''given an event log(sorted by timestamps!!!), add PrevAttrValue(D1) attribute to each event and then return the log,
        Definition D1: says which is the latest assigned value of a given attribute excluding the current event, NotAssigned is the placeholder'''
    for trace in log:
        for event in trace:  
                event['Prev '+ attr +' Value(D1)'] = prevValue(trace, event, attr)

    return log



# returns the value of an attribute at time of a given event excluding itself
def prevValue(trace, event, attr):
    '''returns the value of an attribute at time of a given event excluding itself'''
    # denotes the latest value of the attribute
    attr_Value = 'NotAssigned'
    # denotes if we are before the event
    before = True
    

    for ev in trace:

        # update before
        if ev == event:
            before = False

        if before:
            # if the current event has the attribute, update attr_Value
            if attr in ev:
                attr_Value = ev[attr]
        else:
            return attr_Value

    return attr_Value



