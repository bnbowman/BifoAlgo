#! /usr/bin/env python3

def find_skew( sequence_file, n ):
	sequence = parse_sequence_file( sequence_file )
	count = 0
	skew = [ count ]
	for i in range(n):
		if sequence[i] == 'G':
			count += 1
		if sequence[i] == 'C':
			count -= 1
		skew.append( count ) 
	return skew

def parse_sequence_file( sequence_file ):
	seq = ''
	with open(sequence_file) as handle:
		for line in handle:
			seq += line.strip()
	return seq

if __name__ == '__main__':
	import sys

	sequence_file = sys.argv[1]
	n = int(sys.argv[2])

	skew = find_skew(sequence_file, n)
	print(skew)
