import nltk
import re
from nltk.collocations import *
from nltk.corpus import stopwords
from pattern.en import parsetree
import warnings

stopset = set(stopwords.words('english')) 
stopset.add('A')
stopset.add('An')
stopset.add('The')

def is_ascii(text):
    if isinstance(text, unicode):
        try:
            text.encode('ascii')
        except UnicodeEncodeError:
            return False
    else:
        try:
            text.decode('ascii')
        except UnicodeDecodeError:
            return False
    return True

def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)

with open('imdb.txt', 'r') as text_file:
	pattern = re.compile(r'\d\$,')
	lines = text_file.readlines()
	for text in lines:
		s = parsetree(text)
		for sentence in s:
			# print sentence.chunks
			for idx in range(0,len(sentence.chunks)):
				if (sentence.chunks[idx].tag == "NP" or sentence.chunks[idx].tag == "ADJP"):
					words = []
					check = 0
					for word in sentence.chunks[idx].words:
						if (word.tag == "JJ"):
							check = 1
							break
					if check:
						for word in sentence.chunks[idx].words:
							if (is_ascii(str(word)) and not hasNumbers(str(word))):
								word = str(word).replace("/"+ word.tag + "')","")
								word = str(word).replace("Word(u'","")
								if (re.match('^[\w-]+$', word)):
									words.append(word)

					tokens = [w for w in words if not w in stopset]

					candidate = ""
					for word in tokens:
						candidate += word + " "

					if (len(candidate.strip().split()) > 1):
						warnings.filterwarnings("ignore")
						print candidate

# for sentence in s:
# 	# print sentence.chunks
# 	for idx in range(0,len(sentence.chunks)-2):
# 		if ((sentence.chunks[idx].tag == "NP" or sentence.chunks[idx].tag == "ADJP") and sentence.chunks[idx].tag):
# 			print sentence.chunks[idx]
		# if (idx == 0):
		# 	if (sentence.chunks[idx].tag == "ADJP"):
		# 		if (sentence.chunks[idx+1].tag == "NP"):
		# 			print sentence.chunks[idx]
		# 			print sentence.chunks[idx+1]
		# 			print "\n"
		# else:
		# 	if (sentence.chunks[idx].tag == "ADJP"):
		# 		if (sentence.chunks[idx+1].tag == "NP"):
		# 			print sentence.chunks[idx]
		# 			print sentence.chunks[idx+1]
		# 			print "\n"
		# 		if (sentence.chunks[idx-1].tag == "NP"):
		# 			print sentence.chunks[idx-1]
		# 			print sentence.chunks[idx]
		# 			print "\n"
				# print sentence.chunks[idx-1]
				# print sentence.chunks[idx]
				# print sentence.chunks[idx+1]
				# print "\n"
			
	# for chunk in sentence.chunks:
	# 	print chunk
 #        for tag in chunk.tag:
 #            print tag,
 #        print