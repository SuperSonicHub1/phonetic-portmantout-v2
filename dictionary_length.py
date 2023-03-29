from nltk.corpus import cmudict

print(
	sum(len(pronunciation) for _, pronunciation in cmudict.entries()),
	"phones"
)
