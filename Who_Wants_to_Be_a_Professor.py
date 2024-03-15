## Linguistic Gaming with Python
## Daniel Wambach, Mary-Kate Murphy and Michelle Vuong
## "Who Wants to Be a Professor?", inspired by the game show "Who Wants to Be a Millionaire?"


# import pygame, random, sys
import pygame
import random
import sys
from pygame.locals import *

# instantiate global variable to track level progress
# starting with level 1
LEVEL = 1

# instantiate dictionaries globally, so all functions can access them
# for now, they are empty
BA_QNA = {}
MA_QNA = {}
PHD_QNA = {}

# instantiate global joker variable
# the joker is set to the value true, meaning that it is available for use
JOKER = True

pygame.init()


def display_text(surface, text, pos, box, font, color):
    """ Function that can be called, whenever text needs to be displayed on the screen. Takes the screen,
        a string and position of the text and the box that contains it, as well as a font and a colour as arguments.
        Guarantees that text is within the corresponding box and doesn't exceed the width of the box by line
        breaking if necessary. """
    collection = [word.split(" ") for word in text.splitlines()]
    space = font.size(" ")[0]
    x, y = pos
    for lines in collection:
        for words in lines:
            word_surface = font.render(words, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= (box[0] + box[1] - 20):
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]
        y += word_height


def main():
    """ Main game loop that directs to different functions based on the value in the "scene" variable. """
    # draw screen
    screen = pygame.display.set_mode((1200, 600))
    dictionary_assignment()  # instantiate the dictionaries with the corresponding function
    pygame.display.set_caption("Who Wants to Be a Professor?")
    scene = "welcome_scene"
    while True:
        if scene == "welcome_scene":
            scene = welcome(screen)
        elif scene == "play_scene":
            scene = play(screen)
        elif scene == "info_scene":
            scene = info(screen)
        elif scene == "cheat_scene":
            scene = cheat(screen)
        elif scene == "congrats_scene":
            scene = congrats(screen)
        elif scene == "losing_scene":
            scene = losing(screen)
        elif scene == "winning_scene":
            scene = winning(screen)


def welcome(screen):
    """ Function that displays the welcome screen and clickable buttons to start playing or access other screens. """
    # draw screen and boxes
    screen.fill("midnightblue")
    welcomeBox = pygame.draw.rect(screen, "mediumblue", (150, 100, 900, 200))
    # biggest box on screen position and colour
    playBox = pygame.draw.rect(screen, "mediumblue", (150, 370, 250, 75))  # play box position and colour
    infoBox = pygame.draw.rect(screen, "dodgerblue", (475, 370, 250, 75))  # info box position and colour
    cheatsheetBox = pygame.draw.rect(screen, "darkblue", (800, 370, 250, 75))  # cheatsheet box position and colour

    # loading logo picture
    welcome_png = pygame.image.load("Who_Wants_to_Be_a_Professor.jpg")  # load picture from file
    welcome_png = pygame.transform.scale(welcome_png, (
        int(welcome_png.get_width() * 0.38), int(welcome_png.get_height() * 0.38)))  # adjust the size of the picture
    screen.blit(welcome_png, (850, 100))  # draws image onto screen

    # defining the font and adding text with the display_text function
    font = pygame.font.SysFont("freesansbold.ttf", 35)
    display_text(screen, "Welcome to 'Who Wants to Be a Professor'!", (280, 190), (150, 900), font, "white")

    display_text(screen, "Play", (250, 395), (150, 250), font, "white")  # wording and its colour for play box
    display_text(screen, "Info", (570, 395), (475, 250), font, "white")  # wording and its colour for info box
    display_text(screen, "Cheatsheet", (850, 395), (800, 250), font, "white")
    # wording and its colour for cheatsheet box
    display_text(screen, "Press <Esc> to quit the game.", (150, 460), (150, 1000), font, "white")
    # informing player how to exit game

    pygame.display.update()

    while True:  # detecting where on the screen the player makes a mouse click
        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                # detection is only depending on when the player releases a click. Not the down click
                mousex, mousey = event.pos  # x and y positions of the mouse on the screen
                if playBox.collidepoint(mousex, mousey):
                    # if player releases a click and the x & y coordinates of
                    # mouse curser align with the play box position, play screen will be shown
                    scene = "play_scene"
                    return scene
                elif infoBox.collidepoint(mousex, mousey):
                    # if player releases a click and the x & y coordinates of mouse curser align with the info box
                    # position, info screen will be shown
                    scene = "info_scene"
                    return scene
                elif cheatsheetBox.collidepoint(mousex, mousey):
                    # if player releases a click and the x & y coordinates of mouse curser align with the cheatsheet
                    # box position, cheatsheet screen will be shown
                    scene = "cheat_scene"
                    return scene


