#! /usr/bin/env python3

REV_COM = str.maketrans("ATGC-", "TACG-")

def peptide_encodings( sequence_file, codon_table_file ):
	sequence, peptide = parse_sequence_file( sequence_file )
	peptide_size = len(peptide)
	codon_table = parse_codon_table( codon_table_file )

	for f, frame in enumerate(reading_frames( sequence )):
		trans = rna_to_protein( frame, codon_table )
		for i in range(len(trans)-peptide_size+1):
			peptide_slice = trans[i:i+peptide_size]
			if peptide_slice == peptide:
				rna_source = frame[3*i:3*(i+peptide_size)]
				dna_source = rna_to_dna( rna_source )
				if f <= 2:
					yield dna_source
				elif f > 2:
					yield reverse_complement( dna_source )

def rna_to_protein( sequence, codon_table ):
	trans = ''
	for i in range(0,len(sequence),3):	
		codon = sequence[i:i+3]
		if len(codon) < 3:
			break
		trans += codon_table[codon]
	return trans

def dna_to_rna( sequence ):
	return ''.join([b if b != 'T' else 'U' for b in sequence])

def rna_to_dna( sequence ):
	return ''.join([b if b != 'U' else 'T' for b in sequence])

def reverse_complement( sequence ):
    return sequence.translate(REV_COM)[::-1]

def reading_frames( sequence ):
	forward_rna = dna_to_rna( sequence )
	for i in range(3):
		yield forward_rna[i:]
	reverse_rna = dna_to_rna( reverse_complement( sequence )) 
	for i in range(3):
		yield reverse_rna[i:]

def parse_sequence_file( sequence_file ):
	inputs = []
	with open(sequence_file) as handle:
		for line in handle:
			line = line.strip()
			inputs.append( line )
	return inputs

def parse_codon_table( codon_table_file ):
	table = {}
	with open( codon_table_file ) as handle:
		for line in handle:
			codon, *translation = line.strip().split()
			if len(translation) == 0:
				table[codon] = '*'
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

	encodings = list(peptide_encodings( sequence_file, codon_table_file ))
	print(' '.join(encodings))
