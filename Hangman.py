import check
class Hangman:
  '''
  Fields:
     secret_word (Str)
     in_progress_word (Str)
     guessed_letter_hits (listof Str)
     guessed_letter_misses (listof Str)
     
     Requires: 
        in_progress_word and secret_word correspond to a valid Hangman pair
        guessed_letter_hits and guessed_letter_misses 
             contain only capital letters
        len(guessed_letter_misses) <= Hangman.max_strikes
  '''
    
  ##These are constants for your Hangman class.
  ##Reference by calling for example 
  ##Hangman.max_strikes or Hangman.max_word
  
  max_strikes = 6
  max_word = 1000
  enter_game_number = \
  "Please enter a valid game number between 1 and {0}: ".format(max_word)
  invalid_game_number = "Error, the number entered was not valid."
  letter_prompt = "Please enter a letter: "
  not_a_letter = "The character {0} is not a letter."
  already_guessed_letter = \
  "You have already guessed the letter {0}. Please enter another letter."
  not_in_word = "The letter {0} is not in the word."
  not_last_guess = \
  "Watch out! You only have {0} more guesses left before your man is hung!"
  play_again = "Do you want to play again? (Y for yes, N for no)."
  invalid_play_again_response = "Error, invalid response."
  game_over = "Game over. The correct word was {0}."
  congratulations = "You win! The correct word was {0}."
  
  def __init__(self, word_number):
    self.secret_word = self.get_word(word_number)
    self.in_progress_word = ("_" * len(self.secret_word))
    self.guessed_letter_hits = []
    self.guessed_letter_misses = []
  
  def __repr__(self):
    '''
    Returns a string representation of self
  
    __repr__: Hangman -> Str
    '''
    fin = open("hangman_board.txt")
    L = fin.readlines()
    fin.close()
    start = len(self.guessed_letter_misses)
    board_length = 15
    return "".join(L[start*board_length:start*board_length+board_length])
  
  def __eq__(self, other):
    return isinstance(other, Hangman) and\
    self.secret_word == other.secret_word and\
    self.in_progress_word == other.in_progress_word and\
    self.guessed_letter_hits == other.guessed_letter_hits and\
    self.guessed_letter_misses == other.guessed_letter_misses
    
  def get_word(self, n):
    '''
    Returns a secret word corresponding to entry n in a list.
  
    get_word: Nat -> Str
    Requires: 1 <= n <= Hangman.max_word
    '''
    fin = open("words.txt")
    L = fin.readlines()
    fin.close()
    return L[n].strip()
    
  def update_board(self, guess):
    if guess not in self.secret_word:
      self.guessed_letter_misses.append(guess)
    else:
      i = 0
      Lsecret = list(self.secret_word)
      Lin_progress = list(self.in_progress_word)
      while i < len(Lsecret):
        if guess == Lsecret[i]:
            Lin_progress[i] = guess
        i += 1
      self.in_progress_word = "".join(Lin_progress)
      self.guessed_letter_hits.append(guess)
      
    def game_over(self):
    if len(self.guessed_letter_misses) >= self.max_strikes:
      print("Game over. The correct word was {0}.".format(self.secret_word))
      return True
    if self.secret_word == self.in_progress_word:
      print("You win! The correct word was {0}.".format(self.secret_word))
      return True
    else:
      return False

def play_game():
  '''#Part I: Choose a word from the list:
     Reads in a string,game_number, guees and play_again from the keyboard and 
     prints a message about 
     Effects: Mutates guess
     play_game: None -> None
     '''
  #Choose a word from the list:
  game_number = input(Hangman.enter_game_number)
  while not(game_number.isnumeric()):
    print(Hangman.invalid_game_number)
    game_number = input(Hangman.enter_game_number)
  
  while not(int(game_number) >= 0 and int(game_number) < 1000):
    game_number = input(Hangman.enter_game_number)
    if game_number.isnumeric(): 
      if not(int(game_number) >= 0 and int(game_number) < 1000):
        print(Hangman.invalid_game_number)
  game = Hangman(int(game_number))
  print(game)
  print(game.in_progress_word)
  
  # Guessing the word:
  hits = game.guessed_letter_hits 
  misses = game.guessed_letter_misses
  while not game.game_over():
    guess = input(Hangman.letter_prompt)
    if guess.isalpha():
      if guess.islower():
        guess = guess.upper()
      if guess.isupper():
        if guess in game.secret_word and guess not in hits: 
          game.update_board(guess)
        elif guess not in game.secret_word and guess not in misses:
          game.update_board(guess)
          print(Hangman.not_in_word.format(guess))
          print(Hangman.not_last_guess.format(Hangman.max_strikes-len(misses)))
        else:
          print(Hangman.already_guessed_letter.format(guess))
        print(game)
        print(game.in_progress_word)
    else:
      print(Hangman.not_a_letter.format(guess))
      
    #Replay?
  play_again = ""
  while play_again is not "N":
    play_again = input(Hangman.play_again)
    if play_again.isalpha():
      if play_again is "Y":
        return play_game()
    else:
      print(Hangman.invalid_play_again_response)

'''Test:'''
check.set_input("comet","10","z","d","e","l","A","Y","1","N")
check.set_screen("Prints Hangman.invalid_game_number")
check.set_screen("Prints Hangman Object for each input")
check.set_screen("Prints in_progress Field for each input")
check.set_screen("You win! The correct word was DELAY.for last input")
check.set_screen("Error, invalid response.")
check.expect("Example 1", play_game(), None)

'''Test_for_init:'''
##Testing __init__
ZERO = Hangman(0) 

check.expect("Testing Zero secret word", ZERO.secret_word, "ZERO")
check.expect("Testing Zero in progress word", ZERO.in_progress_word, "____")
check.expect("Testing Zero guessed letter hits", ZERO.guessed_letter_hits, [])
check.expect("Testing Zero guessed letter misses", ZERO.guessed_letter_misses,[])