def play(screen):
    """ Main play function. Displays question and answers, level and joker and checks user
    input against the solutions."""
    # enable function to alter the global JOKER variable
    global JOKER
    # question selection tracker and level tracker
    # depending on the level, different question-answer dictionaries will be used to generate increasing difficulty
    if LEVEL < 4:
        # retrieve a question and the corresponding answers with a selection function
        question, answers = ba_selection()
    elif LEVEL > 3 and LEVEL < 7:
        question, answers = ma_selection()
    elif LEVEL > 6 and LEVEL < 10:
        question, answers = phd_selection()
    else:
        winning(screen)

    # fill surface midnightblue
    screen.fill("midnightblue")
    # draw different figures on the canvas
    pygame.draw.rect(screen, "mediumblue", (75, 90, 800, 200))  # Question

    # Answer a, x-position, y-position, width, height
    answera = pygame.draw.rect(screen, "mediumblue", (75, 325, 375, 75))
    answerb = pygame.draw.rect(screen, "dodgerblue", (500, 325, 375, 75))  # Answer b
    answerc = pygame.draw.rect(screen, "dodgerblue", (75, 425, 375, 75))  # Answer c
    answerd = pygame.draw.rect(screen, "mediumblue", (500, 425, 375, 75))  # Answer d

    pygame.draw.rect(screen, "dodgerblue", (925, 50, 200, 40))  # Level 9
    pygame.draw.rect(screen, "dodgerblue", (925, 100, 200, 40))  # Level 8
    pygame.draw.rect(screen, "dodgerblue", (925, 150, 200, 40))  # Level 7
    pygame.draw.rect(screen, "mediumblue", (925, 200, 200, 40))  # Level 6
    pygame.draw.rect(screen, "mediumblue", (925, 250, 200, 40))  # Level 5
    pygame.draw.rect(screen, "mediumblue", (925, 300, 200, 40))  # Level 4
    pygame.draw.rect(screen, "darkblue", (925, 350, 200, 40))  # Level 3
    pygame.draw.rect(screen, "darkblue", (925, 400, 200, 40))  # Level 2
    pygame.draw.rect(screen, "darkblue", (925, 450, 200, 40))  # Level 1
    back = pygame.draw.rect(screen, "mediumblue", (950, 500, 150, 40))  # Back Button

    font = pygame.font.SysFont("freesansbold.ttf", 35)

    # check if joker is still available (True if yes, False if no)
    # if joker is unused, print the following object
    if JOKER is True:
        joker = pygame.draw.rect(screen, "mediumblue", (800, 30, 75, 40))  # Joker
        display_text(screen, "50/50", (810, 15), (800, 75), font, "white")  # Joker

    # if joker was used, display this on the screen instead
    if JOKER is False:
        joker = pygame.draw.rect(screen, "darkmagenta", (800, 30, 75, 40))  # Joker

    drawHighlightBox(screen)

    # adding text using the display_text function
    display_text(screen, question, (100, 150), (75, 800), font, "white")

    display_text(screen, "PhD-3", (990, 60), (925, 200), font, "white")  # Level 9
    display_text(screen, "PhD-2", (990, 110), (925, 200), font, "white")  # Level 8
    display_text(screen, "PhD-1", (990, 160), (925, 200), font, "white")  # Level 7
    display_text(screen, "MA-3", (990, 210), (925, 200), font, "white")  # Level 6
    display_text(screen, "MA-2", (990, 260), (925, 200), font, "white")  # Level 5
    display_text(screen, "MA-1", (990, 310), (925, 200), font, "white")  # Level 4
    display_text(screen, "BA-3", (990, 360), (925, 200), font, "white")  # Level 3
    display_text(screen, "BA-2", (990, 410), (925, 200), font, "white")  # Level 2
    display_text(screen, "BA-1", (990, 460), (925, 200), font, "white")  # Level 1
    display_text(screen, "back", (1000, 510), (925, 200), font, "white")  # back button

    # display the strings generated by the selection function from earlier and show them in the corresponding boxes
    display_text(screen, answers[0][0], (100, 350), (75, 375), font, "white")  # Answer a
    display_text(screen, answers[1][0], (525, 350), (500, 375), font, "white")  # Answer b
    display_text(screen, answers[2][0], (100, 450), (75, 375), font, "white")  # Answer c
    display_text(screen, answers[3][0], (525, 450), (500, 375), font, "white")  # Answer d

    pygame.display.update()

    while True:
        # keep checking for quit events
        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                # track, where user clicked
                mousex, mousey = event.pos
                # if position of mouse at mouse button release collides with back, go back to welcome screen
                if back.collidepoint(mousex, mousey):
                    scene = "welcome_scene"
                    return scene
                # if position of mouse at mouse button release collides with box of answer a, check the Boolean of
                # the corresponding answer
                # if False, show losing screen, if True (else), show congrats screen
                if answera.collidepoint(mousex, mousey):
                    if answers[0][1] is False:
                        scene = "losing_scene"
                        return scene
                    else:
                        scene = "congrats_scene"
                        return scene
                if answerb.collidepoint(mousex, mousey):
                    if answers[1][1] is False:
                        scene = "losing_scene"
                        return scene
                    else:
                        scene = "congrats_scene"
                        return scene
                if answerc.collidepoint(mousex, mousey):
                    if answers[2][1] is False:
                        scene = "losing_scene"
                        return scene
                    else:
                        scene = "congrats_scene"
                        return scene
                if answerd.collidepoint(mousex, mousey):
                    if answers[3][1] is False:
                        scene = "losing_scene"
                        return scene
                    else:
                        scene = "congrats_scene"
                        return scene
                # if joker button is clicked
                if joker.collidepoint(mousex, mousey):
                    # check whether joker is still available (hasn't been used yet) (=True)
                    if JOKER is True:
                        # get the indices of false answers
                        indices = []
                        # iterate over answers variable from selection function
                        for answer in answers:
                            if answer[1] is False:
                                indices.append(answers.index(answer))

                        # select two indices randomly and store them in the to_delete variable
                        to_delete = random.sample(indices, 2)

                        # sanity check for us during coding
                        # print(to_delete)

                        # check for each index if it will be deleted (= is in to_delete list)
                        # if index 0 is false and was selected
                        if 0 in to_delete:
                            # redraw the box of answer a to "grey-out" the false answer
                            pygame.draw.rect(screen, "darkmagenta", (75, 325, 375, 75))  # answer a
                            # grey-out the joker to show that it cannot be used again
                            pygame.draw.rect(screen, "darkmagenta", (800, 30, 75, 40))  # Joker
                            pygame.display.update()

                        if 1 in to_delete:
                            pygame.draw.rect(screen, "darkmagenta", (500, 325, 375, 75))  # answer b
                            pygame.draw.rect(screen, "darkmagenta", (800, 30, 75, 40))  # Joker
                            pygame.display.update()

                        if 2 in to_delete:
                            pygame.draw.rect(screen, "darkmagenta", (75, 425, 375, 75))  # answer c
                            pygame.draw.rect(screen, "darkmagenta", (800, 30, 75, 40))  # Joker
                            pygame.display.update()

                        if 3 in to_delete:
                            pygame.draw.rect(screen, "darkmagenta", (500, 425, 375, 75))  # answer d
                            pygame.draw.rect(screen, "darkmagenta", (800, 30, 75, 40))  # Joker
                            pygame.display.update()

                        # since the randomization of question-answer pairs happens before, we know that index 0
                        # is always answer a and so on

                        # set global joker variable to false, so it cannot be used again
                        JOKER = False

                    # if joker was used (= variable set to false)
                    if JOKER is False:
                        # nothing happens in game but a print statement can be found in the console
                        print("JOKER NOT FOUND")


