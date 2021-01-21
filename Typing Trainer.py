import random, os, glob, re, sys
print(sys.platform[:3])
if sys.platform[:3] == 'win':
    import msvcrt
    def getKey():
        return msvcrt.getch()
elif sys.platform[:3] == 'lin':
    import termios, sys, os
    TERMIOS = termios
    def getKey():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        new = termios.tcgetattr(fd)
        new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
        new[6][TERMIOS.VMIN] = 1
        new[6][TERMIOS.VTIME] = 0
        termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
        c = None
        try:
            c = os.read(fd, 1)
        finally:
            termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
        return c


class Colours:
    red = '\33[31m'
    reset = '\33[0m'
    green = '\33[32m'
    white = '\33[37m'

class Config():
    # Define game parameters
    word_buffer_size = 10
    word_queue_count = 10

    # Define which keys are for which hand
    right_hand = set('6yhn7ujm8ik,9ol.0p;:/?<>-[\'\"=]()*&^')
    left_hand = set('1qaz2wsx3edc4rfv5tgb%$#@!')
    all_characters = right_hand | left_hand

# Convenience function
def clear():
    if sys.platform[:3] == 'win':
        os.system('cls')
    elif sys.platform[:3] == 'lin':
        os.system("clear")

def list_files():
    # prints files in a numbered selection list and returns the file paths
    # (From what I can tell. It's been a while.)
    for index, file in enumerate(glob.glob("Texts/*.txt")):
        print('[' + str(index) + ']', file)
    return glob.glob("Texts/*.txt") # TODO: This double string thing sucks

# Reads a file into memory
def read_words_from_file(in_file):
    print('Loading', in_file + '...')
    with open(in_file) as word_file:
        valid_words = set(word_file.read().split())
    return valid_words

# Rebuilds the queue
def iterate_queue(word_list, word_queue, capitalise):
    word_queue = build_queue(word_list, capitalise)
    return word_queue

# Generates a full queue
def build_queue(word_list, capitalise, word_buffer_size = Config.word_buffer_size):
    # word buffer is empty list
    word_queue = ''
    prev_word = ''
    # get 'word_buffer_size' amount of words randomly from the main list of words
    if len(word_list) < word_buffer_size:
        amt = len(word_list)
    else:
        amt = word_buffer_size
    word_list_tuple = tuple(word_list)
    for x in range(0, amt):
        print('\rBuilding word queue... ' + str(x) + '/' + str(word_buffer_size), end='')
        while True:
            word = random.choice(word_list_tuple)
            if word != prev_word.lower:
                if(capitalise == "y"):
                    if(random.randint(0,1) > 0):
                        prev_word = word
                        word = word.capitalize()
                else:
                    if(capitalise == "a"):
                        prev_word = word
                        word = word.capitalize()
                word_queue += word + ' '
                break
    return word_queue

def init_game():
    clear()
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
    user_word = ''
    right_hand_words = set()
    left_hand_words = set()

    # get words from user selected file
    while True:
        user_input = input('>>')
        if (user_input == ""):
            exit()
        try:
            user_input = int(user_input)
            break
        except:
            print("Type the number next to one of the files or leave it empty and hit enter to exit.")
    word_list_file = file_list[user_input]
    all_words = read_words_from_file(word_list_file)
    both_hand_words = all_words

    # sorts the file into words that can be typed by the left hand or right hand.
    for x in all_words:
        if set(x).issubset(Config.left_hand):
            left_hand_count += 1
            left_hand_words.add(x)
        else:
            if set(x).issubset(Config.right_hand):
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
    print('Hit escape when playing to return to the main menu.')
    print('Close the window at any time or hit just enter while on the main menu to exit.')
    print()

    print('Would you like randomized capitalisation? [Y]es (default), [N]o, [A]lways (capitalise every word)')
    while True:
        response = input('>>').lower()
        if(response == "y" or response == "n" or response == "a"):
            capitalise = response
            break
        else:
            if(response == ""):
                capitalise = "y"
                break
        print("Enter Y, N, or A or just hit enter to auto pick yes.")
    print()

    print('Do you want [L]eft [R]ight or [B]oth (default) handed word practice?')
    while True:
        user_input = input('>>')
        if (user_input.lower() == "l"):
            print('Left hand chosen')
            wordset = left_hand_words
            break
        else:
            if (user_input.lower() == "r"):
                print('Right hand chosen')
                wordset = right_hand_words
                break
            else:
                if (user_input.lower() == "b"):
                    print('Both hands chosen')
                    wordset = both_hand_words
                    break
                else:
                    if (user_input == ""):
                        print('Both hands chosen')
                        wordset = both_hand_words
                        break
                    else:
                        print("Type L, R or B or just hit enter to auto pick 'Both'")
    start_game(wordset, capitalise)

# Game loop
def start_game(word_list, capitalise):
    restart_game = False

    # constructs the word buffer to avoid queue generation lag on large files
    word_queue = build_queue(word_list, capitalise)

    clear()
    # loops every time the user types the queue correctly
    while(True): # -- Word Loop
        if(restart_game):
            break
        typed_chars = ''
        # if len(word_buffer) <= 0:
        word_queue = iterate_queue(word_list, word_queue, capitalise)
        # loops every time the user enters a keystroke.
        # clears user word every time they complete a queue
        while(True): # -- Character Loop --------------------------------------------------------------------------
            # Print the word queue
            sys.stdout.write('\r')
            sys.stdout.write(word_queue + ' ')
            sys.stdout.flush()
            sys.stdout.write('\r')


# --        # DRAW CHARACTERS
            # loops through the displayed characters and checks if the user's characters match up,-
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


# --        # GET NEXT CHARACTER INPUT
            user_input = getKey().decode("utf-8")
            # if it's a letter or number
            if Config.all_characters.__contains__(user_input.lower()) or user_input == ' ':
                # add it to their word
                typed_chars = typed_chars + user_input
            else:
                # or if it is a backspace
                if user_input == '\x08' or user_input == '\x7f':
                    # remove one character from their word
                    typed_chars = typed_chars[:-1]
                # or if it's escape
                if user_input == '\x1b':
                    # reboot the game
                    restart_game = True
                    break
                # or if it is an enter keystroke
                if user_input == '\r' or user_input == '\n':
                    # if the user's queue is correct and ends with a space, add a line break and generate a new queue
                    sys.stdout.write('\n')
                    word_queue = build_queue(word_list, capitalise)
                    break
    init_game()

# ENTRY POINT - Set up the game
if __name__ == '__main__':
    init_game()