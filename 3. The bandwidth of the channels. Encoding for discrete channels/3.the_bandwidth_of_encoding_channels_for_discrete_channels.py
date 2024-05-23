import numpy as np
import heapq
import math
from collections import defaultdict
import os

os.chdir('C:/Users/anodd/Documents/coding/information_theory/3. The bandwidth of the channels. Encoding for discrete channels/')

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
        code_length = math.ceil(-math.log2(probability))
        code = math.floor(F * 2 ** code_length)
        output += bin(code)[2:].zfill(code_length)
    return output

def encode_Hamming(data):
    code_length = 0
    data_len = len(data)
    for i in range(data_len):
        if (2**i >= data_len + i + 1):
            code_length = i
            break

    redundant_bit_position = 0
    data_bit_index = 0
    output = [None]*(code_length + data_len)
    for position in range(1, data_len + code_length + 1):
        # Если текущая позиция является степенью двойки, вставляем '0'
        if position & (position - 1) == 0:
            output[position - 1] = 0
        else:
            # Вставляем текущий информационный бит
            output[position - 1] = int(data[data_bit_index])
            data_bit_index += 1

    output = result[:]
    print(output)

    for parity_bit_index in range(code_length):
        parity_value = 0
        for bit_position in range(1, data_len + 1):
            # Если позиция бита имеет 1 в parity_bit_index-м значащем разряде
            if (bit_position & (2**parity_bit_index) == (2**parity_bit_index)):
                # Выполняем XOR для вычисления значения проверочного бита
                parity_value ^= int(data[bit_position-1])
                # -bit_position используется, так как массив реверсирован
 
    # # Обновляем строку, вставляя вычисленный проверочный бит
    # data = data[data_len - (2**parity_bit_index) + 1:] + str(parity_value) + data[:data_len - (2**parity_bit_index)] 

    # return data
    return ''.join(map(str, encoded))



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

word = encode_Shannon(frequency, string)

#print(encode_Hamming(word))
print(encode_Hamming('100100101110001'))