def info(screen):
    """ Displays the info screen containing information about the game and how to play it.
    Adapted from https://github.com/pickry/programmingknowledge/blob/master/twolines.py"""
    screen.fill("midnightblue")
    pygame.draw.rect(screen, "mediumblue", (75, 75, 1050, 300))
    back = pygame.draw.rect(screen, "mediumblue", (975, 450, 150, 60))  # Back Button

    # adding text using the display_text-function
    font = pygame.font.SysFont("freesansbold.ttf", 35)
    display_text(screen, "This game is inspired by the game show 'Who Wants to Be a Millionaire'.\n"
                         "Instead of answering trivia questions, you will be challenged with questions from semantics. "
                         "Each time you answer a question correctly, you proceed to the next level.\n"
                         "Once you have correctly answered three Bachelor's, three Master's and three PhD questions, "
                         "you have won the game.\n"
                         "You have one 50/50 joker that eliminates two wrong answers. "
                         "Choose wisely when to use the joker, you only have one!\n"
                         "You can have a look at the Cheatsheet if you want to revise some logic knowledge.\n"
                         "Your run restarts completely once you win or answer a question incorrectly.\n"
                         "Have fun!", (100, 100), (75, 1050), font, "white")

    display_text(screen, "back", (1020, 465), (975, 150), font, "white")

    pygame.display.update()

    while True:
        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                # give option to go back to welcome screen
                if back.collidepoint(mousex, mousey):
                    scene = "welcome_scene"
                    return scene


