import pandas as pd
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
df = pd.read_csv("https://raw.githubusercontent.com/nextstrain/ncov/fe5a7ed1f92af63d6d1d43d0307e4b2620108aaa/data/metadata.tsv", sep = '\t')
from ipycytoscape import *
df.columns
cytoscapeobj = CytoscapeWidget()
cytoscapeobj.set_tooltip_source('name')
cytoscapeobj.graph.add_graph_from_df(df[:30], ['country'], ['age', 'virus'])
cytoscapeobj
