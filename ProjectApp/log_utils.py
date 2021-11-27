import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
import sys
import os
import pandas as pd
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.util import constants
from xml.etree.ElementTree import ElementTree as ET

# global variables for designating activity, resource, timestamp etc. with their default values
activity_attr = 'Activity'
resource_attr = 'Resource'
timestamp_attr = 'time:timestamp'
lifecycle_transition_attr = ''


def getPathOfLogFile():
    '''returns path to log file '''
    # get log location dir
    dir_name_here = os.path.dirname(__file__)
    folder_of_log = os.path.dirname(dir_name_here)
    path_for_adding_attr = os.path.join(folder_of_log, 'media', 'eventlog')

    # add filename
    if isXES():
        our_filePath = os.path.join(path_for_adding_attr, 'our_file.xes')
    else:
        our_filePath = os.path.join(path_for_adding_attr, 'our_file.csv')

    return our_filePath


def getPathOfLogDir():
    ''' returns directory of log file'''
    # get dir location of log
    dir_name_here = os.path.dirname(__file__)
    folder_of_log = os.path.dirname(dir_name_here)
    path_for_adding_attr = os.path.join(folder_of_log, 'media', 'eventlog')

    return path_for_adding_attr





def isXES():
    '''IMPORTANT: We assume the file to be either csv and xes and for exactly one file, named our_file to be there
     returns true if our file is an XES file
     else return false '''
    # there should only ever be one file, so just take first element of dir's list
    list_of_files = os.listdir(getPathOfLogDir())

    if list_of_files[0] == 'our_file.xes':
        return True
    else:
        return False 



def get_log():
    ''' returns a log created from the current file'''

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

    return log


def update_log(log):
    '''updates actual log file with a given event log'''
    # update actual XES file else csv
    if isXES():
        xes_exporter.apply(log, getPathOfLogFile())
    else:
        tmp_df = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)
        tmp_df.to_csv(getPathOfLogFile())

    print("Updated log file!")


# TODO Properly read out log events rather than first event, for csv easy first line, but how for XES, treat it as XML?
def get_log_attributes(log):
    '''Returns event attributes of the given log(Just looks at first event!)'''

    return list(log[0][0].keys())



def get_df_of_log(log):
    '''Given a log return converted dataframe(pandas)'''
    parameters = {log_converter.Variants.TO_DATA_FRAME.value.Parameters.DEEP_COPY: True}
    df = log_converter.apply(log, parameters=parameters, variant=log_converter.Variants.TO_DATA_FRAME)

    return df