def cheat(screen):
    """ Displays the cheatsheet screen that shows explanations and hints for logic operators. """
    screen.fill("midnightblue")
    back = pygame.draw.rect(screen, "mediumblue", (1050, 520, 100, 50))  # back button

    font = pygame.font.SysFont("freesansbold.ttf", 35)
    display_text(screen, "back", (1070, 530), (1100, 100), font, "white")

    # load cheatsheet picture and display it
    cheatsheet = pygame.image.load("Cheatsheet.jpg")
    cheatsheet = pygame.transform.scale(cheatsheet,
                                        (int(cheatsheet.get_width() * 0.95), int(cheatsheet.get_height() * 0.95)))
    screen.blit(cheatsheet, (200, 5))  # draws image onto screen

    pygame.display.update()

    while True:
        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if back.collidepoint(mousex, mousey):
                    scene = "welcome_scene"
                    return scene


def losing(screen):
    """ Function that displays the losing screen, appearing when the user got an answer wrong. """
    # after losing we need to reset the progress and the joker, which is why the function has access
    # to these global variables
    global LEVEL, JOKER
    # reset level to 1 after loosing
    LEVEL = 1
    # make joker available again
    JOKER = True

    # reassign the questions, so all are available again
    dictionary_assignment()

    screen.fill("midnightblue")
    pygame.draw.rect(screen, "mediumblue", (75, 75, 1050, 300))
    back = pygame.draw.rect(screen, "mediumblue", (975, 450, 150, 60))  # back button

    font = pygame.font.SysFont("freesansbold.ttf", 35)
    display_text(screen, "Oops! Wrong answer.", (100, 150), (75, 1050), font, "white")
    display_text(screen, "back", (1020, 467), (975, 150), font, "white")

    # inserting a picture of Günther Jauch for the loosing screen
    losing_jauch = pygame.image.load("Jauch_losing.jpg")
    losing_jauch = pygame.transform.scale(losing_jauch, (
        int(losing_jauch.get_width() * 1), int(losing_jauch.get_height() * 1)))
    screen.blit(losing_jauch, (700, 140))  # draws image onto screen

    pygame.display.update()

    while True:
        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if back.collidepoint(mousex, mousey):
                    scene = "welcome_scene"
                    return scene


