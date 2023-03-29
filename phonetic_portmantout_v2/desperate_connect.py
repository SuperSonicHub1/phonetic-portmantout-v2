"""
High score: 1098210 phones
"""

import json
import networkx as nx
from networkx.exception import NetworkXNoPath, NodeNotFound
from networkx.readwrite import json_graph
from .cmutils import is_vowel
from itertools import pairwise
import random

def first(iterator):
	if "__len__" in dir(iterator):
		assert len(iterator), f"{iterator=} has no items."

	for item in iterator:
		return item

def upto(iterator, condition):
	for item in iterator:
		yield item
		if condition(item):
			return

def chain_exists(G, links):
	return all(G.has_edge(u, v) for u, v in pairwise(links))

def chain_has_connections(G, links):
	return G.degree[links[0]] > 0 and G.degree[links[-1]] > 0

def try_or_exception(function):
	try:
		return function()
	except Exception as e:
		return e

def vowel_first_phones(phones):
	return phones[-1]

def vowel_last_phones(phones):
	return phones[0]

def main():
	with open("particles.json") as f:
		particles = set(tuple(particle) for particle in json.load(f))

	with open("phoneme_graph.json") as f:
		phoneme_graph = json_graph.node_link_graph(json.load(f))

	used_particles = set()

	first_particle = first(particles)
	the_big_word = first_particle
	used_particles.add(first_particle)
	
	while len(used_particles) < len(particles):
		first_phones = list(upto(the_big_word, is_vowel))
		last_phones = list(upto(reversed(the_big_word), is_vowel))[::-1]

		first_in_graph = chain_exists(phoneme_graph, first_phones)
		last_in_graph = chain_exists(phoneme_graph, last_phones)

		if not first_in_graph and not last_in_graph:
			print("We've hit a dead end with", repr(" ".join(the_big_word)), "at", len(the_big_word), "phones")
			exit()

		first_has_connections = first_in_graph and chain_has_connections(phoneme_graph, first_phones)
		last_has_connections = last_in_graph and chain_has_connections(phoneme_graph, last_phones)

		new_particle = random.choice(tuple(particles - used_particles))
		new_first_phones = list(upto(new_particle, is_vowel))
		new_last_phones = list(upto(reversed(new_particle), is_vowel))[::-1]
		
		new_first_in_graph = chain_exists(phoneme_graph, new_first_phones)
		new_last_in_graph = chain_exists(phoneme_graph, new_last_phones)

		if not new_first_in_graph and not new_last_in_graph:
			print(new_particle, "possibly sucks")
			print(new_first_in_graph, new_last_in_graph)
			# used_particles.add(new_particle)
			continue

		new_first_has_connections = new_first_in_graph and chain_has_connections(phoneme_graph, new_first_phones)
		new_last_has_connections = new_last_in_graph and chain_has_connections(phoneme_graph, new_last_phones)

		if not new_first_has_connections and not new_last_has_connections:
			# OLD ME: May be ignoring perfectly good words, but I don't care
			# NEW ME: I do care, goshdarnit.
			print(new_particle, "sucks")
			# used_particles.add(new_particle)
			continue

		if first_in_graph and first_has_connections and new_last_in_graph and new_last_has_connections:
			try:
				start_phone = vowel_last_phones(new_last_phones)
				end_phone = vowel_first_phones(first_phones)

				path = nx.shortest_path(phoneme_graph, source=start_phone, target=end_phone)

				the_big_word = (
					new_particle[:-len(new_last_phones)]
					+ tuple(path)
					+ the_big_word[len(first_phones):]
				)

				used_particles.add(new_particle)
				print("New addition at", len(the_big_word), "phones.")
				print(len(particles - used_particles), "particles left")
				continue
			except NetworkXNoPath as e:
				print(e)
				pass

		if last_in_graph and last_has_connections and new_first_in_graph and new_first_has_connections:
			try:
				start_phone = vowel_last_phones(last_phones)
				end_phone = vowel_first_phones(new_first_phones)
		
				path = nx.shortest_path(phoneme_graph, source=start_phone, target=end_phone)

				the_big_word = (
					the_big_word[:-len(last_phones)]
					+ tuple(path)
					+ new_particle[len(new_first_phones):]
				)

				used_particles.add(new_particle)
				print("New addition at", len(the_big_word), "phones.")
				print(len(particles - used_particles), "particles left")
				continue
			except NetworkXNoPath as e:
				print(e)
				pass

	with open("the_big_word.json", 'w') as f:
		json.dump(the_big_word, f)
