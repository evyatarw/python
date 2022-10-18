
# welcom message
HANGMAN_ASCII_ART = """
""" + PURPLE + """  _    _                                         
 | |  | |                                        
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |                      
                     |___/""" + END_CLR
MODE_0 = """x-------x
"""
MODE_1 = """x-------x
|
|
|
|
|
"""
MODE_2 = """x-------x
|       |
|       0
|
|
|
"""
MODE_3 = """x-------x
|       |
|       0
|       |
|
|
"""
MODE_4 = """x-------x
|       |
|       0
|      /|\\
|
|
"""
MODE_5 = """x-------x
|       |
|       0
|      /|\\
|      /
|
"""
MODE_6 = """x-------x
|       |
|""" + RED + """       0""" + END_CLR + """
|""" + RED + """      /|\\""" + END_CLR + """
|""" + RED + """      / \\""" + END_CLR + """
|
"""
HANGMAN_PHOTOS = {0: MODE_0, 1: MODE_1, 2: MODE_2, 3: MODE_3, 4: MODE_4
    , 5: MODE_5, 6: MODE_6}
RED = '\x1b[5;31;40m'
PINK = '\x1b[1;31;40m'
PURPLE = '\x1b[0;35;40m'
GREEN = '\x1b[1;32;40m'
GREY = '\x1b[1;30;40m'
LINEN = '\x1b[4;37;40m'
GREEN_MARK = '\x1b[0;30;42m'
RED_MARK = '\x1b[0;30;41m'
END_CLR = '\x1b[0m'

# define maximum tries
MAX_TRIES = 6

def print_slow(string, hold=0, enter=1, bit=0.03):
    """
    print slow
    :param string: string to print
    :type string: str
    :rtype: None
    """
    import sys,time
    for letter in string:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(bit)
    if enter: print('')
    time.sleep(hold)

def print_sad_smiley():
    import time
    screen_clear()
    sad_face = RED + """
     .-''''''-.
   .'          '.
  /   O      O   \ 
 :           `    :
 :    .------.    :
  \  '        '  / """ + END_CLR
    cry_mouth = RED + "   \  '------'  /   " + END_CLR
    print(sad_face)
    time.sleep(0.2)
    for i in [1, 2, 3]:
        print('\r' + cry_mouth, end='')
        time.sleep(0.4)
        print("\r                ", end='')
        time.sleep(0.4)
    screen_clear()

def print_happy_smiley():
    import time
    screen_clear()
    print(GREEN + """

      _.-'''''-._
    .'  _     _  '.
   /   (_)   (_)   \ 
  :  ,           ,  :
  :  \`.       .`/  :
   \  '.`'""'"`.'  / 
    '.  `'---'`  .'
      '-._____.-' """ + END_CLR)
    time.sleep(0.5)
    screen_clear()

def print_welcom_message():
    print_slow("Welcome to the game Hangman", 0.2)
    print(HANGMAN_ASCII_ART + "\n" + GREY + 'Max Tries = ' + str(MAX_TRIES) + END_CLR + '\n')
    from time import sleep
    sleep(2)

def screen_clear(sec=0):
    """
    hold a few seconds and clear the screen
    :param sec: seconds to hold
    :type sec: float
    :rtype: None
    """
    import os
    from time import sleep
    sleep(sec)
    if os.name == 'posix':  # for mac and linux
        _ = os.system('clear')
    else:                   # for windows platfrom
        _ = os.system('cls')

def check_valid_input(letter_guessed, old_letters_guessed):
    """
    check if the input is a singel alpha-beta char, and if it a new guess
    :param letter_guessed: letter checked
    :param old_letters_guessed: letters of old guesses
    :type letter_guessed: str
    :type old_letters_guessed: list
    :rtype: bool
    """
    return (len(letter_guessed) == 1) and (letter_guessed.isalpha())
        and not(letter_guessed.lower() in old_letters_guessed)

def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """
    if the input is valid - insert it to old_letters_guessed
    :param letter_guessed: letter checked
    :param old_letters_guessed: letters of old guesses
    :type letter_guessed: str
    :type old_letters_guessed: list
    :rtype: bool
    """
    if check_valid_input(letter_guessed, old_letters_guessed):
        return True
    print(RED + "X" + END_CLR)
    print_slow((GREY + " -> " + END_CLR).join(sorted(old_letters_guessed))
        , 0, 1, 0.008)
    return False

def show_hidden_word(secret_word, old_letters_guessed):
    """
    show the hidden word ("_ _ _") with the currect letters guessed ("_ e _")
    :param secret_word: the secret word the player should guess
    :param old_letters_guessed: letters of old guesses
    :type secret_word: str
    :type old_letters_guessed: list
    :rtype: str
    """
    result = ''
    for char in secret_word:
        if char in old_letters_guessed:
            result += char + ' '
        elif char == ' ':
            result += '   '
        else: result += '_ '
    return result[:-1]

