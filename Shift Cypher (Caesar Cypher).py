#       #               #               #               #               #
#   
#    Shift Cypher a.k.a. Ceasar Cypher
#       
#       The Shift Cypher is a simple way to encrypt alphabetic text. The encryption starts by creating a bijective mapping
#    from the set of all the letters of the alphabet into the additive group of integers Z mod 26 in order (out of order assignment would be the monoalphabetic shift cypher).
#    The mapping is then applied to the plaintext to get a series of integers. Then the secret key, which can be any integer, is added (mod 26) to each character value from
#    from the plaintext. Finally the mapping is applied in reverse to obtain the cyphertext. The method for decryption is exactly the same but in reverse; convert to integers,
#    subtract the secret key (mod 26 of course) and then convert back to text.
#       Breaking this encryption is relatively easy and only requires a rudimentary frequency analysis. Since the shift is done uniformly to each letter, the frequencies of
#    of each letter are preserved, just shifted in place by the key. Because of this there are a few ways to compare the frequencies to see which key makes the cyphertext match
#    the frequencies of English speech.
#   
#       #               #                #               #               #

from math import *

# Initialize some variables to hold values related to letter position and frequency in the english language
alphabet_dict = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8, 'i':9, 'j':10, 'k':11, 'l':12, 'm':13, 'n':14, 
                 'o':15, 'p':16, 'q':17, 'r':18, 's':19, 't':20, 'u':21, 'v':22, 'w':23, 'x':24, 'y':25, 'z':26}
alphabet_list = list(alphabet_dict.keys())

english_freq = {'a':0.0855, 'b':0.0160, 'c':0.0316, 'd':0.0387, 'e':0.1210, 'f':0.0218, 'g':0.0209, 'h':0.0496, 'i':0.0733, 
                'j':0.0022, 'k':0.0081, 'l':0.0421, 'm':0.0253, 'n':0.0717, 'o':0.0747, 'p':0.0207, 'q':0.0010, 'r':0.0633, 
                's':0.0673, 't':0.0894, 'u':0.0268, 'v':0.0106, 'w':0.0183, 'x':0.0019, 'y':0.0172, 'z':0.0011}


textfile = 'dummytext.txt'
test = 'test.txt'


####
#    Here we create some functions to filter plaintext, and encrypt and decrypt shift cyphers. 
#       These will be used to create cyphertext to test the encryption breaking algorithms.        
####


# This function filters a txt file into only
#       plain lowercase text which is what
#       is required for analysis
def filter_plaintext(txtfile):
    filteredtext = ""
    with open(txtfile) as f:
        plaintext = f.readlines()
        for line in plaintext:
            for character in line.lower():
                try:
                    number = alphabet_dict[character]
                    filteredtext += character
                except: pass
    return filteredtext


# This function counts the frequency of letters, it only accepts 
#       filtered plaintext with just lowercase letters
#       and then returns the percentage of each frequency in a dictionary
def letter_frequency(text):
    frequencies = {x:0 for x in alphabet_dict.keys()}
    for character in text:
        frequencies[character] += 1
    total = sum(list(frequencies.values()))

    for key in frequencies.keys():
        frequencies[key] /= total
    return frequencies


# This function encrypts the plaintext file with the shift key
def shift_encrypt(plaintext, key):
    cyphertext = ""
    for character in plaintext:
        cyphertext += alphabet_list[((int((alphabet_dict[character] + key)) % 26)) - 1] 
    return cyphertext


# This function decrypts the cyphertext using a known shift key
def shift_decrypt(cyphertext, key):
    plaintext = ""
    for character in cyphertext:
        plaintext += alphabet_list[(int((alphabet_dict[character] - key)) % 26) - 1]
    return plaintext


#       #               #               #               #               #
#
#   The Main Decryption Breaking Function
#
#           This function takes an encrypted cyphertext and returns
#       the most statistically likely key using a simple frequency
#       analysis. The sum of the squares of the frequencies of each letter
#       is approximately 0.065, so the sum of the products of the frequencies
#       of the english alphabet and the shifted cyphertext will be closest to 0, when the
#       shift used is equal to the key used to encrypt
#
#       #               #               #               #               #
def shift_break(cyphertext):
    total = 0
    tot_list = []

    cyph_list = list(letter_frequency(cyphertext).values())
    english_freq_list = list(english_freq.values())

    for num in range(0,26):
        for loop in range(0,26):
            total += english_freq_list[loop] * cyph_list[(loop + num) % 26]
        tot_list.append(abs(total - 0.065))
        total = 0

    minimum = min(tot_list)
    for i in range(0,26):
        if (tot_list[i] == minimum):
            return i 
        

# This is a more primitive version of the above function that determines the key based on the squared difference of the frequency 
#       of each letter in the cyphertext. It is fairly accurate but not as good as the above one. This one was created without
#       consulting any texts, the above one used an algorithm pulled from a cryptography textbook
def primitive_shift_break(cyphertext):
    dum_freq, cyph_freq = english_freq, letter_frequency(cyphertext)
    shifted_placement = []

    for letter in list(cyph_freq.keys()):
        freq_difference = [abs((x - cyph_freq[letter])**2) for x in list(dum_freq.values())]
        
        minimum = min(freq_difference)
        count = 1
        for num in freq_difference:
            if(num == minimum):
                shifted_placement.append(count)
            count += 1

    for i in range(1,27):
        shifted_placement[i-1] -= i + 26
        shifted_placement[i-1] = abs(shifted_placement[i-1]) % 26

    from statistics import mode
    shift = mode(shifted_placement)
    return round(shift)



# This is a test. It takes a plaintext file 'text' and runs it through all 26 shifts
#   it tries to break each shift and outputs the key if it is successful, and an error
#   if it is not
if __name__ == "__main__":
    for i in range(0, 26):
        if(i == shift_break(shift_encrypt(filter_plaintext(test), i))):
            print("This shift was broken and it was shifted by:", i)
        else:
            print('Failed to Break, Key Was:', i)
