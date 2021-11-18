import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer



# given an event log(sorted by timestamps!!!), add sum[attribute](D3) attribute to each event and then return the log
# Definition D6: computes the sum of an attributes assigned values at event time(including itself), undefined is the placeholder, if there were no prior assignments of the attribute
def add_D6(log, attr):

    for trace in log:
        for event in trace:  
            event['sum' + attr + '(D6)'] = sumValue(trace, event, attr)


    return log



# returns the sum value of an attribute at time of a given event(inlcuding itself)
def sumValue(trace, event, attr):

    # denotes the sum value of the attribute
    sum_Value = 0.0
    # denotes if we are before the event
    before = True
    # denotes whether we have found at least one assignment for attr
    un_assingned = True

    for ev in trace:

        if before:
            # if the current event has the attribute, add to sum_Value
            if attr in ev:
                try:
                    tmp_float = float(ev[attr])
                    sum_Value += tmp_float
                    un_assingned = False
                except ValueError:
                    print("ValueError: Failure to cast " + ev[attr] + " to float")
                    return 'FailureToCastFloat'

        # update before
        if ev == event:
            before = False

        # return attr_Value if given event has been reached and num_of_occ > 0 else return undefined
        if not before:
            if not un_assingned:
                res = sum_Value
                return res
            else:
                return 'undefined'

    return 'undefined'