def congrats(screen):
    """ Function that displays the congrats scene, which appears after a correct answer by the user. """
    # refer to global variable
    global LEVEL
    # increasing the level after a question was answered correctly
    LEVEL += 1

    screen.fill("midnightblue")
    pygame.draw.rect(screen, "mediumblue", (75, 75, 1050, 300))
    continue_on = pygame.draw.rect(screen, "mediumblue", (775, 450, 150, 60))  # Back Button
    back = pygame.draw.rect(screen, "mediumblue", (975, 450, 150, 60))  # Back Button

    font = pygame.font.SysFont("freesansbold.ttf", 35)
    display_text(screen, "Good job, correct answer.", (100, 150), (75, 1050), font, "white")
    display_text(screen, "continue", (800, 445), (775, 150), font, "white")
    display_text(screen, "back", (1020, 467), (975, 150), font, "white")

    pygame.display.update()

    while True:
        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                # continue playing
                if continue_on.collidepoint(mousex, mousey):
                    scene = "play_scene"
                    return scene
                # go back to welcome screen
                elif back.collidepoint(mousex, mousey):
                    scene = "welcome_scene"
                    return scene


def winning(screen):
    """ Function that shows the winning screen, which appears, when the user gets all 10 answers right. """
    # resetting the level and joker when player won the game, so it can be played again
    global LEVEL, JOKER
    LEVEL = 1
    JOKER = True

    # reassign the questions, so all are available again
    dictionary_assignment()

    screen.fill("midnightblue")
    pygame.draw.rect(screen, "mediumblue", (75, 75, 1050, 300))
    back = pygame.draw.rect(screen, "mediumblue", (975, 450, 150, 60))  # Back Button

    font = pygame.font.SysFont("freesansbold.ttf", 35)
    display_text(screen, "Congratulations on your PhD!", (100, 150), (75, 1050), font, "white")
    display_text(screen, "back", (1020, 467), (975, 150), font, "white")

    # load a picture of Günther Jauch smiling
    winning_jauch = pygame.image.load("Jauch_winning.jpg")
    winning_jauch = pygame.transform.scale(winning_jauch, (int(winning_jauch.get_width() * 0.7),
                                                           int(winning_jauch.get_height() * 0.7)))
    screen.blit(winning_jauch, (700, 125))  # draws image onto screen

    pygame.display.update()

    while True:
        checkForQuit()
        for event in pygame.event.get():  # event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if back.collidepoint(mousex, mousey):
                    main()


def drawHighlightBox(screen):
    """ Function that draws a highlight box and that way shows the user's current level based on the number
        of correct answers. """
    # check global level variable and draw a box around the corresponding level that the player is at
    if LEVEL == 1:
        pygame.draw.rect(screen, "darkmagenta", (925, 450, 200, 40), 4)  # Level 1 frame
    elif LEVEL == 2:
        pygame.draw.rect(screen, "darkmagenta", (925, 400, 200, 40), 4)  # Level 2 frame
    elif LEVEL == 3:
        pygame.draw.rect(screen, "darkmagenta", (925, 350, 200, 40), 4)  # Level 3 frame
    elif LEVEL == 4:
        pygame.draw.rect(screen, "darkmagenta", (925, 300, 200, 40), 4)  # Level 4 frame
    elif LEVEL == 5:
        pygame.draw.rect(screen, "darkmagenta", (925, 250, 200, 40), 4)  # Level 5 frame
    elif LEVEL == 6:
        pygame.draw.rect(screen, "darkmagenta", (925, 200, 200, 40), 4)  # Level 6 frame
    elif LEVEL == 7:
        pygame.draw.rect(screen, "darkmagenta", (925, 150, 200, 40), 4)  # Level 7 frame
    elif LEVEL == 8:
        pygame.draw.rect(screen, "darkmagenta", (925, 100, 200, 40), 4)  # Level 8 frame
    elif LEVEL == 9:
        pygame.draw.rect(screen, "darkmagenta", (925, 50, 200, 40), 4)  # Level 9 frame


