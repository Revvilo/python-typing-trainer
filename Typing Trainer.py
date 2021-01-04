import random, os, glob, msvcrt, re, sys

class Colours:
    red = '\33[31m'
    reset = '\33[0m'
    green = '\33[32m'
    white = '\33[37m'

# Convenience function
def clear():
    os.system('cls')

def list_files():
    # prints files in a numbered selection list and returns the file paths
    # (From what I can tell. It's been a while.)
    os.chdir(os.path.dirname(__file__))
    for index, file in enumerate(glob.glob("texts\\*.txt")):
        print('[' + str(index) + ']', file)
    return glob.glob("texts\\*.txt")

# Reads a file into memory
def read_words_from_file(in_file):
    print('Loading', in_file + '...')
    with open(in_file) as word_file:
        valid_words = set(word_file.read().split())
    return valid_words

# Adds a single word, which is unique to the previous word, to the queue
def iterate_queue(word_list, word_queue):
    word_queue = build_queue(word_list)
    return word_queue

# Generates a full queue
def build_queue(word_list):
    # word buffer is empty list
    word_queue = ''
    prev_word = ''
    # get 'word_buffer_size' amount of words randomly from the main list of words
    if len(word_list) < word_buffer_size:
        amt = len(word_list)
    else:
        amt = word_buffer_size
    for x in range(0, amt):
        print('\rBuilding word queue... ' + str(x) + '/' + str(word_buffer_size), end='')
        while True:
            word = random.choice(tuple(word_list))
            if word != prev_word:
                word_queue += word + ' '
                break
    return word_queue

# Game loop
def start_game(word_list):
    # constructs the word buffer to avoid lag on large files
    word_queue = build_queue(word_list)
    clear()
    # loops every time the user types the queue correctly
    while(True): # -- Word Loop
        typed_chars = ''
        # if len(word_buffer) <= 0:
        word_queue = iterate_queue(word_list, word_queue)
        # loops every time the user enters a keystroke.
        # clears user word every time they complete a queue
        while(True): # -- Character Loop
            # Print the word queue
            sys.stdout.write('\r')
            sys.stdout.write(word_queue + ' ')
            sys.stdout.flush()
            sys.stdout.write('\r')


# --        # loops through the displayed characters and checks if the user's characters match up,-
            # -printing correct chars as green and incorrect as red, and white for spaces where they shouldn't be-
            # -over the top of the previously printed word queue.
            for i, x in enumerate(typed_chars):
                # 'try' for handling if the user's string is longer than the queue they're trying to type
                try:
                    # letter is correct
                    if x == word_queue[i]:
                        sys.stdout.write(Colours.green + x + Colours.reset)
                    # or not correct
                    else:
                        if x == ' ':
                            sys.stdout.write(Colours.white + word_queue[i] + Colours.reset)
                        else:
                            sys.stdout.write(Colours.red + x + Colours.reset)
                # if it's longer than the actual queue, then it's incorrect no matter what
                except:
                    sys.stdout.write(Colours.red + x + Colours.reset)
            sys.stdout.flush()


# --        # get user's next character
            user_input = msvcrt.getch().decode("utf-8")
            # if it's a letter or number
            if user_input.isalnum() or user_input == ' ':
                # add it to their word
                typed_chars = typed_chars + user_input
            else:
                # or if it is a backspace
                if user_input == '\x08':
                    # remove one character from their word
                    typed_chars = typed_chars[:-1]
                # or if it is an enter keystroke
                if user_input == '\r':
                    # if the user's queue is correct and ends with a space, add a line break and generate a new queue
                    sys.stdout.write('\n')
                    word_queue = build_queue(word_list)
                    break
                    

# ENTRY POINT - Set up the game
if __name__ == '__main__':
    # BEGIN CFG
    # NOTE: I'm referring to these variables in a function outside of this code block... idrk why that even works let alone if it's proper
    # Define game parameters
    word_buffer_size = 10
    word_queue_count = 10

    # Define which keys are for which hand
    right_hand = set('6yhn7ujm8ik,9ol.0p;/-[\'=]')
    right_hand_words = set()
    left_hand = set('1qaz2wsx3edc4rfv5tgb')
    left_hand_words = set()
    # END CFG

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
    all_words = read_words_from_file(word_list_file)
    both_hand_words = all_words


    # sorts the file into words that can be typed by the left hand or right hand.
    for x in all_words:
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
    print('If you hit any of the arrow keys while playing the program will just crash, so that\'s one way of doing it.')
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