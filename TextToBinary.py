import binascii

def ASCII_to_binary(input):
    with open (input, 'rb') as myfile:
        data = myfile.read().replace('\n', '')

    return bin(int(binascii.hexlify(data), 16))

def binary_to_ASCII(input):
    string = int(input, 2)

    return binascii.unhexlify('%x' % string)

def ASCII_to_hex(input):
    with open (input, 'rb') as myfile:
        data = myfile.read().replace('\n', '')
    return binascii.hexlify(data)

def hex_to_ASCII(input):
    return binascii.unhexlify(input)

binary = ASCII_to_binary('test.txt')
print(binary)

binary_string = binary_to_ASCII(binary)
print(binary_string)

hex = ASCII_to_hex('test.txt')
print(hex)

hex_string = hex_to_ASCII(hex)
print(hex_string)