# Prerequisites, just run this
import networkx as nx
import pandas as pd
import json
from ipycytoscape import *
import streamlit as st

st.markdown('#Materialcheck Graph Module')


df = pd.read_csv('data_materialcheck.csv', sep=';')
# Also this
df = df.fillna('')
# df
# Import stuff to dynamically update the graph
from ipywidgets import Output
from IPython.display import display

# instantiate an jupyternotebook output
out = Output()
# style
fin_style = []
# define a function that draws the network wrt a selected node
def draw_net(node_filter):
    base_graph = nx.Graph() # reset the network obj
    for index, row in df.iterrows(): # iterate the dataframe
        if row['subgraph'] == node_filter.replace(' ',''): # if the clicked node has a subgraph
            base_graph.add_node(row['connection_to']) # add node
            base_graph.add_node(row['connection_from']) # add node
            base_graph.add_edge(row['connection_to'], row['connection_from']) # now connect the nodes
            rank = row['rank'] # also use rank as output
            subgraph = row['subgraph'] # also use subgraph as output
        elif row['label'] == node_filter: # if the clicked node does not have a subgraph, but it is alone
            base_graph.add_node(row['label']) # just draw the node on its own
            rank = row['rank'] # also use rank as output
            subgraph = row['subgraph'] # also use subgraph as output
    return [base_graph,rank,subgraph] # return the drawn graph
# define a function that logs mouse clicks
def log_clicks(node):
    # style
    fin_style = []
    with out: # while the graph is drawn
        [net,rank,subgraph] = draw_net(node['data']['id']) # draw the network
        cytoscapeobj.graph.clear() # reset cytoscape object
        cytoscapeobj.graph.add_graph_from_networkx(net, directed=True) # now convert the network to a cytoscape object
        cytoscapeobj.set_layout(name = 'dagre')  # it is hierarchical, so show it like that!
        for node in net.nodes: # now iterate the nodes
            shape = df[df.eval("(label == \""+node+"\") & ("+"subgraph == \""+subgraph+"\") & (rank == "+str(rank)+")")]['shape'].values # get the shape by filtering the dataframe
            if len(shape) == 0: # if not found, i.e. 0th level node
                shape = ['rectangle'] # draw as rectangle
            node_dict = {'selector': f'node[id = \"{node}\"]'} # get node id in cyto logic
            style_dict = {"style": {'font-family': 'helvetica','font-size': '20px','label': node, 'shape':shape[0]}} # put node id and shape in cyto logic
            node_dict.update(style_dict) # update dict
            fin_style.append(node_dict) # append to style list
        cytoscapeobj.set_style(fin_style) # now set the final style
# just initialise the 0th level graph
def init_graph():
    base_graph = nx.Graph() # reset the network obj
    for index, row in df.iterrows(): # iterate the dataframe
        if row['subgraph'] == 'initial' and row['rank'] == 1: # only draw the initial and 0th level nodes
        #base_graph.add_node(row['connection_to'])
        #base_graph.add_node(row['connection_from'])
            base_graph.add_edge(row['connection_to'], row['connection_from']) # add the edges, nodes should be added automatically
    cytoscapeobj.graph.clear() # reset cytoscape object
    cytoscapeobj.graph.add_graph_from_networkx(base_graph, directed=True) # now convert the network to a cytoscape object
    cytoscapeobj.set_layout(name = 'circle') # show it in a circular fashion
    cytoscapeobj.set_style(my_style) # set the style
# reset the graph
def res_graph(node):
    with out: # reset the DRAWN graph
        base_graph = nx.Graph() # reset the network obj
        for index, row in df.iterrows(): # iterate the dataframe
            if row['subgraph'] == 'initial' and row['rank'] == 1: # only draw the initial and 0th level nodes
            #base_graph.add_node(row['connection_to'])
            #base_graph.add_node(row['connection_from'])
                base_graph.add_edge(row['connection_to'], row['connection_from']) # add the edges, nodes should be added automatically
        cytoscapeobj.graph.clear() # reset cytoscape object
        cytoscapeobj.graph.add_graph_from_networkx(base_graph, directed=True) # now convert the network to a cytoscape object
        cytoscapeobj.set_layout(name = 'circle') # show it in a circular fashion
        cytoscapeobj.set_style(my_style) # set the style

cytoscapeobj = CytoscapeWidget() # ok now create the cytoscape object
my_style = [ # a variable for our initial style
    {'selector': 'node','style': {
        'font-family': 'helvetica',
        'font-size': '20px',
        'label': 'data(id)', 'shape':'rectangle'}},
    ]
init_graph() # init the network graph
#cytoscapeobj.set_style(my_style) # set the style
#
cytoscapeobj.on('node', 'click', log_clicks) # dynamically listen to left clicks
cytoscapeobj.on('node', 'cxttap', res_graph) # dynamically listen to right clicks

display(cytoscapeobj) # display the object
display(out) # display the output
