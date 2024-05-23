from math import ceil, log2, floor
from collections import defaultdict
import os

os.chdir('S:/Coding/information_theory/3. The bandwidth of the channels. Encoding for discrete channels/')


def encode_Shannon(frequency, string):
    """Calculating cumulative probabilities"""
    cumulative_freq = defaultdict(float)
    sum_freq = 0
    for char in sorted(frequency.keys()):
        cumulative_freq[char] = sum_freq
        sum_freq += frequency[char]

    """Encoding the message"""
    output = ""
    for char in string:
        probability = frequency[char]
        F = cumulative_freq[char]
        code_length = ceil(-log2(probability))
        code = floor(F * 2 ** code_length)
        output += bin(code)[2:].zfill(code_length)
    return output

def encode_Hamming(data):
    """Encodes data using a Hamming code."""
    num_data_bits = len(data)

    """Calculating the number of redundant bits (check bits)"""
    num_redundant_bits = 0
    while (2 ** num_redundant_bits < num_data_bits + num_redundant_bits + 1):
        num_redundant_bits += 1

    """Creating an array for encoded data, including redundant bits"""
    encoded_data = [None] * (num_data_bits + num_redundant_bits)
    
    """Index for data bits"""
    data_index = 0
    for position in range(1, len(encoded_data) + 1):
        """Check if the current position is a power of two (the position for the redundant bit)"""
        if (position & (position - 1)) == 0:
            """Setting the excess bit to 0 (to be calculated later)"""
            encoded_data[position - 1] = 0  
        else:
            encoded_data[position - 1] = int(data[data_index])  
            """Inserting a data bit"""
            data_index += 1

    """Calculating the values of redundant bits"""
    for redundant_index in range(num_redundant_bits):
        """Position of the redundant bit (1, 2, 4, 8, ...)"""
        redundant_position = 2 ** redundant_index  
        """The value of the redundant bit (will be calculated using XOR)"""
        redundant_value = 0  
        
        for bit_position in range(1, len(encoded_data) + 1):
            if bit_position & redundant_position:
                """Performing XOR with the bits at the appropriate positions"""
                redundant_value ^= encoded_data[bit_position - 1]  

        """Setting the value of the redundant bit"""
        encoded_data[redundant_position - 1] = redundant_value  

    """Converting an array of bits to a string"""
    return ''.join(map(str, encoded_data))


def hamming_decode(encoded_data):
    """Decodes data encoded using the Hamming code and checks for errors."""
    num_bits = len(encoded_data)
    num_redundant_bits = 0
    
    """Calculating the number of redundant bits"""
    while (2 ** num_redundant_bits < num_bits):
        num_redundant_bits += 1

    """Error position (0 if there are no errors)"""
    error_position = 0  

    """Checking the values of redundant bits"""
    for redundant_index in range(num_redundant_bits):
        redundant_position = 2 ** redundant_index
        redundant_value = 0
        
        for bit_position in range(1, num_bits + 1):
            if bit_position & redundant_position:
                redundant_value ^= int(encoded_data[bit_position - 1])
        
        """If the value of the excess bit does not match, then add the position in the sum"""
        if redundant_value != 0:
            error_position += redundant_position

    if error_position != 0:
        print(f"An error was detected in the position: {error_position}")
        """Error correction"""
        encoded_data_list = list(encoded_data)
        encoded_data_list[error_position - 1] = '1' if encoded_data_list[error_position - 1] == '0' else '0'
        encoded_data = ''.join(encoded_data_list)
        print(f"Corrected data: {encoded_data}")
    else:
        print("No errors were found")

    """Data extraction (excluding redundant bits)"""
    decoded_data = ''
    for position in range(1, num_bits + 1):
        """Not a power of two"""
        if (position & (position - 1)) != 0:  
            decoded_data += encoded_data[position - 1]

    return decoded_data


""" Reading data from files """
with open('alphabet.txt', 'r', encoding='UTF-8') as f:
    lines = f.readlines()
    if not lines:
        print("File alphabet.txt is empty!")
        exit()
frequency = {line.split(';')[0]: float(line.split(';')[1]) for line in lines}

with open('input.txt', 'r', encoding='UTF-8') as f:
    string = f.read().strip()
    if not string:
        print("File input.txt is empty!")
        exit()

check = list(set(string) - set(frequency.keys()))
if len(check) != 0:
    print("The input string has a character that is not in the alphabet!")
    exit()

"""Encode the word from input.txt using alphabet.txt"""
word = encode_Shannon(frequency, string)

"""Encode the word with a Hamming code"""
enc = encode_Hamming(word)
print(f'Hamming Code: {enc}')

"""A string with a distorted bit"""
distorted_enc = '110101011010101010101111000101110111101011111010011011000111010110100111000000001110000001010100001100100010110011000000000001111000000101010000110010001011001100010101001110110011100'

print(f'Decoded message: {hamming_decode(distorted_enc)}')
