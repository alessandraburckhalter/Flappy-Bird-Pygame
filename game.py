import pygame, random
from pygame import mixer
from pygame.locals import *
from time import sleep

# variables that will not change
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SPEED = 8
GRAVITY = 0.8
GAME_SPEED = 9

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 120

points = 0
record = 0

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('bluebird-upflap.png').convert_alpha(),
                       pygame.image.load('bluebird-midflap.png').convert_alpha(),
                       pygame.image.load('bluebird-downflap.png').convert_alpha()] # convert_alpha converts a surface to the same 'pixel format' as the display. It will help with the images collision.

        self.speed = SPEED

        self.current_image = 0 

        self.image = pygame.image.load('bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        self.rect[0] = SCREEN_WIDTH / 2  # X position that the bird starts
        self.rect[1] = SCREEN_HEIGHT / 2  # Y position that the bird starts

    def update(self):
        self.current_image = (self.current_image + 1) % 3  # cycle between the 3 images to give the impression that the bird is flapping its wings
        self.image = self.images[self.current_image]
        self.rect[1] += self.speed  # makes the bird fall
        self.speed += GRAVITY

    def bump(self): # makes the bird fly/jump
        self.speed = -SPEED


class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('pipe-red.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))  # change the size of the pipe image

        self.rect = self.image.get_rect()
        self.rect[0] = xpos  # pipes will only appear in X positions

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)  # "False" to flip the X and "True" to flip the Y
            self.rect[1] = -(self.rect[3] - ysize)  # hides a piece of the pipe, to put the size I want
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize  # full screen - a certain y size = pipe size
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED


class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('floor.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos # x position
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT # y position

    def update(self):
        self.rect[0] -= GAME_SPEED #floor speed

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])  # verify if any sprite is off the screen

def get_random_pipes(xpos): # to generate pipes in random sizes
    size = random.randint(100, 300) # sizes between 100 and 300 
    pipe = Pipe(False, xpos, size) # False because it is not inverted
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return (pipe, pipe_inverted) # will return random pipes in 2 different position

#function to count the points after passing pipes
def info():
    global points, record

    if points > record:
        record = points

# function to start the game
def start_the_game():
    menu = True
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # main song
    mixer.music.load('game.wav')
    mixer.music.play(-1)    
    
    # background image
    BACKGROUND = pygame.image.load('background-day.png')
    BACKGROUND = pygame.transform.scale(BACKGROUND, (
    SCREEN_WIDTH, SCREEN_HEIGHT))  # it transforms the size of the background image to the same size as the screen

    bird_group = pygame.sprite.Group()
    bird = Bird()
    bird_group.add(bird)

    ground_group = pygame.sprite.Group()

    for i in range(2):
        ground = Ground(2 * SCREEN_WIDTH * i)
        ground_group.add(ground)

    pipe_group = pygame.sprite.Group()
    for i in range(2):
        pipes = get_random_pipes(SCREEN_WIDTH * i + 800) # distance between pipes
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    clock = pygame.time.Clock()  # Frames Per Second

    global points, record
    points = 0

    while True:  # main loop, what keeps the game running
        font = pygame.font.SysFont(pygame.font.get_default_font(), 60)
        # menu
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and menu == True:
                if event.button == 1:
                    screen.blit(BACKGROUND, (0, 0))
                    ground_group.draw(screen)
                    pygame.display.update()
                    sleep(0.3)
                    screen.blit(font.render('3', True, (255, 255, 255)), (400, 250))
                    pygame.display.update()
                    sleep(1)
                    screen.blit(BACKGROUND, (0, 0))
                    ground_group.draw(screen)
                    pygame.display.update()
                    screen.blit(font.render('2', True, (255, 255, 255)), (400, 250))
                    pygame.display.update()
                    sleep(1)
                    screen.blit(BACKGROUND, (0, 0))
                    ground_group.draw(screen)
                    pygame.display.update()
                    screen.blit(font.render('1', True, (255, 255, 255)), (400, 250))
                    pygame.display.update()
                    sleep(1)
                    screen.blit(BACKGROUND, (0, 0))
                    ground_group.draw(screen)
                    pygame.display.update()
                    menu = False

            if event.type == KEYDOWN and menu == False:
                if event.key == K_SPACE:
                    bird.bump()

        clock.tick(30)
        screen.blit(BACKGROUND,
                    (0, 0))  # takes the surface of the background and draws on the screen from the position (x, y)

        if menu == True:
            # write the message on the first screen
            font = pygame.font.SysFont(pygame.font.get_default_font(), 60)
            ground_group.draw(screen)
            txt = font.render("CLICK TO START", True, (255,255,255))
            screen.blit(txt, (250, 250))
            font = pygame.font.SysFont(pygame.font.get_default_font(), 25)
            ground_group.draw(screen)
            txt = font.render("ONCE GAME STARTS, PRESS SPACE TO MAKE THE BIRD FLY", True, (0, 0, 0))
            screen.blit(txt, (150, 300))
        if menu == False:
            if is_off_screen(ground_group.sprites()[0]):
                ground_group.remove(ground_group.sprites()[0]) # removes the ground if it is off the screen
                new_ground = Ground(GROUND_WIDTH - 20)
                ground_group.add(new_ground)

            if is_off_screen(pipe_group.sprites()[0]):
                pipe_group.remove(pipe_group.sprites()[0])  # removes the pipe if it is off the screen
                pipe_group.remove(pipe_group.sprites()[
                                      0])  # after removing the first pipe, the inverted one becomes 0. That's why there are two equal lines

                pipes = get_random_pipes(SCREEN_WIDTH * 2)
                
                pipe_group.add(pipes[0])
                pipe_group.add(pipes[1])
                points += 1

            bird_group.update()
            ground_group.update()
            pipe_group.update()
            
            bird_group.draw(screen)
            ground_group.draw(screen)
            pipe_group.draw(screen)
            
            font = pygame.font.SysFont(pygame.font.get_default_font(), 80)
            if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
                    pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):# "mask" makes that only the pixels that have any color in the bird collide with the pixels of the floor or pipe
                # hit sound
                hit_sound = mixer.Sound('hit.wav')
                hit_sound.play()
                # creates the box at the end   
                font1 = pygame.font.SysFont("arial", 33)
                pygame.draw.rect(screen, 0x543847, [305, 104, 200, 200 ], 10)
                pygame.draw.rect(screen, 0xDED895, [310, 108, 190, 190])
                font2 = pygame.font.SysFont("arial", 33)
                screen.blit(font2.render('GAME OVER', True, (255,0,0)), (340, 120))
                txt = font1.render("Your Score", 0, (0,0,255))
                screen.blit(txt, (350, 170))
                txt = font1.render(str(points), 0, (0,0,0))
                screen.blit(txt, (400, 200))
                txt = font1.render("Highest Score", 0, (0,0,255))
                screen.blit(txt, (330, 240))
                txt = font1.render(str(record), 0, (0,0,0))
                screen.blit(txt, (400, 270))
                info()
                pygame.display.update()
                sleep(5)
                start_the_game()
            else:
                # creates the points on the screen during the game
                txt = font.render(str(points), 0, (255, 255, 255))
                screen.blit(txt, (380, 146))
        pygame.display.update()         

start_the_game()