import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
import sys
import os
import pandas as pd
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.util import constants


def callAllFilters(log, chosen_filters, extra_input):
    '''For a given log, filters and extra input for certain filters apply them all and return filtered log'''
    return log
