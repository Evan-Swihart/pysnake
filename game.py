# Copyright: 2023, swidude@gmail.com

"""
This is a relatively simple recreation of the game snake using pygame, which
I'm going to call snek for the rest of this file. 

Must be played on a screen with a resolution of at least 400 pixels tall,
otherwise the game will not fit on the screen. The game will automatically
adjust to the width of the screen.

Snek is played by using the arrow keys or wasd to move the snake around
the screen. The goal is to eat as many apples as possible without running into
the walls or yourself. The snake will grow in length as you eat more apples.

Snek is over when you run into the wall or yourself. The user will then
ask if they want to play again. If R is pressed, the game will restart. If not, 
the window can be closed by pressing the escape key (at any time).

The game is written in python 3.6.5 and uses pygame 1.9.3.

First, in the main function, game state variables are initialized. The game 
state dictionary is created, and the game loop is started. The game loop will
call functions to update the game state, draw the game state, and check for
user input. Game loop will continue until the escape key is pressed. 
"""

# Hide pygame support prompt
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# Import the necessary modules
import pygame
import random

# Define the main function
def main():
    # Initialize pygame
    pygame.init()

    # Load and set the logo and the window caption
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Snek")

    """ ========================== VARIABLE SETUP ========================== """
    # Get info on screen size
    info = pygame.display.Info()
    
    # Create the game surface
    screen = pygame.display.set_mode((  info.current_w, info.current_h),
                                        pygame.FULLSCREEN)

    # Set the game background and score region background
    # The play area is the entire screen except for the score region
    # The score region is 100 pixels wide on the right side of the screen
    score_size = 100
    play_area = pygame.Rect(0, 0, 
                            info.current_w - score_size, 
                            info.current_h)
    score_area = pygame.Rect(info.current_w - score_size, 0, 
                            score_size, info.current_h)
    
    play_background = pygame.Surface(play_area.size)
    play_background.convert()
    play_background.fill((0, 0, 0))
    score_backround = pygame.Surface(score_area.size)
    score_backround.convert()
    score_backround.fill((150, 150, 150))

    # Set the button region variables
    # Define button size
    button_width = score_size - 20
    button_height = button_width / 2

    # Define button locations
    button_region_x = play_area.width + ((score_area.width - button_width) / 2)
    button_region_y = (play_area.height - button_height) / 2

    # Set global font
    global font
    font = pygame.font.Font(None, 30)

    # Define size variable to draw the snake and apple based on screen size
    draw_size = int(min(play_area.size) / 40)

    # Define speed variable to move the snake based on screen size
    # The snake will move 1/2500 of the screen size per frame on easy
    # The snake will move 1/2250 of the screen size per frame on medium
    # The snake will move 1/2000 of the screen size per frame on hard
    easy_speed = min(play_area.size) / 2500
    medium_speed = min(play_area.size) / 2250
    hard_speed = min(play_area.size) / 2000
    speed = easy_speed
    # Create the game state dictionary
    game_state = {
                    "score": 0, "score_increment": 1, "difficulty": 1,
                    "snake_x": 0, "snake_y": 0, "snake_length": 0,
                    "snake_speed_x": 0, "snake_speed_y": 0, "snake_body": [],
                    "apple_x": 0, "apple_y": 0, 
                    "snake_color": (0, 255, 0), "apple_color": (255, 0, 0),
                 }
    
    # Button dictionary
    buttons = { "medium": pygame.Rect(button_region_x, button_region_y,
                                        button_width, button_height),
                "easy": pygame.Rect(button_region_x,
                                    button_region_y - button_height - 15,
                                    button_width, button_height),
                "hard": pygame.Rect(button_region_x,
                                    button_region_y + button_height + 15,
                                    button_width, button_height)
                }
    """ ========================== END VARIABLE SETUP ========================== """



    """ ========================== FUNCTIONS ========================== """
    # DRAWING FUNCTIONS
    # Define function to draw both backgrounds
    def draw_backgrounds():
        screen.blit(play_background, play_area)
        screen.blit(score_backround, score_area)

    # Define function to draw text on the screen
    def draw_text(text, location, color=(255, 255, 255)):
        screen.blit(font.render(text, True, color), location)

    # Define function to draw the score in the score region
    def draw_score():
        draw_text("Score: " + str(game_state["score"]), 
                    (play_area.width + 10, 10))

    # Define function to draw the difficulty buttons in the score region
    # Buttons are to be drawn in the center of the score region
    # Button colors are as follows:
    #   Easy:   (0, 255, 0) "Green"
    #   Medium: (255, 255, 0) "Yellow"
    #   Hard:   (255, 0, 0) "Red"
    # Buttons are roughly twice as wide as they are tall
    # Buttons are drawn with a 5 pixel black border
    # Buttons are drawn with a 5 pixel between each other
    # Buttons are drawn with a 5 pixel border between them and the edge of the
    #   score region
    # Text is drawn in the center of the button
    # Text is always drawn in a color opposite to the button color
    # Text is always drawn in all caps
    def draw_difficulty_buttons():
        # MEDUIM BUTTON
        # Draw black border around the medium button
        pygame.draw.rect(screen, (0, 0, 0),
                        pygame.Rect(button_region_x - 5, button_region_y - 5,
                                    button_width + 10, button_height + 10))
        # Draw medium button exactly in the center of the score region
        # and add to the buttons dictionary
        pygame.draw.rect(screen, (255, 255, 0), buttons["medium"])
        # Draw the text centered in the medium button
        draw_text("Medium", (button_region_x + button_width / 2 - 38,
                            button_region_y + button_height / 2 - 10),
                    (0, 0, 0))
        
        # EASY BUTTON
        # Draw black border around the easy button 5 pixels above the medium
        pygame.draw.rect(screen, (0, 0, 0),
                        pygame.Rect(button_region_x - 5, 
                                    button_region_y - button_height - 20,
                                    button_width + 10, button_height + 10))
        # Draw easy button 5 pixels above the medium button and add to the
        # buttons dictionary
        pygame.draw.rect(screen, (0, 255, 0), buttons["easy"])
        # Draw the text centered in the easy button
        draw_text("Easy", (button_region_x + button_width / 2 - 25,
                            button_region_y - button_height / 2 - 25),
                    (0, 0, 0))

        # HARD BUTTON
        # Draw black border around the hard button 5 pixels below the medium
        pygame.draw.rect(screen, (0, 0, 0),
                        pygame.Rect(button_region_x - 5,
                                    button_region_y + button_height + 10,
                                    button_width + 10, button_height + 10))
        # Draw hard button 5 pixels below the medium button and add to the
        # buttons dictionary
        pygame.draw.rect(screen, (255, 0, 0), buttons["hard"])
        # Draw the text centered in the hard button
        draw_text("Hard", (button_region_x + button_width / 2 - 25,
                            button_region_y + button_height * 3 / 2 + 5),
                    (0, 0, 0))

    # Define function to draw game over screen
    def draw_game_over():
        draw_text("Game Over", (play_area.width / 2 - 35, play_area.height / 2 - 30))
        draw_text("Press R to Restart", (play_area.width / 2 - 63, play_area.height / 2 ))
        draw_text("Press Esc to Quit", (play_area.width / 2 - 60, play_area.height / 2 + 30))

    # Define function to draw the snake
    def draw_snake():
        # Draw the head
        pygame.draw.rect(screen, game_state["snake_color"],
                        pygame.Rect(game_state["snake_x"], game_state["snake_y"],
                                    draw_size, draw_size))
        # Draw the body
        # for body_part in game_state["snake_body"]:
        #     pygame.draw.rect(screen, game_state["snake_color"],
        #                     pygame.Rect(body_part[0], body_part[1],
        #                                 draw_size, draw_size))
    
    # Define function to draw the apple
    def draw_apple():
        pygame.draw.rect(screen, game_state["apple_color"], 
                        pygame.Rect(game_state["apple_x"], game_state["apple_y"], 
                                    draw_size, draw_size))
        
    # Define function to draw everything on the screen
    def draw_screen(live):
        draw_backgrounds()
        draw_score()
        draw_difficulty_buttons()
        if live:
            draw_snake()
            draw_apple()
        else:
            draw_game_over()
        pygame.display.update()


    # GAME STATE FUNCTIONS
    # Define function to update snake position
    def update_snake():
        # Update the snake's position
        game_state["snake_x"] += game_state["snake_speed_x"]
        game_state["snake_y"] += game_state["snake_speed_y"]

        # Update the snake's body
        # game_state["snake_body"].insert(0, (game_state["snake_x"], game_state["snake_y"]))
        # if len(game_state["snake_body"]) > game_state["snake_length"]:
        #     game_state["snake_body"].pop()
        # print(game_state["snake_body"])

    # Define function to find direction by key press or by current direction
    # Returns an integer representing the direction
    # Direction key:
    #   1 = up
    #   2 = right
    #   3 = down
    #   4 = left
    #   0 = no input
    # If pressed is True, the function will return the direction based on the
    # last key press. If pressed is False, the function will return the
    # direction based on the current direction. If pressed is true, the game
    # just started and the snake is moving towards the center of the screen.
    def find_direction(pressed):
        if pressed == True:
            if game_state["snake_speed_x"] > 0:
                return 2
            elif game_state["snake_speed_x"] < 0:
                return 4
            elif game_state["snake_speed_y"] > 0:
                return 1
            elif game_state["snake_speed_y"] < 0:
                return 3
            else:
                return 4
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            return 1
        elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            return 2
        elif pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            return 3
        elif pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            return 4
        return 0
        
    # Define function to change the snake's direction
    # Steps:
    # 1. Create variable for desired direction
    # 2. Change desired direction by key press
    # 3. Change snake direction if BOTH:
    #       Desired direction is perpendicular to urrent direction
    #       AND
    #       Snake isn't making two 90 degree turns in a row without moving
    #       at least the draw size distance
    #           Last pressed direction will contain the direction and location
    #           of the last key press as a tuple
    # 4. Return the new direction as a tuple IF the snake's direction changed
    #
    # Returns a tuple containing the new direction and the snake's location,
    # or a tuple containing 0, 0, 0 if the snake's direction did not change
    #
    # Direction key:
    #   1 = up
    #   2 = right
    #   3 = down
    #   4 = left
    #   0 = no input
    # Define function to change the snake's direction
    def change_direction(pressed, last_pressed):
        # Create variable for desired direction
        desired_direction = find_direction(pressed)

        # Return nothing if the key pressed was not a direction key
        if desired_direction == 0:
            return (0, 0, 0)
        
        # Return nothing if the desired direction is not perpendicular to the
        # previous direction
        if abs(desired_direction - last_pressed[0]) % 2 == 0:
            return (0, 0, 0)
        
        # Return nothing if the snake is making two 90 degree turns in a row
        # without moving at least the draw size distance
        if abs(game_state["snake_x"] - last_pressed[1]) < draw_size and \
            abs(game_state["snake_y"] - last_pressed[2]) < draw_size:
            return (0, 0, 0)
        
        # Change the snake's direction
        if desired_direction == 1:
            game_state["snake_speed_x"] = 0
            game_state["snake_speed_y"] = -speed
        elif desired_direction == 2:
            game_state["snake_speed_x"] = speed
            game_state["snake_speed_y"] = 0
        elif desired_direction == 3:
            game_state["snake_speed_x"] = 0
            game_state["snake_speed_y"] = speed
        elif desired_direction == 4:
            game_state["snake_speed_x"] = -speed
            game_state["snake_speed_y"] = 0
        return (desired_direction, game_state["snake_x"], game_state["snake_y"])
        
    # Define function to check for collisions
    # Returns an integer representing the type of collision
    # Collision key:
    #   1 = wall
    #   2 = snake body
    #   3 = apple
    #   0 = no collision
    def check_collisions():
        # Check for collisions with the walls
        # If the snake's head is more than 25% of the draw size out of bounds,
        # return 1
        if game_state["snake_x"] < -draw_size * 25 or \
            game_state["snake_x"] > play_area.width - draw_size * 0.75 or \
            game_state["snake_y"] < -draw_size * 0.25 or \
            game_state["snake_y"] > play_area.height - draw_size * 0.75:
            return 1

        # Check for collisions with the snake's body
        for body_part in game_state["snake_body"]:
            if game_state["snake_x"] == body_part[0] and \
                game_state["snake_y"] == body_part[1]:
                return 2

        # Check for collisions with the apple. If the snake's head is within
        # 1/4 of the apple's hitbox, return 3
        if abs(game_state["snake_x"] - game_state["apple_x"]) < draw_size* 3 / 4 and \
            abs(game_state["snake_y"] - game_state["apple_y"]) < draw_size * 3 / 4:
            return 3

        return 0

    # Define function to draw new apple
    def new_apple():
        appleNear = True
        while appleNear:
            game_state["apple_x"] = random.randint(
                0, play_area.width - draw_size)
            game_state["apple_y"] = random.randint(
                0, play_area.height - draw_size)
            
            if abs(game_state["apple_x"] - game_state["snake_x"]) > 100 or \
            abs(game_state["apple_y"] - game_state["snake_y"]) > 100:
                appleNear = False

    # Define function to check for button presses
    def check_buttons(mouse_pos):

        # Check for difficulty button presses
        mouse_pos = pygame.mouse.get_pos()
        # Check for mouse clicks
        if pygame.mouse.get_pressed()[0]:
            if buttons["easy"].collidepoint(mouse_pos) and \
                game_state["difficulty"] != 1:
                speed = easy_speed
                game_state["score_increment"] = 1
                game_state["difficulty"] = 1
                new_game()
                return 1
            elif buttons["medium"].collidepoint(mouse_pos) and \
                game_state["difficulty"] != 2:
                speed = medium_speed
                game_state["score_increment"] = 2
                game_state["difficulty"] = 2
                new_game()
                return 2
            elif buttons["hard"].collidepoint(mouse_pos) and \
                game_state["difficulty"] != 3:
                speed = hard_speed
                game_state["score_increment"] = 3
                game_state["difficulty"] = 3
                new_game()
                return 3
        return 0
    
    # Define function to start a new game
    def new_game():
        # Set the necessary game state variables back to their initial values
        game_state["score"] = 0
        game_state["snake_length"] = 1
        game_state["snake_x"] = random.randint(0, play_area.width - draw_size)
        game_state["snake_y"] = random.randint(0, play_area.height - draw_size)
        game_state["snake_body"] = []
        game_state["snake_color"] = (0, 255, 0)
        game_state["apple_color"] = (255, 0, 0)

        # Find how far away the snake is from the edge of the screen
        snakeLeftDistance = game_state["snake_x"]
        snakeRightDistance = play_area.width - game_state["snake_x"]
        snakeUpDistance = game_state["snake_y"]
        snakeDownDistance = play_area.height - game_state["snake_y"]
        snakeHorizontalDistance = max(snakeLeftDistance, snakeRightDistance)
        snakeVerticalDistance = max(snakeUpDistance, snakeDownDistance)

        # Set speeds to 0 in case speed didn't reset
        game_state["snake_speed_x"] = 0
        game_state["snake_speed_y"] = 0

        # Set the snake speed to move towards the center of the screen
        if snakeHorizontalDistance > snakeVerticalDistance:
            if snakeLeftDistance > snakeRightDistance:
                game_state["snake_speed_x"] = -speed
            else:
                game_state["snake_speed_x"] = speed
        else:
            if snakeUpDistance > snakeDownDistance:
                game_state["snake_speed_y"] = -speed
            else:
                game_state["snake_speed_y"] = speed

        appleNear = True

        while appleNear:
            game_state["apple_x"] = random.randint(
                0, play_area.width - draw_size)
            game_state["apple_y"] = random.randint(
                0, play_area.height - draw_size)
            
            if game_state["apple_x"] < game_state["snake_x"] - draw_size*5 or \
            game_state["apple_x"] > game_state["snake_x"] + draw_size * 5 or \
            game_state["apple_y"] < game_state["snake_y"] - draw_size * 5 or \
            game_state["apple_y"] > game_state["snake_y"] + draw_size * 5:
                appleNear = False
        
        live = True

    # Define function to end the game
    def end_game(end_type):
        game_state["snake_x"] = 0
        game_state["snake_y"] = 0
        game_state["apple_x"] = 0
        game_state["apple_y"] = 0
        game_state["snake_speed_x"] = 0
        game_state["snake_speed_y"] = 0

        game_state["snake_color"] = (0, 0, 0)
        game_state["apple_color"] = (0, 0, 0)

        live = False
    """ ========================== END FUNCTIONS ========================== """

    
    """ ========================== GAME LOOP ========================== """
    # Define variables to control the game loop
    first = True
    running = True
    last_pressed = (0, 0, 0)
    global live
    live = True

    # Main game loop
    while running:
        # Start a new game if the program was just started
        if first:
            new_game()
            last_pressed = (find_direction(True), 
                            game_state["snake_x"], game_state["snake_y"])
            first = False

        # Check for user input
        temp = (0, 0, 0)
        pressed = pygame.key.get_pressed()

        # Check for escape key press to quit the game
        if pressed[pygame.K_ESCAPE]:
            running = False
        # Check for r key press to restart the game
        elif pressed[pygame.K_r] and live == False:
            new_game()
            live = True
        # Check for all other key presses
        else:
            temp = change_direction(pressed, last_pressed)
        if temp[0] != 0:
            last_pressed = temp

        # Check buttons
        mouse_pos = pygame.mouse.get_pos()
        temp2 = check_buttons(mouse_pos)
        if temp2 != 0:
            last_pressed = (find_direction(True), 
                            game_state["snake_x"], game_state["snake_y"])
        
        # Call update snake function
        update_snake()

        # Check for collisions, and update the game state accordingly
        collision = check_collisions()
        if collision == 1:
            first = True
            live = False
            end_game(1)
        # elif collision == 2:
            # first = True
            # live = False
            # end_game(2)
        elif collision == 3:
            game_state["score"] += game_state["score_increment"]
            game_state["snake_length"] += 1
            new_apple()

        # Draw the screen
        draw_screen(live)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    """ ========================== ENDGAME LOOP ========================== """

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
    