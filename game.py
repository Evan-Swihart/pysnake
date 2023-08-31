# import the pygame module, so you can use it
import pygame

# define a main function
def main():
    
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Bouncing Head")
     
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((1000,667))
    
    # load my first image
    image = pygame.image.load("image.png").convert()
    image.set_colorkey((255,255,255))

    # set starting positions for image
    image_x = 50
    image_y = 50

    # set speed for image
    image_x_speed = 1
    image_y_speed = 1
    # image.set_alpha(128)

    # load and set the background image
    background_image = pygame.image.load("background.png").convert()

    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:

        # check if the image is still on the screen
        if image_x > 1000 - image.get_width() or image_x < 0:
            image_x_speed = image_x_speed * -1
        if image_y > 667 - image.get_height() or image_y < 0:
            image_y_speed = image_y_speed * -1
        
        # update image position
        image_x += image_x_speed
        image_y += image_y_speed

         # blit background on screen
        screen.blit(background_image, [0,0])

        #blit image to screen
        screen.blit(image, (image_x, image_y))

        # update the screen to make the changes visible (fullscreen update)
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
    