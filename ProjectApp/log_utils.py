import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
import sys
import os
import pandas as pd
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter, variants
from pm4py.util import constants
from xml.etree.ElementTree import ElementTree as ET
import datetime

# global variables for designating activity, resource, timestamp etc. with their default values
case_id_attr = '' # needed for creating csv's log
activity_attr = 'Activity'
resource_attr = 'Resource'
timestamp_attr = 'time:timestamp' # needed even for creating log file
lifecycle_transition_attr = ''

# if events contain both their events start and end time
start_time_attr = ''
end_time_attr = ''

# names in correct order of target variable values of last created tree
target_name_list = []

# currently set log
cur_log = ''

# Latest prediction from a decision tree # TODO replace global variable with better solution
last_pred = []

# Latest created sublogs # TODO replace global variable with better solution
last_sublogs = []

# logs event attrs
log_ev_attrs = []

# logs numerical event attrs
num_log_ev_attrs = []

# base log, do not change after set!!!
base_log = []

def getPathOfLogFile():
    '''returns path to log file '''
    # check if a log file is set
    if cur_log == '':
        print('Error: Called getPathLogFile but !!!No Log File Set!!!')
        return 'NoLogFileSet'
    # get log location dir
    dir_name_here = os.path.dirname(__file__)
    folder_of_log = os.path.dirname(dir_name_here)
    path_for_adding_attr = os.path.join(folder_of_log, 'media', 'eventlog')

    # add filename
    our_filePath = os.path.join(path_for_adding_attr, cur_log)
    

    return our_filePath


def getPathOfLogDir():
    ''' returns directory of log file'''
    # get dir location of log
    dir_name_here = os.path.dirname(__file__)
    folder_of_log = os.path.dirname(dir_name_here)
    path_for_adding_attr = os.path.join(folder_of_log, 'media', 'eventlog')

    return path_for_adding_attr


def get_image_path():
    ''' returns directory of image files'''
    # get dir location of images
    dir_name_here = os.path.dirname(__file__)
    folder_of_log = os.path.dirname(dir_name_here)
    path_for_adding_image = os.path.join(folder_of_log, 'media', 'images')

    return path_for_adding_image


def get_sublog_image_path():
    ''' returns directory of sublog image files'''
    # get dir location of images
    dir_name_here = os.path.dirname(__file__)
    folder_of_log = os.path.dirname(dir_name_here)
    path_for_sublog_images = os.path.join(folder_of_log, 'media', 'images', 'sublog images')

    return path_for_sublog_images


def get_sublog_xes_path():
    ''' returns directory of sublog xes files'''
    # get dir location of images
    dir_name_here = os.path.dirname(__file__)
    folder_of_log = os.path.dirname(dir_name_here)
    path_for_sublog_images = os.path.join(folder_of_log, 'media', 'images', 'sublog xes files')

    return path_for_sublog_images

def isXES():
    '''IMPORTANT: We assume the file to be either csv and xes, named our_file to be there
     returns true if our file is an XES file
     else return false '''
 

    # check if a log file is set
    if cur_log == '':
        print('Error: Called isXes but !!!No Log File Set!!!')
        return 'NoLogFileSet'
    
    if len(cur_log) < 4:
        print('Filename to short!!!: ' + cur_log)
        return 'Filename to short!!!'

    if cur_log[-4:] == '.xes':
        return True
    elif cur_log[-4:] == '.csv':
        return False 
    else: # TODO Throw an error of some sort
        print('File currently set: ' + cur_log + ' Does not end with either .xes or .csv!!!')
        return False



def get_log():
    ''' returns a log created from the current file'''

    # read in XES log via pm4py to event log
    if isXES():
        variant = xes_importer.Variants.ITERPARSE
        our_parameters = {variant.value.Parameters.TIMESTAMP_SORT: True, variant.value.Parameters.TIMESTAMP_KEY: timestamp_attr}
        log = xes_importer.apply(getPathOfLogFile(), variant=variant, parameters= our_parameters)
    else:
        # !!!!!! REQUIRES CSV TO HAVE designated timestamp and case columns !!!!!! 
        if not case_id_attr:
            raise NameError("No Value assigned to case_id_attr, hence conversion of csv to log failed")
        log_csv = pd.read_csv(getPathOfLogFile(), sep=',')
        # denotes the case id attribute
        our_parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: case_id_attr}
        log_csv = dataframe_utils.convert_timestamp_columns_in_df(log_csv)
        log_csv = log_csv.sort_values(timestamp_attr)
        log = log_converter.apply(log_csv, parameters= our_parameters, variant= log_converter.Variants.TO_EVENT_LOG)

    return log


