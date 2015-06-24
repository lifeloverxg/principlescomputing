"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided
import math

WORDFILE = "assets_scrabble_words3.txt"

# Functions to manipulate ordered word lists
def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    new_idx = 0
    idx = 1
    new_list = list(list1)
    while idx < len(new_list):
        if new_list[idx] == new_list[new_idx]:
            new_list.pop(idx)
        else:
            new_idx += 1 
            idx += 1
    return new_list
                  
def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """ 
    intersect_list = []
    idx1 = 0
    idx2 = 0
    while idx1 < len(list1) and idx2 < len(list2):
        if list1[idx1] < list2[idx2]:
            idx1 += 1
        elif list1[idx1] > list2[idx2]:
            idx2 += 1 
        else:
            intersect_list.append(list1[idx1])
            idx1 += 1
            idx2 += 1
    return intersect_list

# Functions to perform merge sort
def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """   
    merge_list = []
    idx1 = 0
    idx2 = 0
    while idx1 < len(list1) and idx2 < len(list2):
        if list1[idx1] < list2[idx2]:
            merge_list.append(list1[idx1])
            idx1 += 1
        elif list1[idx1] > list2[idx2]:            
            merge_list.append(list2[idx2])
            idx2 += 1 
        else:
            merge_list.append(list1[idx1])
            merge_list.append(list2[idx2])
            idx1 += 1
            idx2 += 1  
    if idx1 >= len(list1):
        merge_list.extend(list2[idx2:])
    elif idx2 >= len(list2):
        merge_list.extend(list1[idx1:])
    return merge_list
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    #base case
    if len(list1) == 0:
        return []
    if len(list1) == 1:
        return [list1[0]]
    #recursive case
    else:
        first_half = merge_sort(list1[0: int(len(list1) / 2)])
        second_half = merge_sort(list1[int(len(list1) / 2):])        
    return merge(first_half, second_half)

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    #base case
    if len(word) == 0:
        return ['']
    #recursive case
    else:
        first_chr = word[0]
        rest = word[1:]
        rest_strings = gen_all_strings(rest)
        output_string = []
        for string in rest_strings:
            output_string.append(string)
            for string_idx in range(len(string)):
                output_string.append(string[0: string_idx] + first_chr + string[string_idx:])
            output_string.append(string + first_chr)        
        return output_string
    
# Function to load words from a file
def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    FILENAME = "assets_scrabble_words3.txt"
    url = codeskulptor.file2url(FILENAME)
    netfile = urllib2.urlopen(url)
    dictionary = [line[:-1] for line in netfile.readlines()]      
    return dictionary

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

run()
