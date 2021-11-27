from __future__ import print_function

import os
import subprocess

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_graphviz

from . import log_utils


from sklearn.metrics import confusion_matrix 
from sklearn.model_selection import train_test_split 
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.metrics import accuracy_score 
from sklearn.metrics import classification_report 
import graphviz


def analyze_log(log, dep_var, ind_vars):
    '''Given a log, an independant attribute and a list of dependant ones, create a decision tree'''
    print("Dependant attribute: " + dep_var)
    print("Independant attributes: " + str(ind_vars))

    # get pandas dataframe of log
    log_df = log_utils.get_df_of_log(log)
    print(log_df)

    # get independant columns
    data_columns = log_df[ind_vars]
    print(data_columns)

    # get target column
    target_column = log_df[[dep_var]]
    print(target_column)

    # Do onehotencoding:
    one_hot_data = pd.get_dummies(data_columns)
    print(one_hot_data)

    # train DecisionTree, NOT FOR CATEGORICAL VARIABLES
    tree_clf = DecisionTreeClassifier()
    tree_clf.fit(one_hot_data, target_column)
    
    # visualize tree
    dot_data = tree.export_graphviz(tree_clf, out_file=None, feature_names= one_hot_data.columns) 
    graph = graphviz.Source(dot_data) 
    graph.render('test_tree', view=True) 

    
    return log



