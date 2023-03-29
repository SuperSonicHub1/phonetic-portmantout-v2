import json
import networkx as nx
from networkx.readwrite import json_graph
from .deduplicate_words import deduplicated_pronunciations
from itertools import pairwise
from pathlib import Path

def main():
	output_path = Path.cwd() / "phoneme_graph.json"

	if output_path.exists():
		return

	G = nx.DiGraph()
	for pronunciation in deduplicated_pronunciations:
		if len(pronunciation) == 1:
			G.add_node(pronunciation[0])
		else:
			G.add_edges_from(pairwise(pronunciation))

	with output_path.open( 'w') as f:
		json.dump(json_graph.node_link_data(G), f)
