# import the pygame module, mouse, and random module
import random
import pygame.mouse
import pygame

# define a main function
def main():
    
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Snake Game")

    global font
    font = pygame.font.Font(None, 30)
    # function to draw text on screen
    def write(text,location,color=(255,255,255)):
        screen.blit(font.render(text,True,color),location)

    
     
    # Create surface for snake and food to be drawn on
    screen_size = 500
    score_size = 100
    screen = pygame.display.set_mode((screen_size + score_size, screen_size))
    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    
    # Draw background
    screen.blit(background, (0, 0))

    # Create gray background for score and change difficulty section
    score_background = pygame.Surface((screen.get_width() - screen_size, screen_size))
    score_background = score_background.convert()
    score_background.fill((150, 150, 150))
    screen.blit(score_background, (screen_size, 0))

    # Update display
    pygame.display.flip()

    # Set food and snake size
    size = 10

    # Set direction variables for snake
    snake_start = 50
    snake_end = screen_size - 50
    snake_x = snake_start
    snake_y = snake_start
    snake_speed = 0.03
    sx_change = 0
    sy_change = snake_speed

    # Create green square to represent snake
    snake = pygame.Surface((snake_x, snake_y))
    snake = snake.convert()
    snake_color = (0, 255, 0)
    snake = pygame.draw.rect(screen, snake_color, (snake_x, snake_y, size, size))

    # Set location variables for food to be randomly generated
    food_spawn = screen_size - size
    food_x = random.randint(0, food_spawn)
    food_y = random.randint(0, food_spawn)

    # Create red square to represent food
    food = pygame.Surface((food_x, food_y))
    food = food.convert()
    food_color = (255, 0, 0)
    food = pygame.draw.rect(screen, food_color, (food_x, food_y, size, size))

    # Create score variable
    score = 0

    # Create score increment variable
    score_increment = 1

    # Create difficulty variable
    difficulty = 1
    
    # define a variable to control the main loop
    running = True

    # Set variable to determine if snake is alive
    global live
    live = True

    # function to restart game
    def restartgame():
        # Set snake to alive
        live = True

        # Set snake location to almost top left
        snake_x = snake_start
        snake_y = snake_start

        # Set direction variables for snake
        sx_change = 0
        sy_change = snake_speed

        # Set snake fill to green
        snake_color = (0, 255, 0)

        # Set food location to random
        food_x = random.randint(0, food_spawn)
        food_y = random.randint(0, food_spawn)
        # Set food color to red again
        food_color = (255, 0, 0)

        # Set score to 0
        score = 0

        # Set random location for food
        food_x = random.randint(0, screen_size)
        food_y = random.randint(0, screen_size)

        # Hide "Game Over" and "Restart" text
        background.fill((0, 0, 0))
        

    # main loop
    while running:
        # check if the snake has hit the edge of the screen
        if snake_x > screen_size - size or snake_x < 0 or snake_y > screen_size - size or snake_y < 0:
            # GAME OVER CODE
            # Set snake to dead
            live = False

            # Set snake location to hidden location
            snake_x = snake_end
            snake_y = snake_end
            food_x = snake_end
            food_y = snake_end

            # Set direction variables for snake
            sx_change = 0
            sy_change = 0

            # Set snake fill & food fill to black to hide them
            snake_color = (0, 0, 0)
            food_color = (0, 0, 0)

        # if snake is alive, play game
        if live == True:
            # change direction of snake based on keypress
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP] or pressed[pygame.K_w]:
                sx_change = 0
                sy_change = -snake_speed
            elif pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
                sx_change = 0
                sy_change = snake_speed
            elif pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
                sx_change = -snake_speed
                sy_change = 0
            elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
                sx_change = snake_speed
                sy_change = 0

            # update snake location
            snake_x += sx_change
            snake_y += sy_change

            # if snake eats food, increase score and move food to random location
            if snake.colliderect(food):
                score += score_increment
                food_x = random.randint(0, food_spawn)
                food_y = random.randint(0, food_spawn)

            # if button is clicked on screen by mouse, change difficulty
            mouse_pressed = pygame.mouse.get_pressed()
            # if mouse_pressed[0]:
                # Check if mouse is clicked on the button
                # if pygame.Rect(screen_size + 10, 205, 80, 30).collidepoint(pygame.mouse.get_pos()):
                #     difficulty = 1
                # # Check if mouse is clicked on medium button
                # if pygame.Rect(screen_size + 10, 255, 80, 30).collidepoint(pygame.mouse.get_pos()):
                #     difficulty = 2
                # # Check if mouse is clicked on hard button
                # if pygame.Rect(screen_size + 10, 305, 80, 30).collidepoint(pygame.mouse.get_pos()):
                #     difficulty = 3
                # restartgame()

        # if snake is dead, wait for keypress to restart game
        if live == False:
            # when key is pressed, reset game
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_r]:
                # restartgame()
                # Set snake to alive
                live = True

                # Set snake location to almost top left
                snake_x = snake_start
                snake_y = snake_start

                # Set direction variables for snake
                sx_change = 0
                sy_change = snake_speed

                # Set snake fill to green
                snake_color = (0, 255, 0)

                # Set food location to random
                food_x = random.randint(0, food_spawn)
                food_y = random.randint(0, food_spawn)
                # Set food color to red again
                food_color = (255, 0, 0)

                # Set score to 0
                score = 0

                # Set random location for food
                food_x = random.randint(0, screen_size)
                food_y = random.randint(0, screen_size)

                # Hide "Game Over" and "Restart" text
                background.fill((0, 0, 0))

        # blit everything to the screen
        screen.blit(background, (0, 0))

        # if live, draw score and change difficulty section
        # blit score background
        screen.blit(score_background, (screen_size, 0))

        # Set text for score
        write("Score: " + str(score), (screen_size + 10, 10))

        # Set text for change difficulty
        write("Change", (screen_size + 10, 150))
        write("Difficulty", (screen_size + 5, 175))

        # Draw difficulty buttons
        # Easy
        pygame.draw.rect(screen, (0, 255, 0), (screen_size + 10, 205, 80, 30))
        write("Easy", (screen_size + 27, 211), (0, 0, 0))

        # Medium
        pygame.draw.rect(screen, (255, 255, 0), (screen_size + 10, 255, 80, 30))
        write("Medium", (screen_size + 12, 261), (0, 0, 0))

        # Hard
        pygame.draw.rect(screen, (255, 0, 0), (screen_size + 10, 305, 80, 30))
        write("Hard", (screen_size + 27, 311), (0, 0, 0))
        if live == False:
            # Set text for "Game Over" screen
            write("Game Over", (screen_size/2 - 55, screen.get_height()/2 - 50))
            # Set text for "Restart" screen
            write("Press R to restart", (screen_size/2 - 80, screen.get_height()/2))



        # draw food and snake
        food = pygame.draw.rect(screen, food_color, (food_x, food_y, 10, 10))
        snake = pygame.draw.rect(screen, snake_color, (snake_x, snake_y, 10, 10))


        # update screen drawing
        pygame.display.update()

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
    