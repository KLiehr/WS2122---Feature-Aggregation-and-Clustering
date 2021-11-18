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

# MAYBE as utility in views level for log updates

# returns path to log file
def getPathOfLogFile():
    # get log location
    dir_name_here = os.path.dirname(__file__)
    folder_of_log = os.path.dirname(os.path.dirname(dir_name_here))
    print(folder_of_log)

    path_for_adding_attr = os.path.join(folder_of_log, 'media\\eventlog')
    our_filePath = os.path.join(path_for_adding_attr, 'our_file.xes')
    print(our_filePath)
    return our_filePath

# returns dir of log file
def getPathOfLogDir():
    # get dir location of log
    dir_name_here = os.path.dirname(__file__)
    folder_of_log = os.path.dirname(os.path.dirname(dir_name_here))
    print(folder_of_log)

    path_for_adding_attr = os.path.join(folder_of_log, 'media\\eventlog')
    return path_for_adding_attr

def isXES():
    # there should only ever be one file, so just look at its ending
    list_of_files = os.listdir(getPathOfLogDir)
    print(list_of_files)
    return True



# TODO get  xes log, get csv log
# gets a string with the attributes chosen for augmentation, example:  "T1,R2,C2"
# then calls all individual attribute adding functions, updating the xes file in the end
def callAllAttr(chosen_attr):

    # create actual list from string via ,
    attr_list = chosen_attr.split(',')


    # read in XES log via pm4py to event log
    variant = xes_importer.Variants.ITERPARSE
    parameters = {variant.value.Parameters.TIMESTAMP_SORT: True}
    log = xes_importer.apply(getPathOfLogFile, variant=variant, parameters=parameters)
    bool = isXES()


    # call each chosen function:
    for abbrv in attr_list:
        
        # Call all functions, differentiate between those that need extra info
        name_of_method = "add_" + abbrv
        
        print("Adding attribute: " + abbrv)
        log = getattr(getattr(sys.modules[__name__], name_of_method), name_of_method)(log)

    

    # update actual XES file
    xes_exporter.apply(log, getPathOfLogFile)
    print("Updated actual file!")
        

