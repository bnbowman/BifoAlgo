#! /usr/bin/env python3

def find_clumps( sequence_file, k, L, t ):
	sequence = parse_sequence_file( sequence_file )
	kmers = {}
	for i in range(len(sequence)-k+1):
		kmer = sequence[i:i+k]
		try:
			kmers[kmer].append( i )
		except:
			kmers[kmer] = [ i ]
	kmers = {k: sorted(v) for k, v in kmers.items() if len(v) >= t}
	results = set()
	for kmer, positions in kmers.items():
		for i in range(len(positions)-t+1):
			if positions[i+t-1] - positions[i] < L-k:
				results.add( kmer )
				break
	return results

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
	L = int(sys.argv[3])
	t = int(sys.argv[4])

	kmers = list(find_clumps(sequence_file, k, L, t))
	print(len(kmers))
