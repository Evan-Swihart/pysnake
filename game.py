# import the pygame module, so you can use it
import pygame

# define a main function
def main():
    
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Snake Game")
     
    # Create surface for snake and food to be drawn on
    screen = pygame.display.set_mode((500, 500))
    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    
    # Draw background
    screen.blit(background, (0, 0))

    # Update display
    pygame.display.flip()

    # Set direction variables for snake
    snake_start = 50
    snake_end = 450
    snake_x = snake_start
    snake_y = snake_start
    snake_speed = 0.05
    sx_change = 0
    sy_change = snake_speed

    # Create green square to represent snake
    snake = pygame.Surface((snake_x, snake_y))
    snake = snake.convert()
    snake_color = (0, 255, 0)
    snake = pygame.draw.rect(screen, snake_color, (snake_x, snake_y, 10, 10))

    # Set location variables for food
    food_x = 0
    food_y = 0

    # define a variable to control the main loop
    running = True

    # Set variable to determine if snake is alive
    live = True

    # main loop
    while running:
        # check if the snake has hit the edge of the screen
        if snake_x > 500 or snake_x < 0 or snake_y > 500 or snake_y < 0:
            # GAME OVER CODE
            # Set snake to dead
            live = False

            # Set snake location to middle of screen (roughly)
            snake_x = snake_end
            snake_y = snake_end
            # Set direction variables for snake
            sx_change = 0
            sy_change = 0

            # Set snake fill to black to hide it
            snake_color = (0, 0, 0)

            # Set text for "Game Over" screen
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over", 1, (255, 255, 255))
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery-15
            background.blit(text, textpos)
            # Set text for "Restart" screen
            text = font.render("Press R to restart", 1, (255, 255, 255))
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery + 15
            background.blit(text, textpos)


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

        # if snake is dead, wait for keypress to restart game
        if live == False:
            # when key is pressed, reset game
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_r]:
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

                # Hide "Game Over" and "Restart" text
                background.fill((0, 0, 0))

        # blit everything to the screen
        screen.blit(background, (0, 0))
        snake = pygame.draw.rect(screen, snake_color, (snake_x, snake_y, 10, 10))

        # update screen drawing
        pygame.display.flip()

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
    