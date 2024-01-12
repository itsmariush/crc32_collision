import BitVector as bv

def reverse_bits(byte):
    binary_representation = bin(byte)[2:].zfill(8)
    reversed_binary = int(binary_representation[::-1], 2)
    return reversed_binary.to_bytes(1, byteorder='big')

def reverse_bytes_in_string(data):
    reversed_data = [reverse_bits(byte) for byte in data]
    return reversed_data

# Example usage:
original_byte = b'\xBA'  # Example byte
reversed_byte = reverse_bits(original_byte[0])

print("Original byte:", original_byte)
print("Reversed byte:", reversed_byte)
# CRC32 polynomial
poly = bv.BitVector(intVal = 0x104C11DB7)

# multiplicative inverse of x^32, or 0x100000000
inv = bv.BitVector(intVal = 0x100000000).gf_MI(poly, 32)
print(inv.getHexStringFromBitVector()) # output cbf1acda

m1 = 0xF4EF771F # 0xF4EF771F
m2 = 0x1BB63F26 # = CRC(0x818080810f00000000) #0x597A4F4E=CRC(0x123456789A00000000)

xor = int('{:08b}'.format(m1 ^ m2)[::-1], 2)
print(xor)

k = xor
# k*inv mod poly
p = bv.BitVector(intVal = k).gf_multiply_modular(inv, poly, 32)
print(p.get_bitvector_in_hex())

h = 0x25d5cbcd #0x5d9fe0f5 #0xdcd1ea47
byte_array = h.to_bytes(4, byteorder='big')
rev = reverse_bytes_in_string(byte_array)
print(rev)
hex_string = ''.join([byte.decode('utf-8') if isinstance(byte, bytes) else byte for byte in rev])
print(hex_string) # = 0x3b8b57e2
# p = 0011 0110 1110 1010 0011 0001 0011 0000

# 0x818080810fa4abd3b3 !!!!!!

# 0101 1101 1001 1111 1110 0000 1111 0101
# 1011 1010   
# 1011 1010 1111 1001 0000 0111 1010 1111
