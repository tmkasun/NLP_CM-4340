# coding=utf-8
__author__ = 'tmkasun'
import re


def main():
    # Test cases
    rot13_encoder("abcdefg hijklmn opqrst uvw xyz @#$%^&*")
    rot13_decoder("nopqrst uvwxyza bcdefg hij klm @#$%^&*")

    rot13_decoder("Pnrfnepvcre? V zhpucersrePnrfnefnynq!")

    word_list = ["car", "train", "bicycle", "motorcycle", "van", "airplane", "boat"]
    longest_word = find_longest_word(word_lengths, word_list)
    print("DEBUG: Longest word in {} list is {}({})".format(word_list, longest_word, len(longest_word)))

    hapax_list = hapax(u'./madolduwa.txt')
    print("DEBUG: Hapax words({}) in text = {}".format(len(hapax_list), hapax_list))


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
    word_lengths_list = [len(word) for word in word_list]  # Python list comprehension
    return word_lengths_list


def find_longest_word(word_length_calculator, words_list):
    return sorted(words_list, key=word_length_calculator)[-1]


def hapax(text_file):
    """
    A hapax legomenon (/ˈhæpəks lɨˈɡɒmɨnɒn/ also /ˈhæpæks/ or /ˈheɪpæks/; pl. hapax legomena;
    sometimes abbreviated to hapax, pl. hapaxes) is a word that occurs only once within a context,
    either in the written record of an entire language, in the works of an author, or in a single text.
    The term is sometimes incorrectly used to describe a word that occurs in just one of an author's works,
    even though it occurs more than once in that work. Hapax legomenon is a transliteration of Greek ἅπαξ λεγόμενον,
    meaning "(something) said (only) once"

    In Unix systems : " tr -sc 'A-Za-z' '\n' < madolduwa.txt | tr 'A-Z' 'a-z' | grep 'ing$' | sort | uniq -c "
    """
    pattern = re.compile(r'[^A-Za-z]+')
    word_count = {}
    with open(text_file, 'r') as text_file:
        for lines in text_file:
            for word in lines.split(' '):
                word = re.sub(pattern, '', word)
                word = word.lower()
                if word not in word_count:
                    word_count[word] = 1
                else:
                    word_count[word] += 1
    text_file.close()
    hapax_list = []
    for word, count in word_count.items():
        if count is 1:
            hapax_list.append(word)

    # word or can use the import operator
    # sorted_dict = sorted(word_count.items(),key=operator.itemgetter(1))
    return hapax_list


if __name__ == '__main__':
    main()

