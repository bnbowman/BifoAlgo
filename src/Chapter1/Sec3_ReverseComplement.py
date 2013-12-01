#! /usr/bin/env python3

def find_locations( sequence_file, pattern ):
	"""
	Find the most common kmers of a given size in a given text
	"""
	sequence = parse_sequence_file( sequence_file )
	k = len(pattern)
	for i in range(len(sequence)-k+1):
		if sequence[i,i+k] == pattern:
			yield i

def parse_sequence_file( sequence_file ):
	seq = ''
	with open(sequence_file) as handle:
		for line in handle:
			seq += line.strip()
	return seq

if __name__ == '__main__':
	import sys

	sequence_file = sys.argv[1]
	pattern = sys.argv[2]

	starts = list(find_locations(sequence_file, pattern))
	print(' '.join(starts))
