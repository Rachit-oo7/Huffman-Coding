# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 10:50:11 2019

@author: rkt30
"""

from huffman2 import huffmanCoding

path='D:\BTECH\Projects\HuffmanCodingPractice\sample.txt'
file=huffmanCoding(path)
print('Compressing , please wait!!')
compressed_file_path=file.compress()
print('Location of compressed file : ',compressed_file_path)
print()
print('Decompressing , please wait!!')
decompressed_file_path=file.decompress(compressed_file_path)
print('Location of decompressed file : ',decompressed_file_path)