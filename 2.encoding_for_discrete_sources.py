import heapq
import math
from collections import defaultdict
import os


def result_output(output):
    """ Writing an encoded message to a file """
    with open('output.txt', 'a') as file:
        file.write(output + '\n')
        print(output)


def encodeHuffman(frequency, string):
    heap = [[weight, [symbol, ""]] for symbol, weight in frequency.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        low = heapq.heappop(heap)
        high = heapq.heappop(heap)
        for pair in low[1:]:
            pair[1] = '0' + pair[1]
        for pair in high[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [low[0] + high[0]] + low[1:] + high[1:])
    huff = sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

    """ Encoding the message """
    output = ""
    for char in string:
        for hu in huff:
            if char == hu[0]:
                output += hu[1]
    result_output(output)

    """ Decoding the message """
    decoded = ""
    while output:
        for hu in huff:
            if output.startswith(hu[1]):
                decoded += hu[0]
                output = output[len(hu[1]):]
    print("Decoded message using Huffman Encode: ", decoded)


""" mod = 0 to use the usual Shannon encoding;
    mod = 1 to use the Shannon–Fano–Elias encoding """


def encodeShannon(frequency, string, mod=0):
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
        code_length = math.ceil(-math.log2(probability / 2)) + 1
        code = math.floor((F + probability / 2) * 2 ** code_length) if mod == 1 else math.floor(
            F * 2 ** code_length)
        output += bin(code)[2:].zfill(code_length)

    result_output(output)

    """Decoding the message"""
    decoded = ""
    mod_choice = (probability / 2) if mod == 1 else 0
    while output:
        for char, probability in frequency.items():
            code_length = math.ceil(-math.log2(probability / 2)) + 1
            code = int(output[:code_length], 2)
            if math.floor((cumulative_freq[char] + mod_choice) * 2 ** code_length) <= code < math.floor(
                    (cumulative_freq[char] + probability + mod_choice) * 2 ** code_length):
                decoded += char
                output = output[code_length:]
                break

    mod_print = "Shannon-Fano–Elias" if mod == 1 else "Shannon"
    print(f"Decoded message using {mod_print} Encode: ", decoded)


def encodeGilbertMoore(frequency, string):
    """Calculate cumulative probabilities and code lengths"""
    symbols = list(frequency.keys())
    num_symbols = len(frequency)
    symb_probabilities = list(frequency.values())
    cumulative_probs = [0] * num_symbols
    code_lengths = [0] * num_symbols
    cumulative_prob = 0
    for i in range(num_symbols):
        cumulative_probs[i] = cumulative_prob + symb_probabilities[i] / 2
        cumulative_prob += symb_probabilities[i]
        code_lengths[i] = math.ceil(-math.log2(symb_probabilities[i] / 2)) + 1

    """Generate code table"""
    code_table = [[0] * max(code_lengths) for _ in range(num_symbols)]
    for i in range(num_symbols):
        for j in range(code_lengths[i]):
            cumulative_probs[i] *= 2
            code_table[i][j] = math.floor(cumulative_probs[i])
            if cumulative_probs[i] > 1:
                cumulative_probs[i] -= 1

    """Encoding the message"""
    output = ''
    for char in string:
        index = symbols.index(char)
        output += ''.join([str(bit) for bit in code_table[index][:code_lengths[index]]])

    result_output(output)

    """Decoding the message"""
    decoded_word = ''
    i = 0
    while i < len(output):
        for j in range(num_symbols):
            code_length = code_lengths[j]
            code = ''.join([str(bit) for bit in code_table[j][:code_length]])
            if output[i:i + code_length] == code:
                decoded_word += symbols[j]
                i += code_length
                break

    print("Decoded message using Gilbert-Moore Encode:", decoded_word)


""" Cleaning up residual files """
try:
    if open('output.txt'):
        os.remove('output.txt')
    print('output.txt deleted and re-created')
except FileNotFoundError:
    print('output.txt was not found')

""" Reading data from files """
with open('alphabet.txt', 'r') as f:
    lines = f.readlines()
frequency = {line.split()[0]: float(line.split()[1]) for line in lines}
with open('input2.txt', 'r') as f:
    string = f.read().strip()

encodeHuffman(frequency, string)
encodeShannon(frequency, string)
encodeShannon(frequency, string, 1)
encodeGilbertMoore(frequency, string)
