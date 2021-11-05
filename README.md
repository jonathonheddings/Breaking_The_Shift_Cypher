# Breaking The Shift Cypher (a.k.a. Caesar Cypher)
This is a simple project to break the Shift Cypher using basic frequency analysis. 

---
### Overview of The Encryption    
 The Shift Cypher is a simple way to encrypt alphabetic text. The encryption starts by creating a bijective mapping from the set of all the letters of the alphabet into the additive group of integers Z mod 26 in order (out of order 
    assignment would be the monoalphabetic shift cypher). The mapping is then applied to the plaintext to get a series of 
    integers. Then the secret key, which can be any integer, is added (mod 26) to each character value from
    from the plaintext. Finally the mapping is applied in reverse to obtain the cyphertext. The method for decryption is 
    exactly the same but in reverse; convert to integers, subtract the secret key (mod 26 of course) and then convert back to text.
    I have written basic functions for filtering text, and encrypting and decrypting text using the Shift Cypher. 
 
 #### Breaking The Encyption and Recovering The Key
 Breaking this encryption is relatively easy and only requires a rudimentary frequency analysis. Since the key shift is done 
    uniformly to each letter in the message, the frequencies of each letter are preserved, just shifted in place by the value of the key mod 26. Because of this 
    there are a few ways to compare the frequencies to see which key makes the cyphertext match the frequencies of English speech. The key recovery function
    uses the fact that the sum of the square of the frequencies of each letter in the English alphabet, in your average English text, is 0.065, so if you run
    through the possible key shifts and take the sum of the product of the actual English letter frequencies and the calculated frequencies from the shifted cyphertext,
    then the result will be closest to 0.065 when the cyphertext frequencies are shifted by the key.

#### Key Recovery Function
```
def shift_break(cyphertext):
    # Temp variables
    total, tot_list = 0, []

    # Init lists of the frequencies of the cyphertext and average English 
    #       text for indexing for the loops
    cyph_list = list(letter_frequency(cyphertext).values())
    english_freq_list = list(english_freq.values())

    # Run through all the possible shifts on each frequency of each letter
    #       of the alphabet
    for num in range(0,26):
        for loop in range(0,26):
            total += english_freq_list[loop] * cyph_list[(loop + num) % 26]
        tot_list.append(abs(total - 0.065))
        total = 0

    # Find the position of the minimum value.
    minimum = min(tot_list)
    for i in range(0,26):
        if (tot_list[i] == minimum):
            return i 
```

This function when ran on an appropriate cyphertext will return the integer that is statistically most likely to be the shift key, which will be between 0 and 25. 