def get_guess(num_of_tries, secret_word, old_letters_guessed):
    """
    get letter from the player and if it is a currect letter print the secret word,
    if the letter not in the secret word print the hangman mode
    :param num_of_tries: number of wrong trys
    :param secret_word: the secret word the player should guess
    :param old_letters_guessed: letters of old guesses
    :type num_of_tries: int
    :type secret_word: str
    :type old_letters_guessed: list
    :rtype: tuple
    """
    print_slow("Guess a letter:  ", 0, 0)
    letter_guessed = input()
    if try_update_letter_guessed(letter_guessed, old_letters_guessed):
        old_letters_guessed += [letter_guessed]
        if not letter_guessed in secret_word:
            num_of_tries += 1
            print_sad_smiley()
            print(HANGMAN_PHOTOS[num_of_tries])
        else:
            print_happy_smiley()
            print(HANGMAN_PHOTOS[num_of_tries])
        print_slow('\n' + show_hidden_word(secret_word, old_letters_guessed), 0, 1, 0.01)
    return (num_of_tries, old_letters_guessed)

def check_win(secret_word, old_letters_guessed):
    """
    check if the player guessed all the secret word letters
    :param secret_word: the secret word the player should guess
    :param old_letters_guessed: letters of old guesses
    :type secret_word: str
    :type old_letters_guessed: list
    :rtype: bool
    """
    for char in secret_word:
        if char not in old_letters_guessed:
            if char != ' ': return False
    return True
    
def create_defult_list_of_words():
    return ["python", "programming", "game", "bug"
        , "you win", "great job", "find me", "brilliant"]

def file_to_list_of_words(file_path):
    """
    get file adress of words list and return a ditincted list of the words in the file
    :param file_path: file adress of words list (spareted by spaces onley)
    :type file_path: str
    :rtype: list
    """
    import os.path
    import sys,time
    if os.path.isfile(file_path):
        file_of_words = open(file_path, 'r')
        list_of_words = file_of_words.read().split()
        ditincted_list_of_words = []
        for i in range(len(list_of_words)):
            if list_of_words[i] not in ditincted_list_of_words:
                ditincted_list_of_words += [list_of_words[i]]
    else: # if The file does not exist
        print_slow(RED + "\nERROR!\n" + END_CLR
            + PINK + "The file path is not correct. " + END_CLR
            + "you can get the defult words"
            + ".\nDo you want to enter it again? "
            + GREY + "(press 'yes' or 'no') " + END_CLR, 0, 0)
        enter_again = input()
        if enter_again == "yes":
            print_slow("Please enter the "
                + LINEN + "fixed" + END_CLR + " file path: ", 0, 0)
            file_path = input()
            if os.path.isfile(file_path):
                list_of_words = file_to_list_of_words(file_path)
            else:
                print_slow(PINK + "\nThe file path is not correct again... " + END_CLR
                    + "So we enter the defult words.\n")
                time.sleep(1)
                list_of_words = create_defult_list_of_words()
        else:
            print_slow("\nSo we enter the defult words!")
            time.sleep(1)
            list_of_words = create_defult_list_of_words()
    return list_of_words

def choose_word(file_path, index):
    """
    get file adress of words list and index of wished word
    and return the word at the index input
    :param file_path: file adress of words list (spareted by spaces onley)
    :param index: index of wished word
    :type file_path: str
    :type index: int
    :rtype: str
    """
    if file_path == '_n':
        list_of_words = create_defult_list_of_words()
        return list_of_words[(index - 1) % len(list_of_words)]
    list_of_words = file_to_list_of_words(file_path)
    return list_of_words[(index - 1) % len(list_of_words)]

def str_to_num(string):
    """
    get string and convert it to int. if it cause an error, return random number
    :param string: string of number
    :type string: str
    :rtype: int
    """
    try:
        return int(string)
    except:
        import random
        print_slow(RED + "\nERROR!\n" + END_CLR
            + PINK + "The index you entered is not valid." + END_CLR + " you will get a random index.")
        return random.randint(1, 100)

