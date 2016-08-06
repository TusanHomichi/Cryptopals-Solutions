from base64 import b64encode

def hex2bytes(s):
	return bytes([int(s[i:i+2],16) for i in range(0,len(s),2)])

def hex2b64(s):
	return b64encode(hex2bytes(s))
	
print(hex2b64("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"))