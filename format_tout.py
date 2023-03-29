import json

MAX_CHARS = 280
MAX_LINES = 200
JOIN_CHAR = " "

def grouper(iterable, n, *, incomplete='fill', fillvalue=None):
	"""
	https://docs.python.org/3/library/itertools.html#itertools-recipes
	Collect data into non-overlapping fixed-length chunks or blocks
	"""
	# grouper('ABCDEFG', 3, fillvalue='x') --> ABC DEF Gxx
	# grouper('ABCDEFG', 3, incomplete='strict') --> ABC DEF ValueError
	# grouper('ABCDEFG', 3, incomplete='ignore') --> ABC DEF
	args = [iter(iterable)] * n
	return zip(*args)

with open("the_big_word.json") as f:
	phones = json.load(f)

def line_iterator():
	current_line = []
	for phone in phones:
		if (sum(len(string) for string in current_line) + len(phone) + (len(current_line) * len(JOIN_CHAR))) <= MAX_CHARS:
			current_line.append(phone)
		else:
			yield JOIN_CHAR.join(current_line)
			current_line = [phone]
	if current_line:
		yield JOIN_CHAR.join(current_line)

LATEX_TEMPLATE = """
\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\pagenumbering{gobble}
\\setlength\\parindent{0pt}
\\vspace{0pt}
\\usepackage{anyfontsize}
\\usepackage{geometry}
\\geometry{
 a4paper,
 total={200mm,270mm},
 left=4mm,
 top=5mm,
 bottom=5mm
}
\\vspace{0pt}
\linespread{0}
\\begin{document}
{
\\fontsize{2.5pt}{3pt}\\selectfont
REPLACE_ME
}
\end{document}
"""
for i, lines in enumerate(grouper(line_iterator(), int(MAX_LINES * 4.6))):
	text = "\n".join(lines)
	document = LATEX_TEMPLATE.replace("REPLACE_ME", text)
	with open(f"tout_pieces/tout_{i}.tex", "w") as f:
		f.write(document)
