def normalize(input_text):

    cyrillic_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    latin_alphabet = ['a', 'b', 'v', 'g', 'd', 'e', 'ye', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o',
                      'p', 'r', 's', 't', 'u', 'f', 'kh', 'ts', 'ch', 'sh', 'shch', None, 'y', None, 'e', 'yu', 'ya']
    map = {}

    for index in range(len(cyrillic_alphabet)):

        cyrillic_letter_lower = ord(cyrillic_alphabet[index])
        map[cyrillic_letter_lower] = latin_alphabet[index]

    for index in range(len(cyrillic_alphabet)):

        cyrillic_letter_upper = ord(cyrillic_alphabet[index].upper())

        if latin_alphabet[index]:
            map[cyrillic_letter_upper] = latin_alphabet[index].capitalize()

        elif latin_alphabet[index] is None:
            map[cyrillic_letter_upper] = latin_alphabet[index]

    translated_text = input_text.translate(map)

    transliteration = ''

    for i in translated_text:
        if i.isalnum():
            transliteration += i
        else:
            transliteration += '_'

    return transliteration


def main():
    input_text = input()
    print(normalize(input_text))


if __name__ == '__main__':
    main()