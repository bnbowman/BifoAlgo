#! /usr/bin/env python3

def translate_sequence( sequence_file, codon_table_file ):
	sequence = parse_sequence_file( sequence_file )
	codon_table = parse_codon_table( codon_table_file )
	print(codon_table)

	# Find the Kmer positions
	protein = []
	for i in range(0, len(sequence), 3):
		codon = sequence[i:i+3]
		aa = codon_table[codon]
		if aa is None:
			break
		protein.append( aa )

	return ''.join(protein)

def parse_sequence_file( sequence_file ):
	inputs = []
	with open(sequence_file) as handle:
		for line in handle:
			line = line.strip()
			inputs.append( line )
	return inputs[0]

def parse_codon_table( codon_table_file ):
	table = {}
	with open( codon_table_file ) as handle:
		for line in handle:
			codon, *translation = line.strip().split()
			if len(translation) == 0:
				table[codon] = None
			elif len(translation) == 1:
				table[codon] = translation[0]
			else:
				msg = "Invalid Codon Table entry!"
				raise TypeError( msg )
	return table

if __name__ == '__main__':
	import sys

	sequence_file = sys.argv[1]
	codon_table_file = sys.argv[2]

	protein = translate_sequence( sequence_file, codon_table_file )
	print(protein)
