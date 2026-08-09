morse_code_dict = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----'}

# split text into ind letters into a list
# use list comprehension to replace each letter
# combine

text_to_translate = input("Text to translate: ").upper()

converted_word = []
print(list(text_to_translate))
for char in list(text_to_translate):
    if char in morse_code_dict.keys():
        a = morse_code_dict.__getitem__(char.upper())
        converted_word.append(a)
    elif char == " ":
        converted_word.append("/")
    else:
        converted_word.append(char)

print(" ".join(converted_word))

# reflection
# tried to use list comp, did not work
# went back to normal if else statements
# googled and used first solutions that came to mind
# Lots of trial and error/repeated running code and checking
# Will not accidentally look at finished code next time