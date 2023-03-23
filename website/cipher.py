from secrets import choice

class VigenereCipher():
    """
    A class used to encrypt and decrypt a string (plaintext or ciphertext) using the Vigenere Cipher given 
    the key

    Attributes:
        - check_encrypt_key: Checks the encryption key if it is of the same length as the plaintext/ciphertext
        - generate_shifted_alphabet: Generates the shifted alphabet for each letter in the (extended) key
        - encrypt: Encrypts a plaintext given the key (randomly generated if no key is given)
        - decrypt: Decrypts a ciphertext given the key
    """
    def __init__(self):
        self.alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.selection = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.,/?;:+=-*^!#$"
        self.key = []

    def check_encrypt_key(self, plaintext: str, key: str):
        """
        Checks if the key is of the same length as the plaintext, and if it is not, extends the key such that its length is the same as the plaintext

        Arguments:
            - plaintext (str): The original plaintext being used
            - key (str): The key that is being used to encrypt the plaintext

        Returns:
            - new_key (str): The extended key/original key
        """
        new_key = ""
        k_index = 0
        if len(plaintext) == len(key):
            return key
        while len(plaintext) > len(new_key):
            if (k_index + 1) == len(key):
                new_key += key[k_index]
                k_index = 0
            else:
                new_key += key[k_index]
                k_index += 1
        return new_key

    def generate_key(self, plaintext: str):
        """
        Generates a key for the Vigenere cipher given the length of the plaintext

        Arguments:
            - plaintext (str): The plaintext to be encrypted
        
        Returns:
            - key (str): The randomly generated key
        """
        key = ""
        for i in range(len(plaintext)):
            key += choice(self.selection)
        return key

    def generate_shifted_alphabet(self, key: str):
        """
        Generates a shifted alphabet for a Vigenere Cipher using the provided key.

        Arguments:
            - key (str): The key used to generate the shifted alphabet.

        Returns:
            - shifted_alphabet (list): A list containing the shifted alphabets for the Vigenere Cipher.
        """
        # Create a list to store the shifted alphabet
        shifted_alphabet = []

        # Iterate over each character in the key
        for i, char in enumerate(key):
            # Calculate the shift amount for the current character
            shift_amount = ord(char) - ord('a')

            # Generate the shifted alphabet for the current character
            shifted_letters = []
            for j in range(26):
                shifted_letters.append(chr((j + shift_amount) % 26 + ord('a')))

            # Add the shifted alphabet for the current character to the list
            shifted_alphabet.append(shifted_letters)

        return shifted_alphabet

    def encrypt(self, key: str, plaintext: str):
        """
        Generates an encrypted string given a plaintext string and a key

        Arguments:
            - key (str): The key to encrypt the plaintext using the Vigenere Cipher
            - plaintext (str): The text to be encrypted

        Returns:
            - ciphertext (str): The encrypted plaintext using the key
        """
        self.key = self.check_encrypt_key(plaintext, key)
        plaintext = list(plaintext)
        ciphertext = ""
        shifted_alphabet = self.generate_shifted_alphabet(self.key)
        for i, char in enumerate(plaintext):
            shifted_alpha = shifted_alphabet[i]
            if char.islower():
                ciphertext += shifted_alpha[self.alphabet.index(char.upper())]
            elif char.isupper():
                ciphertext += shifted_alpha[self.alphabet.index(char)].upper()
            else:
                ciphertext += char
        return ciphertext

    def decrypt(self, key: str, ciphertext: str):
        """
        Decrypts a given plaintext using a given key

        Arguments:
            - key (str): The key to decrypt the ciphertext using the Vigenere Cipher
            - ciphertext (str): The text to be decrypted

        Returns:
            - plaintext (str): The decrypted plaintext using the key
        """
        self.key = self.check_encrypt_key(ciphertext, key)
        ciphertext = list(ciphertext)
        plaintext = ""
        shifted_alphabet = self.generate_shifted_alphabet(self.key)
        for i, char in enumerate(ciphertext):
            shifted_alpha = shifted_alphabet[i]
            if char.islower():
                plaintext += self.alphabet[shifted_alpha.index(char)].lower()
            elif char.isupper():
                plaintext += self.alphabet[shifted_alpha.index(char.lower())]
            else:
                plaintext += char
        return plaintext