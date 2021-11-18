import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
import sys
import os

# import all add attributes modules
import add_C1
import add_C2
import add_C3

import add_D1
import add_D2
import add_D3
import add_D4
import add_D5
import add_D6

import add_R1
import add_R2

import add_T1
import add_T2
import add_T3
import add_T4





# TODO get  xes log, get csv log
# gets a string with the attributes chosen for augmentation, example:  "T1,R2,C2"
# then calls all individual attribute adding functions, updating the xes file in the end
def callAllAttr(chosen_attr):

    # create actual list from string via ,
    attr_list = chosen_attr.split(',')



    # get log location
    dir_name_here = os.path.dirname(__file__)
    print(dir_name_here)
    path_for_adding_attr = os.path.join(dir_name_here, 'add_Attributes')
    print(path_for_adding_attr)
    sys.path.insert(0, path_for_adding_attr)


    # read in XES log via pm4py to event log
    variant = xes_importer.Variants.ITERPARSE
    parameters = {variant.value.Parameters.TIMESTAMP_SORT: True}
    log = xes_importer.apply('C:\\Users\\kaili\\Desktop\\running-example.xes', variant=variant, parameters=parameters)



    # call each chosen function:
    for abbrv in attr_list:
        
        # TODO Doesn't work for everything cause different parameters in addtion to log
        name_of_method = "add_" + abbrv
        
        print("Adding attribute: " + abbrv)
        log = getattr(getattr(sys.modules[__name__], name_of_method), name_of_method)(log)

    

    # update actual XES file
    print("Updating actual file!")
    
        