def dictionary_assignment():
    """ Function that assigns the question-answer dictionaries. At different points in the game's loop,
        the dictionaries need to be reset, which this function does by reassigning the full ones to the variables"""
    global BA_QNA, MA_QNA, PHD_QNA  # accessing the global variables which allows altering them
    BA_QNA = {"Which of the following strings is not a formula in propositional logic?": [("(p ^ q)( -> q)", True),
                                                                                          ("p -> (p ^ q)", False),
                                                                                          ("((p ^ r) -> q)", False),
                                                                                          ("¬r -> q", False)],

              "Which formula is a tautology?": [("r v ¬r", True),
                                                ("r ^ q", False),
                                                ("p -> ¬r", False),
                                                ("r -> ¬q", False)],

              "What is the main operator of (p ^ ¬q) <-> (r -> (¬(p ^ ¬p)))": [("<->", True),
                                                                               ("^", False),
                                                                               ("->", False),
                                                                               ("¬", False)],

              "Which symbol represents disjunction?": [("v", True),
                                                       ("^", False),
                                                       ("->", False),
                                                       ("¬", False)],

              "Which symbol represents negation?": [("¬", True),
                                                    ("->", False),
                                                    ("<->", False),
                                                    ("^", False)],

              "Which symbol represents conjunction?": [("^", True),
                                                       ("->", False),
                                                       ("<->", False),
                                                       ("¬", False)],

              "Which symbol represents consequent?": [("->", True),
                                                      ("¬", False),
                                                      ("<->", False),
                                                      ("^", False)],

              "Which symbol represents equivalence?": [("<->", True),
                                                       ("->", False),
                                                       ("¬", False),
                                                       ("^", False)],

              "What is the symbol for a universal quantifier?": [("A", True),
                                                                 ("E", False),
                                                                 ("e", False),
                                                                 ("a", False)],

              "What is the symbol for an existential quantifier?": [("E", True),
                                                                    ("A", False),
                                                                    ("e", False),
                                                                    ("a", False)],
              }

    MA_QNA = {"Semantics is the study of ___________ meaning in language. It explores "
              "the relationships between words and their meanings, as well as how "
              "these meanings combine to form coherent sentences and convey information.": [("lexical", True),
                                                                                            ("phonological", False),
                                                                                            ("syntactic", False),
                                                                                            ("emotional", False)],

              "Which of the following allows for a more nuanced representation of "
              "relationships and quantification within statements by using variables, "
              "predicates, and quantifiers.": [("predicate logic", True), ("propositional logic", False),
                                               ("lambda calculus", False), ("algebra", False)],

              "^, v, -> , <-> in propositional logical are known as:": [("logical operators", True),
                                                                        ("connecting logicals", False),
                                                                        ("logical connectings", False),
                                                                        ("operating logicals", False)],

              "Which formula contains two bound variables?": [("Ex(Fx ^ Ax(Fxy)) ^ Ly", True), ("Fx ^ Qy", False),
                                                              ("ExFy", False), ("Ay(Fy -> Qax)", False)],

              "Which formula represents “No pilot is friendly”?": [("Ax(Px -> ¬Fx)", True), ("¬Ax(Px -> ¬Fx)", False),
                                                                   ("E(Px ^ Fx)", False), ("Ax(¬Fx)", False)],

              "Which formula represents “Every pilot has a friendly sibling”?": [("Ax(Px -> (EyFy ^ Sxy))", True),
                                                                                 ("Ax(Px ^ (EyFy ^ Sxy))", False),
                                                                                 ("Ex(Px ^ Ey(Fy ^ Sxy))", False),
                                                                                 ("Ex(Px -> Ey(Fy ^ Sxy))", False)],

              "Which formula contains two free variables?": [("Fx ^ Qy", True), ("Ay(Fy -> Qax) -> Ex(Fx v Sx)", False),
                                                             ("Ex(Fy v Qx)", False), ("Ex(Fx ^ Ax(Fxy)) ^ Ly", False)],

              "((p ^ q) -> ¬r) is a...": [("contingency", True), ("tautology", False), ("contradiction", False),
                                          ("none of the above", False)],

              "((p ^ q) -> (r ^ ¬s)) is a...": [("contingency", True), ("contradiction", False), ("tautology", False),
                                                ("none of the above", False)],

              "What propositional logic formula is said to be ‘necessarily false’ "
              "or ‘false by logical necessity’?": [("contradiction", True), ("contingency", False),
                                                   ("tautology", False), ("none of the above", False)],
              }

    PHD_QNA = {"What formula does not represent “Nobody saw nobody”?": [("¬Ex¬Ey(Sx,y)", True),
                                                                        ("¬Ax¬Ay(Sx,y)", False),
                                                                        ("AxEy(Sx,y)", False),
                                                                        ("¬ExAy(Sx,y)", False)],

               "Which formula reads “Every candidate told Mary a lie” but the lie was always different?": [
                   ("AxEy(Cx -> Ly ^ Tx,y,m)", True),
                   ("EyAx(Cx -> Ly ^ Tx,y,m)", False),
                   ("¬Ax(Cx -> EyLy ^ Tx,y,m)", False),
                   ("AxEy(Cx ^ LyTx,y,m)", False)],

               "Which formula reads “I won’t be upset if you don’t come” ?": [("¬q -> ¬p", True),
                                                                              ("¬(q -> p)", False),
                                                                              ("¬q -> p", False),
                                                                              ("q -> ¬p", False)],

               "Which is the stronger reading if p = Sue visited grandma and q = Sue visited grandpa ?": [
                   ("¬p ^ ¬q", True),
                   ("¬(p ^ q)", False),
                   ("¬¬(p -> ¬q)", False),
                   ("none of the above", False)],

               "Given Q is a formula, Q -> Ax(Wx) <-> Ax(Q -> Wx) "
               "follows the law of quantifier movement, provided that:": [("x is not free in Q", True),
                                                                          ("x is free in Q", False),
                                                                          ("Q does not contain quantifiers", False),
                                                                          (
                                                                              "Wx is not existentially quantified",
                                                                              False)],

               "The following, Ax(¬Wx) <-> ¬Ex(Wx) is an example of": [("Laws of Quantifier Negation", True),
                                                                       ("Laws of Quantifier Distribution", False),
                                                                       ("Laws of Quantifier (In)dependence", False),
                                                                       ("Laws of Quantifier Movement", False)],

               "The following, ExAy(Wx,y) -> AyEx(Wx,y) is an example of": [("Laws of Quantifier (In)dependence", True),
                                                                            ("Laws of Quantifier Distribution", False),
                                                                            ("Laws of Quantifier Negation", False),
                                                                            ("Laws of Quantifier Movement", False)],

               "The following, Ax(Wx) v Ax(Px) -> Ax(Wx v Px) is an example of": [
                   ("Laws of Quantifier Distribution", True),
                   ("Laws of Quantifier Negation", False),
                   ("Laws of Quantifier (In)dependence", False),
                   ("Laws of Quantifier Movement", False)],

               "Which formula reads “Every candidate was interviewed by Penny or by Bernadette” in its strong reading "
               "that only one did all the interview?": [
                   ("Ax (Cx -> I(p,x)) v (Ax (Cx -> I(b,x) ", True),
                   ("Ax (Cx -> I(p,x) v I(b,x))", False),
                   ("Ax (Cx -> I(x,p)) v (Ax (Cx -> I(x,b) ", False),
                   ("Ex (Cx -> I(p,x) v I(b,x))", False)],

               "Which formula reads “Lucia fed a cat that every child liked” ?": [
                   ("Ex(Cx ^ Ay(CHy -> Ly,x) ^ Fl,x))", True),
                   ("Ax((CHx ^ Ey(Cy ^ Lx,y)) -> Fl,x))", False),
                   ("Ex((CHx ^ Ey(Cy ^ Lx,y)) -> Fl,x))", False),
                   ("Ex(Cx ^ Ay(CHy -> Ly,x) -> Fl,x))", False)],
               }


