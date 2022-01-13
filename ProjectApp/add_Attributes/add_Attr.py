import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
import sys
import os
import pandas as pd
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.util import constants

# import all add attributes modules

from . import add_C1
from . import add_C2
from . import add_C3

from . import add_D1
from . import add_D2
from . import add_D3
from . import add_D4
from . import add_D5
from . import add_D6

from . import add_R1
from . import add_R2

from . import add_T1
from . import add_T2
from . import add_T3
from . import add_T4

from ProjectApp import log_utils









# gets a string with the attributes chosen for augmentation, example:  "T1,R2,C2" as well as optionally extra info as String such as [D2:Resource,D3:Activity]
# then calls all individual attribute adding functions, updating the xes file in the end
def callAllAttr(log, chosen_attr, extra_info):

    # create actual list from attribute string via ,
    attr_list = chosen_attr.split(',')

    # create actual list from info string via ,
    extra_info_list = extra_info.split(',')



    # list of attribute abbreviations that require extra_info
    extra_input_needed = ['D1','D2','D3','D4','D5','D6']

    # call each chosen function:
    for abbrv in attr_list:
        
        name_of_method = "add_" + abbrv
        
        print("Adding attribute: " + abbrv)

        # differentiate between those that need extra info
        if abbrv in extra_input_needed:

            # find fitting extra_info for an abbreviation
            for info_element in extra_info_list:
                # split along : for access
                abbr_data = str(info_element).split('!')
                if  abbr_data[0] == abbrv:
                    print("Calling " + abbrv + " with extra data: " + abbr_data[1])
                    log = getattr(getattr(sys.modules[__name__], name_of_method), name_of_method)(log, abbr_data[1])
        else:
            log = getattr(getattr(sys.modules[__name__], name_of_method), name_of_method)(log)



    # returns augmented log
    return log
        

        
# !!!DEPRECATED EVERYTHING BELOW THIS COMMENT !!! DO NOT USE!!!


# gets a string with the attributes chosen for augmentation, example:  "T1,R2,C2" as well as optionally extra info as String such as [D2:Resource,D3:Activity]
# then calls all individual attribute adding functions, updating the xes file in the end
def callAllAttr_old(chosen_attr, extra_info):
    '''Deprecated method of callAllAttr'''

    # create actual list from attribute string via ,
    attr_list = chosen_attr.split(',')

    # create actual list from info string via ,
    extra_info_list = extra_info.split(',')


    # read in XES log via pm4py to event log
    if isXES():
        variant = xes_importer.Variants.ITERPARSE
        parameter = {variant.value.Parameters.TIMESTAMP_SORT: True}
        log = xes_importer.apply(getPathOfLogFile(), variant=variant, parameters=parameter)
    else:
        # !!!!!! REQUIRES CSV TO HAVE timestamp and case:concept:name columns !!!!!!
        log_csv = pd.read_csv(getPathOfLogFile, sep=',')
        log_csv = dataframe_utils.convert_timestamp_columns_in_df(log_csv)
        log_csv = log_csv.sort_values('<timestamp_column>')
        log = log_converter.apply(log_csv)

    # list of attribute abbreviations that require extra_info
    extra_input_needed = ['D1','D2','D3','D4','D5','D6']

    # call each chosen function:
    for abbrv in attr_list:
        
        name_of_method = "add_" + abbrv
        
        print("Adding attribute: " + abbrv)

        # differentiate between those that need extra info
        if abbrv in extra_input_needed:

            # find fitting extra_info for an abbreviation
            for info_element in extra_info_list:
                # split along : for access
                abbr_data = str(info_element).split(':')
                if  abbr_data[0] == abbrv:
                    print("Calling " + abbrv + " with extra data: " + abbr_data[1])
                log = getattr(getattr(sys.modules[__name__], name_of_method), name_of_method)(log, abbr_data[1])
        else:
            log = getattr(getattr(sys.modules[__name__], name_of_method), name_of_method)(log)



    # update actual XES file
    if isXES():
        xes_exporter.apply(log, getPathOfLogFile())
    else:
        tmp_df = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)
        tmp_df.to_csv(getPathOfLogFile())

    
    print("Updated log file!")
    

# returns path to log file
def getPathOfLogFile():
    # get log location dir
    dir_name_here = os.path.dirname(__file__)
    folder_of_log = os.path.dirname(os.path.dirname(dir_name_here))
    path_for_adding_attr = os.path.join(folder_of_log, 'media', 'eventlog')

    # add filename
    if isXES():
        our_filePath = os.path.join(path_for_adding_attr, 'our_file.xes')
    else:
        our_filePath = os.path.join(path_for_adding_attr, 'our_file.csv')

    return our_filePath

# returns directory of log file
def getPathOfLogDir():
    # get dir location of log
    dir_name_here = os.path.dirname(__file__)
    folder_of_log = os.path.dirname(os.path.dirname(dir_name_here))
    path_for_adding_attr = os.path.join(folder_of_log, 'media', 'eventlog')

    return path_for_adding_attr

# IMPORTANT: We assume the file to be either csv and xes and for exactly one file to be there
# returns true if our file is an XES file
# else return false
def isXES():
    # there should only ever be one file, so just take first element of dir's list
    list_of_files = os.listdir(getPathOfLogDir())

    if list_of_files[0] == 'our_file.xes':
        return True
    else:
        return False 
