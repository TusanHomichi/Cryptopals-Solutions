from matasano import *
from base64 import b64decode

file = open('c20.txt','r')
ciphs = []
for line in file:
	ciphs.append(line[:-1])
file.close()

for i in range(len(ciphs)):
	ciphs[i] = b64decode(ciphs[i])

l = max(ciphs,key=len)
for i in range(len(ciphs)):
	ciphs[i] = xor(ciphs[i],l)
	
#Now have a bunch of english plaintexts, XOR'd against another english text
def check_ind(k,i):
	ret = bytes([])
	for c in ciphs:
		if i < len(c):
			ret += bytes([c[i]^k])
	return ret
	
def check_partial(k):
	for c in ciphs:
		print(xor(c,k))
		
def change(k,i,c1,c2):
	return k[:i] + bytes([k[i]^ord(c1)^ord(c2)]) + k[i+1:]
		
#Just looking for making as many characters into letters as possible
key = bytes([])
for i in range(len(l)):
	mx = 0
	mk = 0
	for j in range(256):
		if letter_cnt(check_ind(j,i)) >= mx:
			mx = letter_cnt(check_ind(j,i))
			mk = j
	key = key + bytes([mk])
	