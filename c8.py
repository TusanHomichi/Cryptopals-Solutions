from matasano import *

file = open("c8.txt",'r')
scores = []
for line in file:
	ciph = hex2bytes(line[:-1])
	blocks = freq([ciph[i:i+16] for i in range(0,len(ciph),16)])
	sc = 0
	for i in blocks:
		sc += blocks[i]*blocks[i]
	scores.append((sc,ciph))
	
scores = sorted(scores, reverse=True)

print(scores[:10])