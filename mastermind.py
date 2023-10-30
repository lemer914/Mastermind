"""
Author: Lleyton Emery
CS 021
Final Project
Program description: runs an interactive game of Mastermind where
the player tries to guess the computer's code.
"""

# Import required modules
import random
import turtle

# Define constants
COLORS = ['orange', 'blue', 'green', 'purple', 'yellow', 'pink'] # Peg colors
MAX_GUESSES = 10 # Number of guesses before the player loses
SCORES = 'scores.txt' # File with all of the scores from the previous runs
NUMBER_OF_SCORES = 10 # Number of scores to display
FEEDBACK_X_START = 80 # Start drawing feedback dots from x = 80
FEEDBACK_Y_START = 120 # Start drawing feedback at y = 120
FEEDBACK_Y_SHIFT = 30 # Shift each feeback dot by this amount in the y direction
GUESS_X_START = -280 # Start drawing guess dots at x = -280
INCREMENT_RANGE = 200 # Total amount of space between all drawn dots
TITLE_HEIGHT = 250 # The height of the MASTERMIND title at the top
HEADER_X = 180 # The x avlue of the feedback header
HEADER_Y = 130 # The y value of the feedback and guesses headers
COLORS_Y = 210 # The y value of the color option dots at the top
COLORS_RANGE = 360 # The total space between the drawn color option dots
WINNING_Y_START = 70 # The y value for the start of the winning message
WINNING_Y_SHIFT = 30 # How much the winning message shifts down for each guess
WINNING_X_START = -100 # The x value for the start of the winning message
LOSING_Y = -220 # The y value for the message displayed when user loses

# Display opening messages, such as rules and the game mode the user wants
# Parameters: none. Returns: the number of pegs wide this game will be
def opening_messages():
    print('\nWelcome to Mastermind!')
    rules_choice = input('Would you like to hear the rules? (y/n) ')
    while rules_choice != 'y' and rules_choice != 'Y' and \
          rules_choice != 'n' and rules_choice != 'N':
        print('Type y if you would like to hear the rules or n if you do not,' \
              '\nthen hit Enter. Try again.')
        rules_choice = input('Would you like to hear the rules? (y/n) ')
    # if user wants the rules, display them
    if rules_choice == 'y' or rules_choice == 'Y':
        print('\nThe computer will make a color code, and you will try to ' \
              'break it!')
        print('The code and the guesses can consist of any colors in any' \
              ' arrangement, and \nrepeats are allowed.\n')
        print('For guesses, you will be prompted to input a series of colors.') 
        print('After each guess, the computer will give feedback ' \
              'using white and red pegs:')
        print('\tWhite means right color, wrong spot.')
        print('\tRed means right color, right spot.')
        print("\nThe tricky part is, you don't know which feedback peg " \
              "corresponds to which \ncolored peg that was used to guess.")
        print("So, for example, if the feedback on a guess consists of " \
              "two white pegs and\none red peg, then two of the guessed " \
              "pegs are the right color but in the wrong \nspot, one guessed " \
              "peg is the right color and is in the right spot, and one\n" \
              "guessed peg is the wrong color.")
        print('\nThe aim of the codemaker is to make an unbreakable code,\n' \
              'and the aim of the codebreaker is to break the code in time.')
        print("If the code isn't broken in 10 guesses, the codemaker wins!")
    print('The computer will make the code, and then you can start guessing!')
    print('\nWhich mode: 4 pegs wide (normal) or 6 pegs wide (hard)?')
    # get the size of the code (4 or 6 pegs)
    size = input('Press 4 for 4 pegs or 6 for 6 pegs, then hit Enter: ')
    while size != '4' and size != '6':
        print('You must type 4 for 4 pegs or 6 for 6 pegs, then hit Enter.')
        size = input('Try again: ')
    print('\nA new window will appear with the game picture, but you must use ' \
          '\nthe terminal to makes guesses, so wait for further instructions.')
    return int(size)

# Generates a random code that the user will try to break
# Parameter: how many pegs wide the code should be. Returns: the code which is
# a list of color strings
def make_code(size):
    code = [] # list to hold the code
    # get random colors and add them to the code list
    for _ in range(size):
        code.append(COLORS[random.randint(0, len(COLORS) - 1)])
    return code

