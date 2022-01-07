import unittest
import apply_filters
import log_utils
import os
import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.exporter.xes import exporter as xes_exporter



class TestMethod_F7(unittest.TestCase):
    '''Test filter F7'''


    def test_f7(self):
        '''test filter F7 via unittest'''

        # THE FOUR FOLLOWING VALUES NEED TO BE SET CORRECTLY!!!

        # name of log to be loaded for test, needs to be imported through program first
        log_name = 'running-example234.xes'

        # Name of resource attribute
        resource_attr = 'Resource'

        # value of the resource attribute to be filtered by
        resource_value = "Pete"

        # timestamp attribute of log, REQUIRED for sorting log
        timestamp_attr = 'time:timestamp'




        # load a log
        log = load_log_by_name(log_name, timestamp_attr)

        if not log:
            return False


        # set log_utils resource attr value, as it is used in apply_F7
        log_utils.resource_attr = resource_attr

        # filter log by resource
        log = apply_filters.apply_F7(log, resource_value)


        # assert for all cases in filtered log, that their resource attribute is of the given value
        trace_nr = 1
        for trace in log:
            for event in trace:
                print('Trace Number ' + str(trace_nr))
                print('Resource value: ' )
                print(event[resource_attr])
                self.assertEqual(resource_value, event[resource_attr])

            trace_nr += 1

        return True




def load_log_by_name(log_name, timestamp_attr):
    '''loads log for given file XES!! FILE(assuming it's been imported via program first)'''

    # get path to log file
    dir_name_here = os.path.dirname(__file__)
    folder_of_project = os.path.dirname(dir_name_here)
    folder_of_log = os.path.join(folder_of_project, 'media', 'eventlog')
    log_path = os.path.join(folder_of_log, log_name)

    # if file exists, load it
    if os.path.isfile(log_path):
        pass
    else:
        print('No such file in eventlog folder, make sure file is imported prior!')
        return 0

    # load xes file as pm4py log
    variant = xes_importer.Variants.ITERPARSE
    our_parameters = {variant.value.Parameters.TIMESTAMP_SORT: True, variant.value.Parameters.TIMESTAMP_KEY: timestamp_attr}
    log = xes_importer.apply(log_path, variant=variant, parameters= our_parameters)

    print('Log ' + log_name + ' successfully loaded!')

    return log




# check if test was started
if __name__ == '__main__':

    print('Executing unit test of filter F7')

    res = unittest.main()

    if res:
        print('Test was successfull!')
    else: 
        print('Test failed!')

   