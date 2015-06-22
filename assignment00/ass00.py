__author__ = 'tmkasun'


def main():
    # Test cases
    rot13_encoder("abcdefg hijklmn opqrst uvw xyz @#$%^&*")
    rot13_decoder("nopqrst uvwxyza bcdefg hij klm @#$%^&*")

    rot13_decoder("Pnrfnepvcre? V zhpucersrePnrfnefnynq!")


def pvt_max(number1, number2):
    if number1 > number2:
        return number1
    return number2


english_alphabet = "abcdefghijklmnopqrstuvwxyz"  # Easy to type rather than typing the whole dictionary ;)


def rot13_encoder(message):
    encoded_message = ''  # Placeholder for the encoded message

    for character in message:

        islower = character.islower()

        character = character.lower()

        if character not in english_alphabet:
            encoded_message += character  # If not in the alphabet just add it ;)
            continue

        encoded_index = (english_alphabet.index(character) + 13) % 26
        encoded_character = english_alphabet[encoded_index]

        if not islower:
            encoded_message += encoded_character.upper()
        else:
            encoded_message += encoded_character

    print("DEBUG: encoded_message => {}".format(encoded_message))
    return encoded_message


def rot13_decoder(message):
    decoded_message = ''
    for character in message:

        character = character.lower()  # .lower() is used to accept both uppercase and lowercase characters

        if character not in english_alphabet:
            decoded_message += character
            continue
        decode_index = english_alphabet.index(character) - 13
        decoded_character = english_alphabet[decode_index]
        decoded_message += decoded_character

    print("DEBUG: decoded_message => {}".format(decoded_message))
    return decoded_message


def word_lengths(word_list):
    word_lengths_list = [len(word) for word in word_list] # Python list comprehension
    return word_lengths_list


def find_longest_word(word_lengths, words_list):
    return sorted(word_lengths(words_list))[-1]


if __name__ == '__main__':
    main()

