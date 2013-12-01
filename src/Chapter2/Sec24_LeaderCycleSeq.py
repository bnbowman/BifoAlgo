#! /usr/bin/env python3

from collections import Counter
from operator import itemgetter

def cyclo_seq( spectrum_file, spectrum_table_file ):
	N, spectrum = parse_spectrum_file( spectrum_file )
	spectrum_table = parse_spectrum_table( spectrum_table_file )
	aa_weights = set(spectrum_table.values())
	peptides = list(find_possible_peptides( spectrum, aa_weights, N ))
	max_peptides = find_max_peptides( peptides, spectrum )
	return set(['-'.join([str(w) for w in p]) for p in max_peptides])

def find_possible_peptides( spectrum, weights, N ):
	peptides = [ [0] ]
	true_weight = max(spectrum)
	while peptides:
		peptides = expand_peptides( peptides, weights )
		peptides = [p for p in peptides if sum(p) <= max(spectrum)]
		for p in peptides:
			if sum( p ) != true_weight:
				continue
			yield p
			del p
		peptides = cut_peptides( peptides, spectrum, N )

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

def cut_peptides( peptides, spectrum, N ):
	if len(peptides) <= N:
		return peptides
	scores = {}
	for peptide in peptides:
		sub_peptides = find_subpeptides( peptide )
		weights = [sum(p) for p in sub_peptides]
		peptide_str = '-'.join( [str(p) for p in peptide] )
		scores[peptide_str] = sum([1 for w in weights if w in spectrum])
	sorted_scores = sorted(scores.items(), key=itemgetter(1), reverse=True)
	min_score = sorted_scores[N][1]	
	peptides = [p for p, s in scores.items() if s >= min_score]
	peptides = [[int(n) for n in p.split('-')] for p in peptides]
	return peptides

def find_max_peptides( peptides, spectrum ):
	scores = {}
	for peptide in peptides:
		sub_peptides = find_subpeptides( peptide )
		weights = [sum(p) for p in sub_peptides]
		peptide_str = '-'.join( [str(p) for p in peptide] )
		scores[peptide_str] = sum([1 for w in weights if w in spectrum])
	sorted_scores = sorted(scores.items(), key=itemgetter(1), reverse=True)
	max_score = sorted_scores[0][1]
	peptides = [p for p, s in scores.items() if s == max_score]
	peptides = [[int(n) for n in p.split('-')] for p in peptides]
	return peptides
	
def find_subpeptides( peptide ):
	subpeptides = [ peptide ]
	for j in range(1, len(peptide)):
		for i in range(len(peptide)-j+1):
			subpeptides.append( peptide[i:i+j] )
	return subpeptides

def parse_spectrum_file( spectrum_file ):
	inputs = []
	with open(spectrum_file) as handle:
		for line in handle:
			inputs += [int(w) for w in line.strip().split()]
	return inputs[0], inputs[1:]

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
