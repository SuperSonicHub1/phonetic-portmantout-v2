from difflib import SequenceMatcher
from .cmutils import is_vowel
from typing import Iterable

def join(a: Iterable[str], b: Iterable[str]) -> Iterable[str] | None:
	matcher = SequenceMatcher(a=a, b=b)
	blocks = matcher.get_matching_blocks()
	blocks_with_vowels = [
		block 
		for block 
		in blocks 
		if any(
			is_vowel(phone)
			for phone
			in a[block.a : block.a + block.size]
		)
	]

	if not len(blocks_with_vowels):
		return None
	
	block = max(blocks_with_vowels, key=lambda block: block.size)
	size = block.size

	# Infixes
	if size == len(a):
		return b
	elif size == len(b):
		return a
	# Edges
	elif block.a + size == len(a) and block.b == 0:
		return a[:block.a] + b
	elif block.b + size == len(b) and block.a == 0:
		return b[:block.b] + a
	else:
		# print(f"{a=}, {b=}, {block=}")
		return None

if __name__ == "__main__":
	def test_join(a: str, b: str) -> None:
		result_a_b = join(a, b)
		result_b_a = join(b, a)
		try:
			assert result_a_b == result_b_a
		except AssertionError:
			print(result_a_b, result_b_a)
			raise e
		print(result_a_b)

	# Classic portmanteaus
	# These don't match because we don't get a longer word.
	peaceful = "P IY S F AH L".split(" ")
	cease = "S IY S".split(" ")
	test_join(peaceful, cease)

	watermelon = "W AO T ER M EH L AH N".split(" ")
	melow = "M EH L OW".split(" ")
	test_join(watermelon, melow)

	# "Dangling"
	tree = "T R IY".split(" ")
	pee = "P IY".split(" ")
	test_join(tree, pee)

	# Subsets
	melon = "M EH L AH N".split(" ")
	test_join(watermelon, melon)

	# These don't make sense to join
	test_join(a=('P', 'R', 'AH0', 'Z', 'ER1', 'V', 'AH0', 'T', 'IH0', 'V', 'Z'), b=('P', 'R', 'AO1', 'R', 'AH0', 'K'),)