# Gets a guess one color at a time by the user
# Parameters: the number of guesses the user has made and how many pegs wide the
# code is. Returns: a list of colors that is the user's guess
def get_guess(total_guesses, size):
    guess = [] # this will store the user's guess
    if MAX_GUESSES - total_guesses == 1:
        print('\nCodebreaker, this is you last guess!')
    else:
        print(f'\nCodebreaker, you have {MAX_GUESSES - total_guesses}' \
              f' guesses left.')
    print('What is your guess?')
    print('For each peg, you can guess orange, blue, green,' \
          ' purple, yellow, or pink.')
    # Ask user for a color for however big the size variable is
    for spot in range(size):
        spot_guess = input(f'Peg {spot + 1}: ')
        while spot_guess not in COLORS:
            print('Invalid color choice. Choices are orange, blue, green, ' \
                  'purple, yellow, or pink. \nTry again.')
            spot_guess = input(f'Peg {spot + 1}: ')
        guess.append(spot_guess)
    return guess

# Checks the user's guess against the code and calculates the feedback
# Parameters: the code list and the guess list. Returns: the number of pegs
# that are red and the number of pegs that are white in feedback
def check_guess(code, guess):
    right_spot = 0 # number of red pegs
    wrong_spot = 0 # number of white pegs
    taken_guess_spots = [] # once a spot has a a peg designated to it, we don't
                        # want to have to check it again
    taken_code_spots = [] # similar to the above list
    # Go through each spot where there might be a right spot right color because
    # those need to be prioritized
    for spot in range(len(guess)):
        if guess[spot] == code[spot]:
            taken_guess_spots.append(spot)
            taken_code_spots.append(spot)
            right_spot += 1
    # Check for white pegs now
    for guess_spot in range(len(guess)):
        for code_spot in range(len(code)):
            if guess_spot != code_spot and \
               guess[guess_spot] == code[code_spot] and \
               guess_spot not in taken_guess_spots and \
               code_spot not in taken_code_spots:
                wrong_spot += 1
                taken_guess_spots.append(guess_spot)
                taken_code_spots.append(code_spot)
    return right_spot, wrong_spot

# Draws the red and white feedback pegs in turtle graphics, also draws the guess
# count.
# Parameters: number of red pegs, number of white pegs, number of guesses made,
# the turtle object, and the the width of the code
# Returns: none
def draw_feedback(right_spot, wrong_spot, total_guesses, pen, size):
    increment = 0
    # Draw red pegs first, moving a bit over each time using increment
    for _ in range(right_spot):
        pen.up()
        pen.setpos(FEEDBACK_X_START + increment,
                   FEEDBACK_Y_START - FEEDBACK_Y_SHIFT * total_guesses)
        pen.down()
        draw_circle('red', 7, pen)
        # Make circles evenly spaced
        increment += INCREMENT_RANGE // (size - 1)
    # Draw white pegs next, moving a bit over each time using increment
    for _ in range(wrong_spot):
        pen.up()
        pen.setpos(FEEDBACK_X_START + increment,
                   FEEDBACK_Y_START - FEEDBACK_Y_SHIFT * total_guesses)
        pen.down()
        draw_circle('white', 7, pen)
        # Make circles evenly spaced
        increment += INCREMENT_RANGE // (size - 1)
    # Draw the number of guesses made
    pen.up()
    pen.setpos(0, FEEDBACK_Y_START - FEEDBACK_Y_SHIFT * total_guesses)
    pen.down()
    pen.write(str(total_guesses), align='center', font=('Arial', 14))

# Draws the guess dots in turtle graphics
# Parameters: the guess list, total guesses made, the turtle object, and the
# width of the code
# Returns: none
def draw_guess(guess, total_guesses, pen, size): 
    increment = 0
    # Draw the colored circles, moving them over a bit each time using
    # increment
    for i in range(len(guess)):
        pen.up()
        pen.setpos(GUESS_X_START + increment,
                   FEEDBACK_Y_START - FEEDBACK_Y_SHIFT * total_guesses)
        pen.down()
        draw_circle(guess[i], 12, pen)
        # Make circles evenly spaced
        increment += INCREMENT_RANGE // (size - 1)

# Draws a circle in turtle graphics
# Parameters: circle color, circle radius, and the turtle object
# Returns: none
def draw_circle(color, radius, pen):
    pen.fillcolor(color)
    pen.begin_fill()
    pen.circle(radius)
    pen.end_fill()

# Draw the Mastermind title and the Guesses and feedback titles at the top of
# picture.
# Parameters: the turtle object
# Returns: none
def draw_headers(pen):
    # Draw MASTERMIND at the top
    pen.up()
    pen.setpos(0, TITLE_HEIGHT)
    pen.down()
    pen.write('MASTERMIND', align='center', font=('Arial', 20))
    # Draw the Guesses header
    pen.up()
    pen.setpos(-HEADER_X, HEADER_Y)
    pen.down()
    pen.write('Guesses', align='center', font=('Arial', 16))
    # Draw the Feedback header
    pen.up()
    pen.setpos(HEADER_X, HEADER_Y)
    pen.down()
    pen.write('Feedback', align='center', font=('Arial', 16))
    pen.up()
    pen.setpos(0, 0)
    pen.down()