def ba_selection():
    """ This function randomly selects a question and the corresponding answers from the BA dictionary
        and returns it for use in the play function. To not have duplicate questions in the game, the
        chosen key-value pair is removed from the dictionary."""
    global BA_QNA  # Calling the global variable
    question = random.choice(list(BA_QNA.keys()))
    # Converting the BA_QNA to a list in order to randomly selecting a key, i.e. question.
    answers = BA_QNA[question]
    # Retrieving the values, i.e. answers, for the exact question which was previously chosen.
    random.shuffle(answers)
    # Randomising the answers because as the boolean demonstrates, the correct one is always in the first position.
    del BA_QNA[question]
    # Removing the chosen key, i.e. question, from the dictionary, so it doesn't come up again.
    return question, answers
    # return them to be used, whenever this function is called


def ma_selection():
    """ This function randomly selects a question and the corresponding answers from the MA dictionary
        and returns it for use in the play function. To not have duplicate questions in the game, the
        chosen key-value pair is removed from the dictionary."""
    global MA_QNA
    question = random.choice(list(MA_QNA.keys()))
    # Converting the MA_QNA to a list in order to randomly selecting a key, i.e. question
    answers = MA_QNA[question]
    # Retrieving the values, i.e. answers, for the exact question which was previously chosen.
    random.shuffle(answers)
    # Randomising the answers because as the boolean demonstrates, the correct one is always in the first position.
    del MA_QNA[question]
    # Removing the chosen key, i.e. question, from the dictionary so it doesn't come up again.
    return question, answers


