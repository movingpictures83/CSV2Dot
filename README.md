# CSV2Dot
# Language: Python
# Input: TXT (contains list of CSV files)
# Output: Dot (input file for Dot)
# Tested with: PluMA 1.0, Python 2.7

PluMA plugin to take a network represented by multiple CSV files
and visualize using the Dot format.

The plugin has been oriented around microbial co-occurence networks
though could be applied in general to any network.

The input TXT file contains keyword, value pairs separated by tabs.  The only 
required keyword is "correlations", which should map to a value that specifies
a CSV file with all edges and weights.  Rows and columns of the CSV file should
correspond to nodes in the network and entry (i, j) of the CSV file should
contain the weight of the edge from node i to node j.  Dot will then visualize
positive edges in green and negative edges in red, with edge thickness denoting
edge weight (thicker=stronger).

The user can also specify an optional parameter for "abundances", which maps
to a CSV file containing the abundance of each node in a set of samples (rows
represent samples, columns represent nodes, and entry (i, j) is the abundance
of node j in sample i).  If this file is provided, Dot will visualize node
size in proportion to abundance (higher=more abundant).

Finally, the user can specify an optional parameter for "clusters".  This 
would map to a CSV file containing cluster information for each node, in the following
format:

"","x"
"1","first node in cluster 1"
"2","second node in cluster 1"
"","x"
"1","first node in cluster 2"
etc.

Therefore each line "","x" indicates a new cluster.  Nodes are then specified on
separate lines, with a unique identifier.  Note node names must match between
abundance, correlation and cluster files.  If a cluster file is provided,
Dot will visualize nodes in the same cluster in close proximity, within an
enclosing bounding box.

The output file, in ".dot" format, can then be sent to one of several visualization
engines that understand the Dot language.  For more information on the Dot language,
see "Drawing graphs with dot", Gansner et al, 2015.
