#! /usr/bin/env python3

def find_approx_matches( sequence_file, kmer, mismatch ):
	sequence = parse_sequence_file( sequence_file )
	matches = []
	length = len(kmer)
	for i in range(len(sequence)-length+1):
		substring = sequence[i:i+length]
		count = sum([1 for b1, b2 in zip(kmer, substring) if b1 != b2])
		if count <= mismatch:
			matches.append( i )
	return matches

def parse_sequence_file( sequence_file ):
	seq = ''
	with open(sequence_file) as handle:
		for line in handle:
			seq += line.strip()
	return seq

if __name__ == '__main__':
	import sys

	sequence_file = sys.argv[1]
	kmer = sys.argv[2]
	mismatch = int(sys.argv[3])

	matches = find_approx_matches( sequence_file, kmer, mismatch )
	print(' '.join([str(m) for m in matches]))
