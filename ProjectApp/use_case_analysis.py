from __future__ import print_function
from pdf2image import convert_from_path
import pydot

import os
import subprocess

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.tree import DecisionTreeRegressor, export_graphviz
from . import log_utils



from sklearn.model_selection import train_test_split 
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

import graphviz


def analyze_log(log, dep_var, ind_vars):
    '''Given a log, an independant attribute and a list of dependant ones, create a decision tree, return prediction'''
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

    # get non numerical ind-vars
    cat_vars = []
    for ind_var in ind_vars:
        if not log_utils.isNumerical(data_columns, ind_var):
            cat_vars.append(ind_var)
    print(cat_vars)

    # Do onehotencoding for any non numerical variable:
    one_hot_data = pd.get_dummies(data_columns, columns=cat_vars)
    print(one_hot_data)

    # train DecisionTree for cat target Regression tree for num target, data CANNOT BE CATEGORICAL VARIABLES

    if not log_utils.isNumerical(target_column, dep_var):
        tree_clf = DecisionTreeClassifier()
        tree_clf.fit(one_hot_data, target_column)
        print('Trained a decision tree!')
    else:
        tree_clf = DecisionTreeRegressor()
        tree_clf.fit(one_hot_data, target_column)
        print('Trained a regression tree!')
    
    # visualize tree
    dot_data = tree.export_graphviz(tree_clf, out_file=None, feature_names= one_hot_data.columns) 
    
    
    #graph = graphviz.Source(dot_data) 
    # graph.render(filename= log_utils.cur_log + '-tree', directory= log_utils.get_image_path(),view=True) 
    # images = convert_from_path(os.path.join(log_utils.get_image_path(), (log_utils.cur_log + '-tree')), output_folder= log_utils.get_image_path())
    #(graph,) = pydot.graph_from_dot_file(dot_data)
    #graph.write_png('somefile.png')

    # png_graph = graphviz.Source(dot_data, filename= log_utils.cur_log + '-tree_png', directory= log_utils.get_image_path(), format='png')
    png_graph = graphviz.Source(dot_data, filename= 'decTree-' + log_utils.cur_log, directory= log_utils.get_image_path(), format='png')
    png_graph.render(view=False)

    # get array of leaf values for all events in order
    prediction = tree_clf.apply(one_hot_data)
    return prediction



