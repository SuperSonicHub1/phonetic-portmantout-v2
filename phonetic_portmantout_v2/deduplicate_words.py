"""
Remove overlapping words such as *read* and *reading*...
R IY D .
R IY D IH NG .
using a trie. Because of how tries are constructed, smaller
overlapping words will become part of larger ones, and ultimately
all words will be found at nodes with an out degree of zero.

===

# Subsets and supersets/affixes
In an orthographic sense, *run* is a subset of *run*ning.
Three kinds of subsets: prefixes, suffixes, and infixes.
We already have a prefix tree
We can make a suffix tree as well (this would be a much more literal copying of the rhyme trie)
The words we then want are the leaves of the tree: in degree of one and an out degree of zero.

~Infixes require a little more elbow grease; we can find them through a function that finds any affix~
Going for infixes at this stage isn't worth it, we should just handle them during the main stage.
"""

# import nltk
# nltk.download('cmudict')

from difflib import SequenceMatcher
from typing import Iterable, List
import networkx as nx
from nltk.corpus import cmudict

def leaves(G: nx.DiGraph) -> List[str]:
	return [tuple(node.split(' ')) for node in G.nodes if G.in_degree(node) == 1 and G.out_degree(node) == 0]

def deduplicate(pronunciations: Iterable[str]) -> List[str]:
	trie = nx.DiGraph()

	for pronunciation in pronunciations:
		stages = [''] + [' '.join(pronunciation[:index]) for index in range(1, len(pronunciation) + 1)]
		for i in range(len(stages) - 1):
			trie.add_edge(stages[i], stages[i + 1], phone=pronunciation[i])
	
	return leaves(trie)

def is_affix(subset, superset):
	matcher = SequenceMatcher(a=subset, b=superset)
	block = matcher.find_longest_match(0, len(subset), 0, len(superset))
	return block.a == 0 and block.size == len(subset)

pronunciations = [tuple(pronunciation) for _, pronunciation in cmudict.entries()]
# 133737
# print(len(pronunciations))

unique_pronunciations = set(pronunciations)
# 114966 (14% reduction)
# print(len(unique_pronunciations))

deduplicated_pronunciations_by_prefix = deduplicate(unique_pronunciations)
# 87627 (34% reduction)
# print(len(deduplicated_pronunciations_by_prefix))

deduplicated_pronunciations_by_suffix = {
	pronunciaition[::-1]
	for pronunciaition in
	(deduplicate(pronunciation[::-1] for pronunciation in deduplicated_pronunciations_by_prefix))
}
# 81187 (39% reduction)
# print(len(deduplicated_pronunciations_by_suffix))

deduplicated_pronunciations = deduplicated_pronunciations_by_suffix

