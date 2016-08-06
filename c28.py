from matasano import *

m = sha1()
m.update(b'abc')
assert(m.digest() == b"\xa9\x99\x3e\x36\x47\x06\x81\x6a\xba\x3e\x25\x71\x78\x50\xc2\x6c\x9c\xd0\xd8\x9d")

m = md4()
m.update(b'12345678901234567890123456789012345678901234567890123456789012345678901234567890')
assert(m.digest() == b'\xe3\x3b\x4d\xdc\x9c\x38\xf2\x19\x9c\x3e\x7b\x16\x4f\xcc\x05\x36')

print("Hashes are ok!")