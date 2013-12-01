#! /usr/bin/env python3

def find_skew( sequence_file ):
	sequence = parse_sequence_file( sequence_file )
	count = 0
	skew = [ count ]
	for i in range(len(sequence)):
		if sequence[i] == 'G':
			count += 1
		if sequence[i] == 'C':
			count -= 1
		skew.append( count ) 
	min_skew = min(skew)
	min_pos = [i for i in range(len(skew)) if skew[i] == min_skew]
	return min_pos

def parse_sequence_file( sequence_file ):
	seq = ''
	with open(sequence_file) as handle:
		for line in handle:
			seq += line.strip()
	return seq

if __name__ == '__main__':
	import sys

	sequence_file = sys.argv[1]

	skew = find_skew(sequence_file)
	print(' '.join([str(s) for s in skew]))
