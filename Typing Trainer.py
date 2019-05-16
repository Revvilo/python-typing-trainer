import random, os, glob, msvcrt, re, sys

class Colours:
    red = '\33[31m'
    reset = '\33[0m'
    green = '\33[32m'
    white = '\33[37m'

def start_game(word_list):
    # constructs the word buffer to avoid lag on large files
    word_buffer = build_buffer(word_list)
    retry_list = set()
    clear()
    # loops every time the user types the word correctly
    while(True): # -- Word Loop
        user_word = ''
        added_to_retry = False
        if len(word_buffer) <= 0:
            word_buffer = build_buffer(word_list)
        # clears user word every time they complete a word
        # loops every time the user enters a keystroke.
        while(True): # -- Character Loop
            sys.stdout.write('\r')
            for i in range(0, 10):
                if i >= len(word_buffer):
                    break
                sys.stdout.write(word_buffer[i] + ' ')
            sys.stdout.write(' ' * 10)
            sys.stdout.flush()
            sys.stdout.write('\r')


# --        # loops through the target word and checks if the user's word matches up,-
            # -printing correct chars as green and incorrect as red, and white for spaces where they shouldn't be-
            # -over the top of the previously printed word buffer.
            for i, x in enumerate(user_word):
                # 'try' for handling if the user's word is longer than the word they're trying to type
                try:
                    # letter is correct
                    if x == word_buffer[0][i]:
                        sys.stdout.write(Colours.green + x + Colours.reset)
                    # or not correct
                    else:
                        if not added_to_retry:
                            retry_list.add(word_buffer[0])
                            added_to_retry = True
                        if x == ' ':
                            sys.stdout.write(Colours.white + word_buffer[0][i] + Colours.reset)
                        else:
                            sys.stdout.write(Colours.red + x + Colours.reset)
                # if it's longer than the actual word, then it's incorrect no matter what
                except:
                    sys.stdout.write(Colours.red + x + Colours.reset)
            sys.stdout.flush()


# --        # get user's next character
            user_input = msvcrt.getch().decode("utf-8")
            # if it's a letter or number
            if user_input.isalnum() or user_input == ' ':
                # add it to their word
                user_word = user_word + user_input
            else:
                # or if it is a backspace
                if user_input == '\x08':
                    # remove one character from their word
                    user_word = user_word[:-1]
            # if the user's word is correct and ends with a space, remove the word and continue to the next one
            if user_word.lower() == (word_buffer[0]+' '):
                word_buffer.pop(0)
                break

def clear():
    os.system('cls')

def list_files():
    # prints files in a numbered selection list and returns the file paths
    # (From what I can tell. It's been a while.)
    os.chdir(".")
    for index, file in enumerate(glob.glob("texts\\*.txt")):
        print('[' + str(index) + ']', file)
    return glob.glob("texts\\*.txt")

def read_words_from_file(in_file):
    print('Loading', in_file + '...')
    with open(in_file) as word_file:
        valid_words = set(word_file.read().split())
    return valid_words

def build_buffer(word_list):
    # word buffer is empty list
    word_buffer = list()
    # get 'word_buffer_size' amount of words randomly from the main list of words
    if len(word_list) < word_buffer_size:
        amt = len(word_list)
    else:
        amt = word_buffer_size
    for x in range(0, amt):
        print('\rBuffering words... ' + str(x) + '/' + str(word_buffer_size), end='')
        word_buffer.append(random.choice(tuple(word_list)))
    return word_buffer

if __name__ == '__main__':
    # cfg
    word_buffer_size = 50

    right_hand = set('6yhn7ujm8ik,9ol.0p;/-[\'=]')
    right_hand_words = set()
    left_hand = set('1qaz2wsx3edc4rfv5tgb')
    left_hand_words = set()
    # end cfg

    # prints and returns the file list matching .txt
    file_list = list_files()
    if file_list != []:
        print('\nEnter the number for the file you would like to practice from.')
    else:
        print('\nThere are no files in the "texts" folder from where you ran this script. Go get one then restart the script!')
    print('The files must be a .txt with each word on a new line (line-feed delimited)\n')

    both_hand_count = 0
    right_hand_count = 0
    left_hand_count = 0
    global user_word
    user_word = ''

    # gets words from file
    user_input = int(input('>>'))
    word_list_file = file_list[user_input]
    english_words = read_words_from_file(word_list_file)
    both_hand_words = english_words


    # sorts the file into words that can be typed by the left hand or right hand.
    for x in english_words:
        if set(x).issubset(left_hand):
            left_hand_count += 1
            left_hand_words.add(x)
        else:
            if set(x).issubset(right_hand):
                right_hand_count += 1
                right_hand_words.add(x)
            else:
                # and just counts the file in general for consistency's stake
                both_hand_count += 1
                both_hand_words.add(x)


    print('Complete...')
    print()
    print('Word count')
    print('- Left hand: ', len(left_hand_words))
    print('- Right hand:', len(right_hand_words))
    print('- Both hands:', len(both_hand_words))
    print()
    print('Close the window at any time to exit - WIP: Command to return to word selection or exit')
    print()

    print('Do you want [L]eft [R]ight or [B]oth handed word practice?')
    while True:
        user_input = input('>>')
        if (user_input.lower() == "l"):
            print('Left hand chosen')
            start_game(left_hand_words)
            break
        else:
            if (user_input.lower() == "r"):
                print('Right hand chosen')
                start_game(right_hand_words)
                break
            else:
                if (user_input.lower() == "b"):
                    print('Both hands chosen')
                    start_game(both_hand_words)
                    break
                else:
                    print("Type one of the letters in the [square brackets]")