import numpy as np
from . import log_utils
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
import pandas as pd
from pm4py.visualization.process_tree import visualizer as pt_visualizer
from pm4py.visualization.petri_net import visualizer as pn_visualizer
import os

#prediction = tree_clf.apply(X_value)
def split_log(log, prediction):
    '''Given a log and the predicted leaf node for every event in the log as a list, return a list of sublogs for every leaf node'''

    # get pandas dataframe of log
    log_df = log_utils.get_df_of_log(log)
    
    # FOR TESTING ONLY
    print(log_df)

    print('The case id: ' + log_utils.case_id_attr)
    print('The predicted leaves: ')
    print(prediction)

    sublogs = []

    # for every trace with more than 1 event: change the prediction for every event in the trace to be uniform based on majority
    for i in list(log_df[log_utils.case_id_attr].unique()):
        print('Compute majority leaf of trace: ' + i)
        trace = log_df[log_df[log_utils.case_id_attr] == i]
        if len(trace) > 1:

            # save the prediction and index for every event in a trace
            predict = []
            index = []
            for j in trace.index:
                predict.append(prediction[j])
                index.append(j)

            # count the predicted leaf node for every event in a trace and determinant the most frequent one, ties are solved randomly
            count = np.bincount(predict)
            leaf_node = np.random.choice(np.flatnonzero(count == count.max()))

            # change the prediction
            for idx in index:
                prediction[idx] = leaf_node

    # for every leaf node, create sublogs containing only events assosiated with the node
    # convert pandas dataframe back to event log before returning
    for i in list(np.unique(prediction)):
        sublog_df = log_df.iloc[[idx for idx,pred in enumerate(prediction) if pred ==  i]]
        sublog = log_utils.get_log_of_df(sublog_df)
        sublogs.append(sublog)

    return sublogs

    



def get_petri_net(log):
    '''Given a log, return a petri net'''
    net, initial_marking, final_marking = inductive_miner.apply(log, parameters= {inductive_miner.Variants.IM.value.Parameters.ACTIVITY_KEY: log_utils.activity_attr}) 

    return net, initial_marking, final_marking

def get_process_tree(log):
    '''Given a log, return a process tree'''
    tree = inductive_miner.apply_tree(log)

    return tree


def visualize_petri_net(net, initial_marking, final_marking, leaf_nr):
    gviz = pn_visualizer.apply(net, initial_marking, final_marking)
    # pn_visualizer.view(gviz)
    path_sublogs = os.path.join(log_utils.get_sublog_image_path(), ('Sublog' + str(leaf_nr)+'.png'))
    pn_visualizer.save(gviz, path_sublogs)

def visualize_process_tree(tree):
    
    gviz = pt_visualizer.apply(tree)
    pt_visualizer.view(gviz)


