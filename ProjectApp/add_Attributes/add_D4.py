import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer



# given an event log(sorted by timestamps!!!), add max[attribute](D4) attribute to each event and then return the log
# Definition D4: computes the max value at event time(including itself), undefined is the placeholder, if there were no prior assignments of the attribute
def add_D4(log, attr):

    for trace in log:
        for event in trace:  
            event['max' + attr + '(D4)'] = maxValue(trace, event, attr)


    return log



# returns the max value of an attribute at time of a given event(inlcuding itself)
def maxValue(trace, event, attr):

    # denotes the max value of the attribute
    max_Value = 0.0
    # denotes if we are before the event
    before = True
    # denotes if we are still looking for our first value
    unassigned_attr = True
    

    for ev in trace:

        if before:
            # if the current event has the attribute, add to attr_Value
            if attr in ev:
                try:
                    tmp_float = float(ev[attr])
                    if unassigned_attr:
                        max_Value = tmp_float
                        unassigned_attr = False
                    else:
                        max_Value = max(max_Value, tmp_float)
                except ValueError:
                    print("ValueError: Failure to cast " + ev[attr] + " to float")
                    return 'FailureToCastFloat'

        # update before
        if ev == event:
            before = False

        # return max if given event has been reached and attribute assigned else return undefined
        if not before:
            if not unassigned_attr:
                return max_Value
            else:
                return 'undefined'

    return 'undefined'



