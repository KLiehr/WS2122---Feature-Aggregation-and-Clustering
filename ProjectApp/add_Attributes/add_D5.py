import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer



# given an event log(sorted by timestamps!!!), add min[attribute](D4) attribute to each event and then return the log
# Definition D5: computes the min value at event time(including itself), undefined is the placeholder, if there were no prior assignments of the attribute
def add_D5(log, attr):

    for trace in log:
        for event in trace:  
            event['min' + attr + '(D5)'] = minValue(trace, event, attr)


    return log



# returns the min value of an attribute at time of a given event(inlcuding itself)
def minValue(trace, event, attr):

    # denotes the min value of the attribute
    min_Value = 0.0
    # denotes if we are before the event
    before = True
    # denotes if we are still looking for our first value
    unassigned_attr = True
    

    for ev in trace:

        if before:
            # if the current event has the attribute, compare and possibly set min value
            if attr in ev:
                try:
                    tmp_float = float(ev[attr])
                    if unassigned_attr:
                        min_Value = tmp_float
                        unassigned_attr = False
                    else:
                        min_Value = min(min_Value, tmp_float)
                except ValueError:
                    print("ValueError: Failure to cast " + ev[attr] + " to float")
                    return 'FailureToCastFloat'

        # update before
        if ev == event:
            before = False

        # return min if given event has been reached and attribute assigned, else return undefined
        if not before:
            if not unassigned_attr:
                return min_Value
            else:
                return 'undefined'

    return 'undefined'



