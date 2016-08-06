from matasano import *

e,d,n = gen_rsa(256)

previous = {}
def server(m):
	global d,n
	if m in previous:
		return None
	previous[m] = pow(m,d,n)
	return previous[m]
	
intercept = pow(bytes2int(b'Hello!'),e,n)
server(intercept)

print("Server doesn't decrypt ciphertext: %s" % server(intercept))

s = 2
intercept *= pow(s,e,n)
intercept = server(intercept)
print("Server does allow the multiple: %s" % intercept)
intercept = (intercept*inv(s,n))%n
print("Message recovered: %s" % int2bytes(intercept))