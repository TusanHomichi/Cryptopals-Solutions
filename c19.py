from matasano import *
from base64 import b64decode

ciphs = [b"SSBoYXZlIG1ldCB0aGVtIGF0IGNsb3NlIG9mIGRheQ==", b"Q29taW5nIHdpdGggdml2aWQgZmFjZXM=", b"RnJvbSBjb3VudGVyIG9yIGRlc2sgYW1vbmcgZ3JleQ==", b"RWlnaHRlZW50aC1jZW50dXJ5IGhvdXNlcy4=", b"SSBoYXZlIHBhc3NlZCB3aXRoIGEgbm9kIG9mIHRoZSBoZWFk", b"T3IgcG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==", b"T3IgaGF2ZSBsaW5nZXJlZCBhd2hpbGUgYW5kIHNhaWQ=", b"UG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==", b"QW5kIHRob3VnaHQgYmVmb3JlIEkgaGFkIGRvbmU=", b"T2YgYSBtb2NraW5nIHRhbGUgb3IgYSBnaWJl", b"VG8gcGxlYXNlIGEgY29tcGFuaW9u", b"QXJvdW5kIHRoZSBmaXJlIGF0IHRoZSBjbHViLA==", b"QmVpbmcgY2VydGFpbiB0aGF0IHRoZXkgYW5kIEk=", b"QnV0IGxpdmVkIHdoZXJlIG1vdGxleSBpcyB3b3JuOg==", b"QWxsIGNoYW5nZWQsIGNoYW5nZWQgdXR0ZXJseTo=", b"QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=", b"VGhhdCB3b21hbidzIGRheXMgd2VyZSBzcGVudA==", b"SW4gaWdub3JhbnQgZ29vZCB3aWxsLA==", b"SGVyIG5pZ2h0cyBpbiBhcmd1bWVudA==", b"VW50aWwgaGVyIHZvaWNlIGdyZXcgc2hyaWxsLg==", b"V2hhdCB2b2ljZSBtb3JlIHN3ZWV0IHRoYW4gaGVycw==", b"V2hlbiB5b3VuZyBhbmQgYmVhdXRpZnVsLA==", b"U2hlIHJvZGUgdG8gaGFycmllcnM/", b"VGhpcyBtYW4gaGFkIGtlcHQgYSBzY2hvb2w=", b"QW5kIHJvZGUgb3VyIHdpbmdlZCBob3JzZS4=", b"VGhpcyBvdGhlciBoaXMgaGVscGVyIGFuZCBmcmllbmQ=", b"V2FzIGNvbWluZyBpbnRvIGhpcyBmb3JjZTs=", b"SGUgbWlnaHQgaGF2ZSB3b24gZmFtZSBpbiB0aGUgZW5kLA==", b"U28gc2Vuc2l0aXZlIGhpcyBuYXR1cmUgc2VlbWVkLA==", b"U28gZGFyaW5nIGFuZCBzd2VldCBoaXMgdGhvdWdodC4=", b"VGhpcyBvdGhlciBtYW4gSSBoYWQgZHJlYW1lZA==", b"QSBkcnVua2VuLCB2YWluLWdsb3Jpb3VzIGxvdXQu", b"SGUgaGFkIGRvbmUgbW9zdCBiaXR0ZXIgd3Jvbmc=", b"VG8gc29tZSB3aG8gYXJlIG5lYXIgbXkgaGVhcnQs", b"WWV0IEkgbnVtYmVyIGhpbSBpbiB0aGUgc29uZzs=", b"SGUsIHRvbywgaGFzIHJlc2lnbmVkIGhpcyBwYXJ0", b"SW4gdGhlIGNhc3VhbCBjb21lZHk7", b"SGUsIHRvbywgaGFzIGJlZW4gY2hhbmdlZCBpbiBoaXMgdHVybiw=", b"VHJhbnNmb3JtZWQgdXR0ZXJseTo=", b"QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4="]

for i in range(len(ciphs)):
	ciphs[i] = b64decode(ciphs[i])

l = max(ciphs,key=len)
for i in range(len(ciphs)):
	ciphs[i] = xor(ciphs[i],l)
	
#Now have a bunch of english plaintexts, XOR'd against another english text

#Find punctuation in key
freqs = {}
for i in range(len(l)):
	ct = 0
	for c in ciphs:
		if i < len(c):
			if c[i]//16 >= 4:
				if i not in freqs:
					freqs[i] = 0
				freqs[i] += 1
			ct += 1
	if i in freqs:
		freqs[i] /= ct
			
top = sorted([(freqs[i],i) for i in freqs], reverse=True)
#Guessing punctuation at 7,8,28,17,12,3,25,2

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
		
#Just looking for letters will get me close
key = bytes([])
for i in range(len(l)):
	mx = 0
	mk = 0
	for j in range(256):
		if letter_cnt(check_ind(j,i)) >= mx:
			mx = letter_cnt(check_ind(j,i))
			mk = j
	key = key + bytes([mk])
	