def finish_peinting(num_of_tries, secret_word, old_letters_guessed):
    """
    print finish message
    :param file_path: file adress of words list (spareted by spaces onley)
    :param index: index of wished word
    :type file_path: str
    :type index: int
    :rtype: tuple
    """
    if check_win(secret_word, old_letters_guessed):
        if num_of_tries == 0:
            print(GREEN + """
░█████╗░███╗░░░███╗░█████╗░███████╗██╗███╗░░██╗░██████╗░██╗
██╔══██╗████╗░████║██╔══██╗╚════██║██║████╗░██║██╔════╝░██║
███████║██╔████╔██║███████║░░███╔═╝██║██╔██╗██║██║░░██╗░██║
██╔══██║██║╚██╔╝██║██╔══██║██╔══╝░░██║██║╚████║██║░░╚██╗╚═╝
██║░░██║██║░╚═╝░██║██║░░██║███████╗██║██║░╚███║╚██████╔╝██╗
╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝╚══════╝╚═╝╚═╝░░╚══╝░╚═════╝░╚═╝""" + END_CLR)
        elif num_of_tries == 1:
            print(GREEN + """
░██╗░░░░░░░██╗██╗███╗░░██╗███╗░░██╗███████╗██████╗░
░██║░░██╗░░██║██║████╗░██║████╗░██║██╔════╝██╔══██╗
░╚██╗████╗██╔╝██║██╔██╗██║██╔██╗██║█████╗░░██████╔╝
░░████╔═████║░██║██║╚████║██║╚████║██╔══╝░░██╔══██╗
░░╚██╔╝░╚██╔╝░██║██║░╚███║██║░╚███║███████╗██║░░██║
░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝""" + END_CLR)
        elif 1 < num_of_tries <= 3:
            print(GREEN + """

──────────────────────────────────────────────────────────
─██████──────────██████─██████████─██████──────────██████─
─██░░██──────────██░░██─██░░░░░░██─██░░██████████──██░░██─
─██░░██──────────██░░██─████░░████─██░░░░░░░░░░██──██░░██─
─██░░██──────────██░░██───██░░██───██░░██████░░██──██░░██─
─██░░██──██████──██░░██───██░░██───██░░██──██░░██──██░░██─
─██░░██──██░░██──██░░██───██░░██───██░░██──██░░██──██░░██─
─██░░██──██░░██──██░░██───██░░██───██░░██──██░░██──██░░██─
─██░░██████░░██████░░██───██░░██───██░░██──██░░██████░░██─
─██░░░░░░░░░░░░░░░░░░██─████░░████─██░░██──██░░░░░░░░░░██─
─██░░██████░░██████░░██─██░░░░░░██─██░░██──██████████░░██─
─██████──██████──██████─██████████─██████──────────██████─
──────────────────────────────────────────────────────────""" + END_CLR)
        elif 4 <= num_of_tries:
            print(GREEN + """

██╗░░░██╗░█████╗░██╗░░░██╗  ██████╗░██╗██████╗░  ██╗████████╗
╚██╗░██╔╝██╔══██╗██║░░░██║  ██╔══██╗██║██╔══██╗  ██║╚══██╔══╝
░╚████╔╝░██║░░██║██║░░░██║  ██║░░██║██║██║░░██║  ██║░░░██║░░░
░░╚██╔╝░░██║░░██║██║░░░██║  ██║░░██║██║██║░░██║  ██║░░░██║░░░
░░░██║░░░╚█████╔╝╚██████╔╝  ██████╔╝██║██████╔╝  ██║░░░██║░░░
░░░╚═╝░░░░╚════╝░░╚═════╝░  ╚═════╝░╚═╝╚═════╝░  ╚═╝░░░╚═╝░░░""" + END_CLR)
    else:
        letters_left = []
        for letter in secret_word:
            if (not letter in old_letters_guessed) and (not letter in letters_left):
                letters_left += [letter]
        if len(letters_left) > 1:
            print(RED + """
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█▄─▄███─▄▄─█─▄▄▄▄█▄─▄▄─█
██─██▀█─██─█▄▄▄▄─██─▄█▀█
█▄▄▄▄▄█▄▄▄▄█▄▄▄▄▄█▄▄▄▄▄█""" + END_CLR)
        elif len(letters_left) == 1:
            print(RED + """
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█─▄▄▄▄█─▄▄─███─▄▄▄─█▄─▄███─▄▄─█─▄▄▄▄█▄─▄▄─███████
█▄▄▄▄─█─██─███─███▀██─██▀█─██─█▄▄▄▄─██─▄█▀███████
█▄▄▄▄▄█▄▄▄▄███▄▄▄▄▄█▄▄▄▄▄█▄▄▄▄█▄▄▄▄▄█▄▄▄▄▄█▄█▄█▄█""" + END_CLR)

def main():
    screen_clear()
    print_welcom_message()
    
    # get the secret word
    print_slow("Do you want to enter file path of list of words? " + GREY + "(press 'yes' or 'no') " + END_CLR,
        0, 0)
    if input() in ["yes", "y"]:
        print_slow("Please enter a file path of text file with words:", 0, 0)
        file_path = input()
        print_slow("O.K. now enter index of word (for the secret word):", 0, 0)
        index = input()
        secret_word = choose_word(file_path, str_to_num(index))
    else: 
        import random
        secret_word = choose_word('_n', random.randint(1, 100))
    
    # start the game
    screen_clear()
    old_letters_guessed = []
    num_of_tries = 0
    print('\n' + HANGMAN_PHOTOS[num_of_tries])
    print_slow(show_hidden_word(secret_word, []))
    while ((not check_win(secret_word, old_letters_guessed)) and (num_of_tries != MAX_TRIES)):
        num_of_tries, old_letters_guessed = get_guess(num_of_tries, secret_word, old_letters_guessed)
    
    # end the game
    finish_peinting(num_of_tries, secret_word, old_letters_guessed)

if __name__ == "__main__":
    main()
