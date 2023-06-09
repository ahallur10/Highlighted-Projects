"""
File: writer_bot_ht.py
Author: Anshul Hallur
Purpose: Similar to assignment 9, we implement the Markov Chain Algorithm
but use a Hash ADT to determine the probability that certain words will follow 
combinations of other words in a text. 
Based on those probabilities, we can print out the list of generated text. 
"""

import random
import sys

SEED = 8
NONWORD = '@'

random.seed(SEED)

"""
Class Summary:

Hashtable: represents a hashtable with linear probing (with a decrement of 1) 
by implementing a hash table ADT, uses strings to represent a prefix
and set prefixes to be the keys in the hash table. The class provides 
methods for inserting, retrieving, and checking the presence of keys 
in the hashtable.

Fields:
    _pairs: A list representing the hash table,storing key-value pairs.
    _size: An integer representing the size of the hash table.

Important Methods:
    put(self, key, value): Inserts a key-value pair into the hashtable, 
    resolving collisions using linear probing with a decrement of 1.
    get(self, key): Retrieves the value associated with the given key, 
    returning None if the key is not found.


"""
class Hashtable:
    """
    def __init__(self, size): Initializes the Hashtable with the given size.

    Parameters:
    size: The size of the hashtable.

    Fields:
    _pairs: Initialized to a list of size `size`.
    _size: Set to the input parameter `size`.

    """
    def __init__(self, size):
        self._pairs = [None] * size
        self._size = size
    # hash function required from spec.
    """

    def _hash(self, key): The hash function computes a hash value for a given 
    string by treating its characters as coefficients in a polynomial. 
    It utilizes Horner's rule for polynomial evaluation, with a chosen value 
    of 31 for x.

    Parameters:
        key (str): The string for computing the hash value.

    """
    def _hash(self, key):
        p = 0
        for c in key:
            p = 31*p + ord(c)
        return p % self._size
    # convert tuple of values to string, hash the resulting string
    def _hash_tuple(self, key):
        key_str = ''.join(key)
        return self._hash(key_str)

    def put(self, key, value):
        index = self._hash_tuple(key)
        # linear probing with a decrement of 1
        while self._pairs[index] is not None and self._pairs[index][0] != key:
            index = (index - 1) % self._size
        self._pairs[index] = (key, value)

    def get(self, key):
        index = self._hash_tuple(key)
        # linear probing with a decrement of 1
        while self._pairs[index] is not None and self._pairs[index][0] != key:
            index = (index - 1) % self._size
        if self._pairs[index] is None:
            return None
        else:
            return self._pairs[index][1]
    """
    def __contains__(self, key): Check if the hash table contains the given 
    key.

    Parameters:
    key (tuple): The key to search for in the hash table.

    Returns:
    True if the key is found in the hash table, otherwise False.
    """
    def __contains__(self, key):
        return self.get(key) is not None

    """
    def __str__(self): Generate a string representation of the Hashtable obj. 
    showing only non-empty pairs.

    Returns:
    str: A string representation of the hash table, containing non-empty pairs 
    """
    def __str__(self):
        non_empty_pairs = []
        for pair in self._pairs:
            if pair is not None:
                non_empty_pairs.append(pair)
        return str(non_empty_pairs)

"""
Reads an integer from the user input and ensures that it is greater than 0.

Returns: An integer greater than 0.

"""
def error_check():
    value = int(input())
    while value <= 0:
        value = int(input())
    return value

"""
Reads input values for sfile, table_size, n, and random_text and performs 
error checks on n and random_text.

Returns:
    sfile : file name with the text to analyze
    table_size : size of the hashtable
    n : The prefix size 
    random_text : Size of randome text to generate


"""
def store_input():
    sfile = input()
    table_size = int(input())
    n = int(input())
    random_text = int(input())
    # Check if n is less than one
    if n < 1:
        print("ERROR: specified prefix size is less than one")
        sys.exit(0)
    # Check if random_text is less than one
    if random_text < 1:
        print("ERROR: specified size of the generated text is less than one")
        sys.exit(0)

    return sfile, table_size, n, random_text

"""
Reads and processes the input file, 
creating a hashtable of prefix and next word pairs.

Parameters:
    sfile : file name with the text to analyze
    table_size : size of the hashtable
    n : The prefix size 

Returns:
    dict_prefix : A hashtable containing prefix and next word pairs
    prefix_tuple : The initial prefix tuple

"""
def store_file(sfile, table_size, n):
    list_prefix = [' '] * n
    prefix_tuple = tuple(list_prefix)
    with open(sfile) as open_file:
        for line in open_file:
            words = line.split()
            for word in words:
                list_prefix.append(word)
    # Create a new Hashtable for storing the prefix and next word pairs
    dict_prefix = Hashtable(table_size)
    for i in range(len(list_prefix) - n):
        prefix_1 = tuple(list_prefix[i:i+n])
        next_word = list_prefix[i + n]
        if prefix_1 in dict_prefix:
            dict_prefix.get(prefix_1).append(next_word)
        else:
            dict_prefix.put(prefix_1, [next_word])
    # Return the Hashtable and prefix tuple
    return dict_prefix, prefix_tuple

"""
Generates and prints random text based on the hashtable 
and specified size of the generated text.

Parameters:
    dict_prefix : A hashtable containing prefix and next word pairs
    random_text : Size of random text
    prefix_tuple : Initial prefix tuple

Returns: None

 """

def print_output(dict_prefix, random_text, prefix_tuple):
    store_output = []
    while len(store_output) < random_text:
        # Get the list of next words based on the current prefix_tuple
        list_values = dict_prefix.get(prefix_tuple)
        if len(list_values) > 1:
            generate_random = random.randint(0,len(list_values)-1)
            selected_val = list_values[generate_random]
        else:
            selected_val = list_values[0]
        # Add the selected word to the store_output list
        store_output.append(selected_val)
        # Update prefix_tuple by removing the first word and adding the 
        # selected word
        prefix_tuple = prefix_tuple[1:] + (selected_val,)
    # Format with a space between words and 10 words per line
    for i in range(0, len(store_output), 10):
        print(' '.join(store_output[i:i+10]))

def main():
    sfile, table_size, n, random_text = store_input()
    dict_prefix, prefix_tuple = store_file(sfile, table_size, n)
    print_output(dict_prefix, random_text, prefix_tuple)


if __name__ == "__main__":
    main()