#! /usr/bin/env python3

from collections import Counter

def find_kmers( sequence_file, k ):
	"""
	Find the most common kmers of a given size in a given text
	"""
	sequence = parse_sequence_file( sequence_file )
	c = Counter()
	for i in range(len(sequence)-k+1):
		word = sequence[i:i+k]
		c[word] += 1
	word, max_count = c.most_common(1)[0]
	return [w for w, n in c.items() if n == max_count]

def parse_sequence_file( sequence_file ):
	seq = ''
	with open(sequence_file) as handle:
		for line in handle:
			seq += line.strip()
	return seq

if __name__ == '__main__':
	import sys

	sequence_file = sys.argv[1]
	k = int(sys.argv[2])

	kmers = find_kmers( sequence_file, k )
	print(' '.join(kmers))
