"""
http://www.speech.cs.cmu.edu/cgi-bin/cmudict
"""

def is_vowel(phone: str) -> bool:
	return phone[0] in {"A", "E", "I", "O", "U"}
