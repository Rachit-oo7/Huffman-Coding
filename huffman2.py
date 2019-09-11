# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 10:53:27 2019

@author: rkt30
"""
import heapq
import os

# Class of heap nodes
class heapNode:
    
    # Initialisation method
    def __init__(self,char,freq):
        self.char=char
        self.freq=freq
        self.left=None
        self.right=None
    
    # Overwrite less than method for heap nodes
    def __lt__(self,other):
        return self.freq<other.freq


# Class with compressing and decompressing methods 
class huffmanCoding:
    
    # Initialisation method
    def __init__(self,path):
        self.path=path
        self.frequency={}
        self.heap=[]
        self.codes={}
        self.reverse_codes={}
    
    # Method to get the frequencies of characters
    def obtainFrequencies(self,text):
        for char in text:
            self.frequency[char]=self.frequency.get(char,0)+1
    
    # Method to construct the heap with the help of frequency dictionary
    def constructHeap(self):
        heapq.heapify(self.heap)
        for key in self.frequency:
            temp_heap_node=heapNode(key,self.frequency[key])
            heapq.heappush(self.heap,temp_heap_node)
    
    # Method to make tree out of the heap
    def buildTree(self):
        while len(self.heap)>1:
            min1=heapq.heappop(self.heap)
            min2=heapq.heappop(self.heap)
            tempNode=heapNode(None,min1.freq+min2.freq)
            tempNode.left=min1
            tempNode.right=min2
            heapq.heappush(self.heap,tempNode)
     
    # Method to generate codes recursively
    def generateCodesHelper(self,root,curr_code):
        if not root:
            return 
        if root.char:
            self.codes[root.char]=curr_code
            self.reverse_codes[curr_code]=root.char
        self.generateCodesHelper(root.left,curr_code+'0')
        self.generateCodesHelper(root.right,curr_code+'1')
    
    # Method to generate codes and reverse codes 
    def generateCodes(self):
        root=heapq.heappop(self.heap)
        self.generateCodesHelper(root,'')
    
    # Method to get encoded text out of simple text
    def encodedText(self,input):
        output=''
        for ele in input:
            output+=self.codes[ele]
        return output
    
    # Method to pad encoded text
    def getPaddedEncodedText(self,input):
        length=len(input)
        required_padding=8-length%8
        input=input+'0'*required_padding
        pad_info='{0:08b}'.format(required_padding)
        input=pad_info+input
        return input
    
    # Method to get byte form of encoded text
    def get_byte_encoded(self,padded_encoded_text):
        length=len(padded_encoded_text)
        if length%8!=0:
            print('Improper padding')
            exit(0)
        output=bytearray()
        for i in range(0,length,8):
            byte=padded_encoded_text[i:i+8]
            output.append(int(byte,2))
        return output
            
    # Method to compress the file with path : self.path
    def compress(self):
        filename,extension=os.path.splitext(self.path)
        output_path=filename+'_compressed.bin'
        with open(self.path,'r') as file, open(output_path,'wb') as output:
            text=file.read() # reading the file
            text=text.rstrip() # removing unwanted spaces
            self.obtainFrequencies(text) # Constructing the frequency dictionary of characters in text
            self.constructHeap() # Construct min heap on the basis of frequency of characters 
            self.buildTree() # Construct tree structure using the heap
            self.generateCodes() # Generate code for each of the characters
            encoded_text=self.encodedText(text) # Get encoded text out of simple text
            padded_encoded_text=self.getPaddedEncodedText(encoded_text) # Pad encoded text propoerly
            encoded_text_in_bits=self.get_byte_encoded(padded_encoded_text) # Get byte form of encoded text
            output.write(bytes(encoded_text_in_bits)) # Write to the output file
        print('Compressesd')
        return output_path
     
    '''            OUTPUT FUNCTIONS                '''
    
    # Method to remove padding
    def removePadding(self,input):
        pad_info=input[:8]
        input=input[8:]
        pad_info=int(pad_info,2)
        input=input[:-1*pad_info]
        return input
    
    # Method to decode the text
    def decode(self,input):
        output=''
        curr_code=''
        for ele in input:
            curr_code+=ele
            if curr_code in self.reverse_codes:
                output+=self.reverse_codes[curr_code]
                curr_code=''
        return output
    
    # Method to decompress the file with path : self.path
    def decompress(self,input):
        filename,extension=os.path.splitext(self.path)
        output_path=filename+'2.txt'
        with open(input,'rb') as file, open(output_path,'w') as output:
            bit_string=''
            byte=file.read(1)
            while byte:
                byte=ord(byte)
                bits=bin(byte)[2:].rjust(8,'0')
                bit_string+=bits
                byte=file.read(1)
            bit_string=self.removePadding(bit_string)
            decoded_text=self.decode(bit_string)
            output.write(decoded_text)
        print('Decompressed')
        return output_path
        