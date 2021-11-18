import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer



# given an event log(sorted by timestamps!!!), add avg[attribute](D3) attribute to each event and then return the log
# Definition D3: computes the average value at event time(including itself), undefined is the placeholder, if there were no prior assignments of the attribute
def add_D3(log, attr):

    for trace in log:
        for event in trace:  
            event['avg' + attr + '(D3)'] = avgValue(trace, event, attr)


    return log



# returns the average value of an attribute at time of a given event(inlcuding itself)
def avgValue(trace, event, attr):

    # denotes the sum value of the attribute
    attr_Value = 0.0
    # denotes number of attribute assignments
    num_of_occ = 0
    # denotes if we are before the event
    before = True
    

    for ev in trace:

        if before:
            # if the current event has the attribute, add to attr_Value
            if attr in ev:
                try:
                    tmp_float = float(ev[attr])
                    attr_Value += tmp_float
                    num_of_occ += 1
                except ValueError:
                    print("ValueError: Failure to cast " + ev[attr] + " to float")
                    return 'FailureToCastFloat'

        # update before
        if ev == event:
            before = False

        # return attr_Value if given event has been reached and num_of_occ > 0 else return undefined
        if not before:
            if num_of_occ:
                res = attr_Value/num_of_occ
                return res
            else:
                return 'undefined'

    return 'undefined'