def phd_selection():
    """ This function randomly selects a question and the corresponding answers from the PhD dictionary
        and returns it for use in the play function. To not have duplicate questions in the game, the
        chosen key-value pair is removed from the dictionary."""
    global PHD_QNA
    question = random.choice(list(PHD_QNA.keys()))
    # Converting the PHD_QNA to a list in order to randomly selecting a key, i.e. question
    answers = PHD_QNA[question]
    # Retrieving the values, i.e. answers, for the exact question which was previously chosen.
    random.shuffle(answers)
    # Randomising the answers because as the boolean demonstrates, the correct one is always in the first position.
    del PHD_QNA[question]
    # Removing the chosen key, i.e. question, from the dictionary, so it doesn't come up again.
    return question, answers


def checkForQuit():
    """ Function that tracks quit events from the user, either by pressing the escape button or by
        clicking the "x" on the top right of the screen. """
    # terminates the program if there are any QUIT or escape key events.
    for event in pygame.event.get(QUIT):  # get all the QUIT events
        pygame.quit()  # terminate if any QUIT events are present
        sys.exit()
    for event in pygame.event.get(KEYUP):  # get all the KEYUP events
        if event.key == K_ESCAPE:
            pygame.quit()  # terminate if the KEYUP event was for the Esc key
            sys.exit()
        pygame.event.post(event)  # put the other KEYUP event objects back


if __name__ == "__main__":
    main()
