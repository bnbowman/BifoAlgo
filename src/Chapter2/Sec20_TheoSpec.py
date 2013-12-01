#! /usr/bin/env python3

def calc_theo_spectrum( sequence_file, spectrum_table_file ):
	sequence = parse_sequence_file( sequence_file )
	spectrum_table = parse_spectrum_table( spectrum_table_file )
	peptides = identify_all_peptides( sequence )
	weights = weigh_peptides( peptides, spectrum_table )
	return [str(w) for w in sorted(weights)]

def identify_all_peptides( sequence ):
	peptides = [ sequence ]
	double_seq = sequence + sequence
	for j in range(1, len(sequence)): # peptide size
		for i in range(len(sequence)): # peptide start
			peptides.append( double_seq[i:i+j] )
	return peptides

def weigh_peptides( peptides, spectrum_table ):
	weights = [0]
	for peptide in peptides:
		weight = sum([spectrum_table[aa] for aa in peptide])
		weights.append( weight )
	return weights

def parse_sequence_file( sequence_file ):
	inputs = []
	with open(sequence_file) as handle:
		for line in handle:
			line = line.strip()
			inputs.append( line )
	return inputs[0]

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

	sequence_file = sys.argv[1]
	spectrum_table_file = sys.argv[2]

	spectrum = calc_theo_spectrum( sequence_file, spectrum_table_file )
	print(' '.join(spectrum))
