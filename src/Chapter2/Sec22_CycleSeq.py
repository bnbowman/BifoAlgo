#! /usr/bin/env python3

from collections import Counter

def cyclo_seq( spectrum_file, spectrum_table_file ):
	spectrum = parse_spectrum_file( spectrum_file )
	spectrum_table = parse_spectrum_table( spectrum_table_file )
	aa_weights = set(spectrum_table.values())
	valid_weights = [w for w in spectrum if w in aa_weights]
	peptides = list(find_possible_peptides( spectrum, valid_weights ))
	return set(['-'.join([str(w) for w in p]) for p in peptides])

def find_possible_peptides( spectrum, weights ):
	peptides = [ [0] ]
	true_weight = max(spectrum)
	true_counts = Counter( weights )
	while peptides:
		peptides = expand_peptides( peptides, weights )
		peptides = [p for p in peptides if is_valid_subpeptide(p, spectrum)]
		for p in peptides:
			if sum( p ) != true_weight:
				continue
			counts = Counter( p )
			if counts == true_counts:	
				yield p
				del p

def is_valid_subpeptide( peptide, spectrum ):
	if sum(peptide) not in spectrum:
		return False
	if len(peptide) < 3:
		return True
	for i in range(2, len(peptide)):
		if sum(peptide[-i:]) not in spectrum:
			return False
	return True

def expand_peptides( peptides, weights ):
	new_peptides = []
	for peptide in peptides:
		for weight in weights:
			if peptide == [0]:
				copy = []
			else:
				copy = peptide[:]
			copy.append( weight ) 
			new_peptides.append( copy )
	return new_peptides		

def parse_spectrum_file( spectrum_file ):
	inputs = []
	with open(spectrum_file) as handle:
		for line in handle:
			inputs += [int(w) for w in line.strip().split()]
	return inputs

def parse_spectrum_table( spectrum_table_file ):
	table = {}
	with open( spectrum_table_file ) as handle:
		for line in handle:
			aa, size = line.strip().split()
			try:
				size = int(size)
				table[aa] = size
			except:
				raise ValueError
	return table

if __name__ == '__main__':
	import sys

	spectrum_file = sys.argv[1]
	spectrum_table_file = sys.argv[2]

	results = cyclo_seq( spectrum_file, spectrum_table_file )
	print(' '.join(results))
