from .deduplicate_words import pronunciations
from .join import join
from datetime import timedelta
import json
from time import time
from pathlib import Path

def main():
	output_path = Path.cwd() / "particles.json"

	if output_path.exists():
		return

	start = timedelta(seconds=time())
	def time_passed():
		return timedelta(seconds=time()) - start

	pronunciations = set(pronunciations)
	particles = []
	# Generated with https://github.com/ssb22/lexconvert
	# python lexconvert/lexconvert.py --phones2phones unicode-ipa cmu "ˌpɔːɹtmænˈtoʊ"
	# Doesn't seem to be entirely accurate but I'll leave it be for now.
	# current_particle = tuple("P AO2 R T M AE N T OW1".split(" "))
	current_particle = pronunciations.pop()

	while len(pronunciations):
		print("Time passed:", time_passed())

		used_pronunciations = set()
		for pronunciation in pronunciations:
			possible_join = join(current_particle, pronunciation)
			if possible_join:
				current_particle = possible_join
				used_pronunciations.add(pronunciation)

		particles.append(current_particle)
		pronunciations -= used_pronunciations
		current_particle = pronunciations.pop()
		print(current_particle)
		print(len(pronunciations), "pronunciations,", len(particles), "particles")

	# 58546 particles
	with output_path.open("w", encoding="utf-8") as f:
		json.dump(sorted(list(particles), key=len), f)
