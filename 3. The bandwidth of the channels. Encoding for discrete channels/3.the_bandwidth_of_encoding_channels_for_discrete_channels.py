from math import ceil, log2, floor
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
        code_length = ceil(-log2(probability))
        code = floor(F * 2 ** code_length)
        output += bin(code)[2:].zfill(code_length)
    return output

def encode_Hamming(data):
    """Кодирует данные с использованием кода Хэмминга."""
    num_data_bits = len(data)
    print(num_data_bits)

    # Вычисление количества избыточных битов (проверочных битов)
    num_redundant_bits = 0
    while (2 ** num_redundant_bits < num_data_bits + num_redundant_bits + 1):
        num_redundant_bits += 1
    print(num_redundant_bits)

    # Создание массива для закодированных данных, включая избыточные биты
    encoded_data = [None] * (num_data_bits + num_redundant_bits)
    
    data_index = 0  # Индекс для битов данных
    for position in range(1, len(encoded_data) + 1):
        # Проверяем, является ли текущая позиция степенью двойки (позиция для избыточного бита)
        if (position & (position - 1)) == 0:
            encoded_data[position - 1] = 0  # Устанавливаем избыточный бит в 0 (будет вычислен позже)
        else:
            encoded_data[position - 1] = int(data[data_index])  # Вставляем бит данных
            data_index += 1

    # Вычисление значений избыточных битов
    for redundant_index in range(num_redundant_bits):
        redundant_position = 2 ** redundant_index  # Позиция избыточного бита (1, 2, 4, 8, ...)
        redundant_value = 0  # Значение избыточного бита (будет вычислено с использованием XOR)
        
        for bit_position in range(1, len(encoded_data) + 1):
            if bit_position & redundant_position:
                redundant_value ^= encoded_data[bit_position - 1]  # Выполняем XOR с битами на соответствующих позициях

        encoded_data[redundant_position - 1] = redundant_value  # Устанавливаем значение избыточного бита

    # Преобразуем массив битов в строку
    return ''.join(map(str, encoded_data))


def hamming_decode(encoded_data):
    """Декодирует данные, закодированные с использованием кода Хэмминга, и проверяет наличие ошибок."""
    num_bits = len(encoded_data)
    num_redundant_bits = 0
    
    # Вычисление количества избыточных битов
    while (2 ** num_redundant_bits < num_bits):
        num_redundant_bits += 1

    error_position = 0  # Позиция ошибки (0 если ошибок нет)

    # Проверка значений избыточных битов
    for redundant_index in range(num_redundant_bits):
        redundant_position = 2 ** redundant_index
        redundant_value = 0
        
        for bit_position in range(1, num_bits + 1):
            if bit_position & redundant_position:
                redundant_value ^= int(encoded_data[bit_position - 1])
        
        # Если значение избыточного бита не совпадает, то добавляем позицию в сумме
        if redundant_value != 0:
            error_position += redundant_position

    if error_position != 0:
        print(f"Ошибка обнаружена в позиции: {error_position}")
        # Исправление ошибки
        encoded_data_list = list(encoded_data)
        encoded_data_list[error_position - 1] = '1' if encoded_data_list[error_position - 1] == '0' else '0'
        encoded_data = ''.join(encoded_data_list)
        print(f"Исправленные данные: {encoded_data}")
    else:
        print("Ошибок не обнаружено")

    # Извлечение данных (исключая избыточные биты)
    decoded_data = ''
    for position in range(1, num_bits + 1):
        if (position & (position - 1)) != 0:  # Не степень двойки
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

# Кодируем слово из input.txt, используя alphabet.txt
word = encode_Shannon(frequency, string)

# Кодируем слово кодом Хэмминга
enc = encode_Hamming(word)
print(f'Код Хэмминга: {enc}')

# Строка с искаженным битом
distorted_enc = '110100011010101010101111000101110111101011111010011011000111010110100111000000001110000001010100001100100010110011000000000001111000000101010000110010001011001100010101001110110011100'

print(f'Декодированное сообщение: {hamming_decode(distorted_enc)}')