# Draw the dots at the top that show all of the colors that the user can guess
# with.
# Parameters: the turtle object
# Returns: None
def draw_color_options(pen):
    increment = 0
    pen.up()
    pen.setpos(0, COLORS_Y)
    pen.down()
    pen.write('Your Color Choices:', align='center', font=('Arial', 16))
    increment = 0
    # Draw the colored circles, moving them over a bit each time using
    # increment
    for color in COLORS:
        pen.up()
        pen.setpos(-HEADER_X + increment, HEADER_X)
        pen.down()
        draw_circle(color, 12, pen)
        increment += COLORS_RANGE // (len(COLORS) - 1)

# Draw the winning message if the user guessed the code
# Parameters: turtle object, the number of guesses the user has made, the code
# as a list of colors
# Returns: none
def draw_winning_message(pen, total_guesses, code):
    pen.up()
    pen.setpos(0, WINNING_Y_START - WINNING_Y_SHIFT * total_guesses)
    pen.down()
    pen.write('You Broke the Code! The Code was:', align='center',
              font=('Arial', 20))
    increment = 0
    # Draw the circles of the code, moving them over a bit each time using
    # increment
    for color in code:
        pen.up()
        pen.setpos(WINNING_X_START + increment,
                   (WINNING_Y_START - WINNING_Y_SHIFT) - \
                   WINNING_Y_SHIFT * total_guesses)
        pen.down()
        draw_circle(color, 12, pen)
        increment += INCREMENT_RANGE // (len(code) - 1)

# Draw the losing message if the user loses
# Parameters: turtle object, the code as a list of colors
# Returns: none
def draw_losing_message(pen, code):
    pen.up()
    pen.setpos(0, LOSING_Y)
    pen.down()
    pen.write('Sorry, out of guesses. The code was:', align='center',
              font=('Arial', 16))
    increment = 0
    # Draw the circles of the code, moving them over a bit each time using
    # increment
    for color in code:
        pen.up()
        pen.setpos(WINNING_X_START + increment, LOSING_Y - WINNING_Y_SHIFT)
        pen.down()
        draw_circle(color, 12, pen)
        increment += INCREMENT_RANGE // (len(code) - 1)

# Ask the user if they want to play again
# Parameters: none
# Returns: the input from the user saying if they want to play again or not
def play_again():
    again = input('Would you like to play again? (y/n): ')
    while again != 'y' and again != 'Y' and again != 'n' and again != 'N':
        print('Type y to play again or type n to quit.')
        again = input('Would you like to play again? (y/n): ')
    return again

# Ask the user if they want to be on the leaderboard. If yes, call functions to
# add their socre to the file and then display the leaderboard.
# Parameters: total number of guesses, and the width of the code
# Returns: none
def ask_leaderboard(total_guesses, size):
    leaderboard_choice = input('\nWould you like to add your initials to' \
                               ' the leaderboard? (y/n): ')
    while leaderboard_choice != 'y' and leaderboard_choice != 'Y' and \
          leaderboard_choice != 'n' and leaderboard_choice != 'N':
        print('Type y to add your inititals or type n if you '\
              'do not want to. Try again.')
        leaderboard_choice = input('\nWould you like to add your initials to' \
                               ' the leaderboard? (y/n): ')
    if leaderboard_choice == 'y' or leaderboard_choice == 'Y':
        initials = input('What are you initials (3 letters long)? ')
        while len(initials) != 3 or not initials.isalpha():
            print('Your initials should be be composed of 3 letters.' \
                  '\nTry again.')
            initials = input('What are your initials (3 letters long)? ')
        add_leaderboard(initials.upper(), total_guesses, size)
        get_top_scores()

# Add the user's score to the file of scores
# Parameters: the user's initials, the number of guesses, and the code width
# Returns: none
def add_leaderboard(initials, total_guesses, size):
    try:
        out_file = open(SCORES, 'a')
    except IOError:
        print('Error opening file')
    else:
        out_file.write(f'{initials}     Pegs: {size}     Guesses: {total_guesses}\n')
        out_file.close()
    
