from BitVector import BitVector
import binascii

def reverse_bits(byte):
    binary_representation = bin(byte)[2:].zfill(8)
    reversed_binary = int(binary_representation[::-1], 2)
    return reversed_binary

def msb_to_lsb(m):
    b1 = m >> 24 & 0xff
    b2 = m >> 16 & 0xff
    b3 = m >> 8 & 0xff
    b4 = m >> 0 & 0xff
    r1 = reverse_bits(b1)
    r2 = reverse_bits(b2)
    r3 = reverse_bits(b3)
    r4 = reverse_bits(b4)
    r = 0 | r1
    r = r << 8 | r2
    r = r << 8 | r3
    r = r << 8 | r4
    return r

# https://www.reddit.com/r/crypto/comments/3h6qeh/generating_crc32_collisions/
def crc32_collision(msg):
    # CRC32 polynomial
    poly = BitVector(intVal = 0x104C11DB7)
    print("CRC32 Generator polynomial:", hex(poly.int_val()))

    # multiplicative inverse of x^32, or 0x100000000
    inv = BitVector(intVal = 0x100000000).gf_MI(poly, 32)
    print("Multiplicative inverse for x^32 in mod polynomial:", hex(inv.int_val()))

    m1 = msg
    m1_crc = binascii.crc32(m1.to_bytes((m1.bit_length() + 7) // 8, byteorder='big'))
    m2 = m1 << 32
    m2_crc = binascii.crc32(m2.to_bytes((m2.bit_length() + 7) // 8, byteorder='big'))

    print("m1: {} m2: {}".format(hex(m1), hex(m2)))
    print("m1_crc: {} m2_crc: {}".format(hex(m1_crc), hex(m2_crc)))

    xor = m1_crc ^ m2_crc
    k = int(bin(xor)[2:][::-1], 2)

    # k*inv mod poly
    p = BitVector(intVal = k).gf_multiply_modular(inv, poly, 32)
    res = p.int_val()
    print("m1_crc XOR m2_crc * x^32_inverse in modulo polynomial =", hex(res))

    res_lsb = msb_to_lsb(res)
    print("with Least Significant Bit first:", hex(res_lsb))
    col = m2 ^ res_lsb
    col_crc = binascii.crc32(col.to_bytes((col.bit_length() + 7) // 8, byteorder='big'))
    print("m2:", hex(col), " CRC(m2) =", hex(col_crc))

if __name__ == "__main__":
    crc32_collision(0x818080810f)
