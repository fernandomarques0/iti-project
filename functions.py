import bitarray
import random
from collections import defaultdict


def read_file(filename):
    with open(filename, 'rb') as file:
        bytes_array = []
        byte = file.read(1)
        while byte:
            value = int.from_bytes(byte, byteorder='little')
            bytes_array.append(value)
            byte = file.read(1)
    return bytes_array

def compressor_lzw(data, N_BITS, dictionary_length):
    dictionary = defaultdict(int)
    message = bitarray.bitarray()
    i = 0

    for x in data:
        value_bytes = bytes([x[0]])
        for d in range(len(x)):
            if d + 1 >= len(x):
                if value_bytes in dictionary:
                    message.extend(bin(dictionary[value_bytes])[2:].zfill(N_BITS))
                    break
            else:
                c = bytes([x[d+1]])

            seq = value_bytes + c

            if seq in dictionary:
                value_bytes = seq
            else:
                message.extend(bin(dictionary[value_bytes])[2:].zfill(N_BITS))
                if len(dictionary) == dictionary_length:
                    i = 1
                    value_bytes = c
                    continue
                else:
                    dictionary[seq] = len(dictionary)
                value_bytes = c

    return dictionary

def test(data, dictionary, N_BITS, dictionary_length):
    msg = bitarray.bitarray()
    value_bytes = bytes([data[0]])

    for d in range(len(data)):
        if d + 1 >= len(data):
            if value_bytes in dictionary:
                msg.extend(bin(dictionary[value_bytes])[2:].zfill(N_BITS))
                break
        else:
            c = bytes([data[d+1]])

        seq = value_bytes + c

        if seq in dictionary:
            value_bytes = seq
        else:
            msg.extend(bin(dictionary[value_bytes])[2:].zfill(N_BITS))
            if len(dictionary) == dictionary_length:
                value_bytes = c
                continue
            else:
                dictionary[seq] = len(dictionary)
            value_bytes = c

    return len(msg)
