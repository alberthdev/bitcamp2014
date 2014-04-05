#!/usr/bin/env python
# SoundRXTX v1.0 - receive and transmit data with sound!
# Copyright (C) 2014 Albert Huang, Neil Alberg, and William Heimsmoth
# Portions Copyright (C) 2006-2012 Hubert Pham
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 

import binascii

def ASCII_file_to_binary(input_file):
    with open (input_file, 'rb') as myfile:
        data = myfile.read().replace('\n', '')

    return bin(int(binascii.hexlify(data), 16))

def ASCII_to_binary(input_str):
    return bin(int(binascii.hexlify(input_str), 16))[2:]

def binary_to_ASCII(input_str):
    string = int(input_str, 2)

    return binascii.unhexlify('%x' % string)

def ASCII_file_to_hex(input_file):
    with open (input_file, 'rb') as myfile:
        data = myfile.read().replace('\n', '')
    return binascii.hexlify(data)

def ASCII_to_hex(input_str):
    return binascii.hexlify(input_str)

def hex_to_ASCII(input_str):
    return binascii.unhexlify(input_str)

if __name__ == "__main__":
    binary = ASCII_file_to_binary('test.txt')
    print(binary)
    
    binary_string = binary_to_ASCII(binary)
    print(binary_string)
    
    hex = ASCII_file_to_hex('test.txt')
    print(hex)
    
    hex_string = hex_to_ASCII(hex)
    print(hex_string)