def create_log(log, action_name):
    '''updates actual log file with a given event log'''
    # update actual XES file else csv
    # !!! FOR NOW ALWAYS CREATE XES !!!
    new_file_name = timeStamped(action_name) + '.xes'
    # if isXES():
    xes_exporter.apply(log, os.path.join(getPathOfLogDir(), new_file_name))
    # else:
    #    tmp_df = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)
    #    tmp_df.to_csv(os.path.join(getPathOfLogDir(), new_file_name))

    print("Updated log file named: " + new_file_name)



def create_log_without_time(log, action_name):
    '''updates actual log file with a given event log !!without timestamping!! but current log name'''
    # update actual XES file else csv
    # !!! FOR NOW ALWAYS CREATE XES !!!
    new_file_name = action_name + cur_log
    if isXES():
        xes_exporter.apply(log, os.path.join(getPathOfLogDir(), new_file_name))
    else:
        xes_exporter.apply(log, os.path.join(getPathOfLogDir(), new_file_name + '.xes'))
    # else:
    #    tmp_df = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)
    #    tmp_df.to_csv(os.path.join(getPathOfLogDir(), new_file_name))

    print("Updated log file named: " + new_file_name)



def timeStamped(fname, fmt='%Y-%m-%d-%H-%M-%S-{fname}'):
        '''This creates a timestamped filename so we don't overwrite our good work'''
        return datetime.datetime.now().strftime(fmt).format(fname=fname)


def get_df_of_log(log):
    '''Given a log(pm4py object!) return converted dataframe(pandas)'''
    parameters = {log_converter.Variants.TO_DATA_FRAME.value.Parameters.DEEP_COPY: True}
    df = log_converter.apply(log, parameters=parameters, variant=log_converter.Variants.TO_DATA_FRAME)

    return df


# gets event attributes and TRACE ATTRS by columns
def get_log_attributes():
    '''Returns event AND TRACE level attributes of the given log'''

    # check if a log file is set
    if cur_log == '':
        print('Error: Called get_log_attributes but !!!No Log File Set!!!')
        return 'NoLogFileSet'
    # get df of FILE(not log)   
    if isXES():
        variant = xes_importer.Variants.ITERPARSE
        log = xes_importer.apply(getPathOfLogFile(), variant=variant)
        log_df = get_df_of_log(log)
    else:
        log_df = pd.read_csv(getPathOfLogFile(), sep=',')

    return list(log_df.columns)




# gets event level attributes which can be cast to float
def get_numerical_attributes():
    '''Returns NUMERICAL event level attributes of the given log'''

    # check if a log file is set
    if cur_log == '':
        print('Error: Called get_log_attributes but !!!No Log File Set!!!')
        return 'NoLogFileSet'

    # get df of log FILE 
    log_df = get_df_of_log(base_log)

    num_attrs = []

    # check for each attribute by casting to float all values, whether or not it's numerical
    for attr in log_ev_attrs:
        try:
            if isNumerical(log_df, attr):
                num_attrs.append(attr)
        except TypeError: # for timestamp columns
            pass
    
    
    # return to float castable attributes
    return num_attrs




def isNumerical(log_df, col_name):
    '''Given a pandas dataframe of a log and a column name, check for float castability'''
    for col_val in log_df[col_name]:
        try:
            float(col_val)
        except ValueError:
            return False
    return True





def get_log_of_df(df):
    '''Given a dataframe(pandas) return converted log'''
    parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: case_id_attr}
    log = log_converter.apply(df, parameters=parameters, variant=log_converter.Variants.TO_EVENT_LOG)
    return log



def get_attr_values(chosen_attr):
    '''Returns list of values for a given attribute'''

    # check if a log file is set
    if cur_log == '':
        print('Error: Called get_log_attributes but !!!No Log File Set!!!')
        return 'NoLogFileSet'

    # get df of log FILE
    log_df = get_df_of_log(base_log)

    # get different values existing in the log
    attr_values = list(log_df[chosen_attr].unique())

    return attr_values