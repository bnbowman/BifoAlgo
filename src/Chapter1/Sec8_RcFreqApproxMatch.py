#! /usr/bin/env python3

import itertools

REV_COM = str.maketrans("AGCT-", "TCGA-")

def find_approx_kmer( sequence_file ):
	sequence, k, m = parse_sequence_file( sequence_file )
	k = int(k)
	m = int(m)

	# Find the Kmer positions
	kmers = {}
	for i in range(len(sequence)-k+1):
		kmer = sequence[i:i+k]
		try:
			kmers[kmer].append( i )
		except:
			kmers[kmer] = [ i ]
		rc_kmer = kmer.translate(REV_COM)[::-1]
		try:
			kmers[rc_kmer].append( i )
		except:
			kmers[rc_kmer] = [ i ]

	# Add together similar kmers
	new_kmers = {}
	for kmer, pos in kmers.items():
		for similar_kmer in string_permutations( kmer, m ):
			try:
				new_kmers[similar_kmer] += pos[:]
			except KeyError:
				new_kmers[similar_kmer] = pos[:]

	max_count = max([len(v) for v in new_kmers.values()])
	best_kmers = [k for k, v in new_kmers.items() if len(v) == max_count]
	return best_kmers

def string_permutations( query, m ):
	query_list = list(query)
	output = set() # hold output
	for i in range(1,m+1):
		# pre-calculate the possible combinations of new bases
		base_combinations = list(itertools.product('AGCT', repeat=i))
		# for each combination `idx` in idxs, replace str[idx]
		for positions in itertools.combinations(range(len(query_list)), i):
			for bases in base_combinations:
				copy = query_list[:] # make a copy
				for p, b in zip(positions, bases):
					copy[p] = b
				output.add( ''.join(copy) ) # convert back to string
	return output

def parse_sequence_file( sequence_file ):
	inputs = []
	with open(sequence_file) as handle:
		for line in handle:
			line = line.strip()
			inputs.append( line )
	return inputs

if __name__ == '__main__':
	import sys

	sequence_file = sys.argv[1]

	kmers = find_approx_kmer( sequence_file )
	print(' '.join( kmers ))