# Get the best ten scores for each game mode from the scores file
# Parameters: none
# Returns: none
def get_top_scores():
    easy_scores_list = []
    hard_scores_list = []
    try:
        in_file = open(SCORES, 'r')
    except IOError:
        print('Error opening file')
    else:
        try:
            for line in in_file:
                line = line.rstrip()
                if 'Pegs: 6' in line:
                    hard_scores_list.append(line)
                else:
                    easy_scores_list.append(line)
        except ValueError:
            print('Invalid data:', line)
        in_file.close()
    # Display 10 hard scores unless there are less than 10 scores to display
    best_hard_list = []
    number_of_hard_scores = NUMBER_OF_SCORES
    if len(hard_scores_list) < NUMBER_OF_SCORES:
        number_of_hard_scores = len(hard_scores_list)
    # Get the top score by going through the list of score each time and then
    # taking the best score
    for _ in range(number_of_hard_scores):
        best_hard_score = 10 # Start the best score out as 10
        best_hard_entry = ''
        for entry in hard_scores_list:
            # If the last character is 0, the score was a 10
            if int(entry[-1:]) == 0:
                score = 10
            # Else, the last character is the score
            else:
                score = int(entry[-1:])
            if score <= best_hard_score and entry not in best_hard_list:
                best_hard_entry = entry.strip()
                best_hard_score = score
        best_hard_list.append(best_hard_entry)
    # Display 10 easy scores unless there are less than 10 scores to display
    best_easy_list = []
    number_of_easy_scores = NUMBER_OF_SCORES
    if len(easy_scores_list) < NUMBER_OF_SCORES:
        number_of_easy_scores = len(easy_scores_list)
    # Get the top score by going through the list of score each time and then
    # taking the best score
    for _ in range(number_of_easy_scores):
        best_easy_score = 10 # Start the best score out as 10
        best_easy_entry = ''
        for entry in easy_scores_list:
            # If the last character is 0, the score was a 10
            if int(entry[-1:]) == 0:
                score = 10
            # Else, the last character is the score
            else:
                score = int(entry[-1:])
            if score <= best_easy_score and entry not in best_easy_list:
                best_easy_entry = entry.strip()
                best_easy_score = score
        best_easy_list.append(best_easy_entry)
    display_leaderboard(best_hard_list, best_easy_list)

# Display the best ten scores for each game mode
# Parameters: the best scores for hard mode, and the best score for easy mode
# Returns: none
def display_leaderboard(hard_scores, easy_scores):
    print('\nLEADERBOARD\n')
    print('Best scores for 4 pegs:')
    previous_score = -1 # No score can be -1, it's just a placeholder
    if len(easy_scores) == 0:
        print('No scores yet!')
    else:
        # If two scores are the same, don't display the rank for the second
        # one to show that they're tied
        for rank in range(len(easy_scores)):
            if int(easy_scores[rank][-1:]) == previous_score:
                print(f'   {easy_scores[rank]}')
            else:
                print(f'{rank + 1}. {easy_scores[rank]}')
            previous_score = int(easy_scores[rank][-1:])
    print('\nBest scores for 6 pegs:')
    previous_score = -1 # No score can be -1, it's just a placeholder
    if len(hard_scores) == 0:
        print('No scores yet!')
    else:
        # If two scores are the same, don't display the rank for the second
        # one to show that they're tied
        for rank in range(len(hard_scores)):
            if int(hard_scores[rank][-1:]) == previous_score:
                print(f'   {hard_scores[rank]}')
            else:
                print(f'{rank + 1}. {hard_scores[rank]}')
            previous_score = int(hard_scores[rank][-1:])
    print()

# Main function that stes up the game and calls other functions
# Parameters: none
# Returns: none
def main():
    size = opening_messages()
    code = make_code(size)
    game_over = False
    total_guesses = 0
    pen = turtle.Turtle()
    turtle.bgcolor('cadetblue1') # set the background color
    pen.hideturtle() # make the turtle invisible
    draw_headers(pen)
    draw_color_options(pen)
    while not game_over:
        guess = get_guess(total_guesses, size)
        total_guesses += 1
        right_spot, wrong_spot = check_guess(code, guess)
        draw_guess(guess, total_guesses, pen, size)
        draw_feedback(right_spot, wrong_spot, total_guesses, pen, size)
        if guess == code:
            if total_guesses == 1:
                print(f'The code has been broken in {total_guesses} guess!')
            else:
                print(f'The code has been broken in {total_guesses} guesses!')
            game_over = True
            draw_winning_message(pen, total_guesses, code)
            ask_leaderboard(total_guesses, size)
        elif total_guesses == MAX_GUESSES:
            print("Sorry, you're out of guesses.")
            game_over = True
            draw_losing_message(pen, code)
    again = play_again() # see if user wants to play again
    if again == 'y' or again == 'Y':
        turtle.clearscreen()
        main()
    turtle.done()
    
# Call main
if __name__ == '__main__':
    main()
    
        
        

    
