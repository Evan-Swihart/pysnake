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
    snake_x = 0
    snake_y = 0
    sx_change = 0
    sy_change = 0.05

    # Create green square to represent snake
    snake = pygame.Surface((snake_x, snake_y))
    snake = snake.convert()
    snake.fill((0, 255, 0))
    snake = pygame.draw.rect(screen, (0, 255, 0), (snake_x, snake_y, 10, 10))

    # Draw snake
    # screen.blit(snake, (snake_x, snake_y))

    # Set location variables for food
    food_x = 0
    food_y = 0

    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:
        # check if the snake has hit the edge of the screen
        if snake_x > 500 or snake_x < 0:
            # Show "Game Over" screen
            print("Game Over")
            running = False
        if snake_y > 500 or snake_y < 0:
            # Show "Game Over" screen
            print("Game Over")
            running = False

        # change direction of snake based on keypress
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            sx_change = 0
            sy_change = -0.05
        elif pressed[pygame.K_DOWN]:
            sx_change = 0
            sy_change = 0.05
        elif pressed[pygame.K_LEFT]:
            sx_change = -0.05
            sy_change = 0
        elif pressed[pygame.K_RIGHT]:
            sx_change = 0.05
            sy_change = 0
            
        # update snake location
        snake_x += sx_change
        snake_y += sy_change

        # blit everything to the screen
        screen.blit(background, (0, 0))
        snake = pygame.draw.rect(screen, (0, 255, 0), (snake_x, snake_y, 10, 10))

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
    