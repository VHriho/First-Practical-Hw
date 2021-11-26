# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"



def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()



def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    if set(letters_guessed) == set(secret_word):
        return True
    else:
        return False



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    list_word = []

    for i in secret_word:
        if i in letters_guessed :
            list_word.append(i)
        else:
            list_word.append('_ ')

    return ''.join(list_word)



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    list_all_letters = [x for x  in string.ascii_lowercase]

    for i in letters_guessed:
        if i in list_all_letters:
            list_all_letters.remove(i) 

    return ''.join(list_all_letters)



def hangman(secret_word):
    
    vowels = ['a', 'e', 'i', 'o', 'u']
    warnings_remaining = 3
    guesses_remaining = 6
    letters_guessed = []
    letters_not_in_word = []

    print(f'Welcome to the game Hangman!\nI am thinking of a word that is {len(secret_word)} letters long.')
    print(f'You have {warnings_remaining} warnings left.')

    while guesses_remaining != 0:

        print('-'*12)
        if is_word_guessed(secret_word, letters_guessed):
            print(f'Congratulations, you won! Your total score for this game is: {guesses_remaining * len(letters_guessed)}')
            break
        print(f'You have {guesses_remaining} guesses left.')
        print(f'Available letters: {get_available_letters(letters_guessed + letters_not_in_word)}')

        try:
            guessing = input('Please guess a letter: ').lower()
            if len(guessing) == 1:
              if guessing.isalpha() and guessing in string.ascii_lowercase:
                if guessing not in get_available_letters(letters_guessed + letters_not_in_word):
                    warnings_remaining -= 1
                    raise NameError
                elif guessing in secret_word:
                    letters_guessed.append(guessing)
                    print(f'Good guess: {get_guessed_word(secret_word, letters_guessed)}')        
                elif guessing not in secret_word:
                    letters_not_in_word.append(guessing)
                    if guessing in vowels:
                        guesses_remaining -= 2
                    else:
                        guesses_remaining -= 1
                    print(f'Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}')
              else: 
                raise TypeError      
            else: 
                raise TypeError
        except NameError:
            if warnings_remaining < 0:
                guesses_remaining -= 1
                print(f"Oops! You've already guessed that letter. You have no warnings left so you lose one guess: {get_guessed_word(secret_word, letters_guessed)}")
            else:
                print(f"Oops! You've already guessed that letter. You have {warnings_remaining} warnings left: {get_guessed_word(secret_word, letters_guessed)}")
        except TypeError:
            if warnings_remaining == 0:
                guesses_remaining -= 1
                print(f'Oops! That is not a valid letter. You have no warnings left so you lose one guess: {get_guessed_word(secret_word, letters_guessed)}')
            else:
                warnings_remaining -= 1
                print(f'Oops! That is not a valid letter. You have {warnings_remaining} warnings left: {get_guessed_word(secret_word, letters_guessed)}')

    if guesses_remaining == 0:
        print('-'*12)
        print(f'Sorry, you ran out of guesses. The word was: {secret_word}')
    


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)



# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    list_my_word = list(my_word.replace(' ', ''))
    list_other_word = list(other_word )

    if len(list_my_word) != len(list_other_word): 
        return False 
    else:  
        for i in range (len(list_my_word)):
            if list_my_word[i] != '_' and list_my_word [i] != list_other_word [i]:
                return False
        for i in range(len(list_my_word)): 
            j = i + 1 
            for j in range(len(list_my_word)):
                if list_other_word [i] == list_other_word [j] and list_my_word [i] != list_my_word [j]: 
                    return False 
    return True



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.
    '''
    coint = 0
    possible_word = [] 

    for i in wordlist:
       if match_with_gaps(my_word, i):
           coint = 1
           possible_word.append(i) 
    if coint == 0: 
        print('No matches found')
    else:  
        print('Possible word matches are: ', end = ' ')
        for i in possible_word:
            print (i, end = ' ') 
    print ('')



def hangman_with_hints(secret_word):

    vowels = ['a', 'e', 'i', 'o', 'u']
    warnings_remaining = 3
    guesses_remaining = 6
    letters_guessed = []
    letters_not_in_word = []

    print(f'Welcome to the game Hangman!\nI am thinking of a word that is {len(secret_word)} letters long.')
    print(f'You have {warnings_remaining} warnings left.')

    while guesses_remaining != 0:

        print('-'*12)
        if is_word_guessed(secret_word, letters_guessed):
            print(f'Congratulations, you won! Your total score for this game is: {guesses_remaining * len(letters_guessed)}')
            break
        print(f'You have {guesses_remaining} guesses left.')
        print(f'Available letters: {get_available_letters(letters_guessed + letters_not_in_word)}')

        try:
            guessing = input('Please guess a letter: ').lower()
            if guessing == '*':
                show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            elif len(guessing) == 1:
              if guessing.isalpha() and guessing in string.ascii_lowercase:
                if guessing not in get_available_letters(letters_guessed + letters_not_in_word):
                    warnings_remaining -= 1
                    raise NameError
                elif guessing in secret_word:
                    letters_guessed.append(guessing)
                    print(f'Good guess: {get_guessed_word(secret_word, letters_guessed)}')        
                elif guessing not in secret_word:
                    letters_not_in_word.append(guessing)
                    if guessing in vowels:
                        guesses_remaining -= 2
                    else:
                        guesses_remaining -= 1
                    print(f'Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}')
              else: 
                raise TypeError      
            else: 
                raise TypeError
        except NameError:
            if warnings_remaining < 0:
                guesses_remaining -= 1
                print(f"Oops! You've already guessed that letter. You have no warnings left so you lose one guess: {get_guessed_word(secret_word, letters_guessed)}")
            else:
                print(f"Oops! You've already guessed that letter. You have {warnings_remaining} warnings left: {get_guessed_word(secret_word, letters_guessed)}")
        except TypeError:
            if warnings_remaining == 0:
                guesses_remaining -= 1
                print(f'Oops! That is not a valid letter. You have no warnings left so you lose one guess: {get_guessed_word(secret_word, letters_guessed)}')
            else:
                warnings_remaining -= 1
                print(f'Oops! That is not a valid letter. You have {warnings_remaining} warnings left: {get_guessed_word(secret_word, letters_guessed)}')

    if guesses_remaining == 0:
        print('-'*12)
        print(f'Sorry, you ran out of guesses. The word was: {secret_word}')
    



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
