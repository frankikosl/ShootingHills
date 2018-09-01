#import basic modules
import pygame
from pygame.locals import *
import random
import os.path
import ctypes
#test
pygame.init()
ctypes.windll.user32.SetProcessDPIAware()

#game constants
MAX_SHOTS      = 2      #most player bullets onscreen
ENEMY_ODDS     = 10     #chances a new alien appears
TRUERES = (
    ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)) #screen resolution
width, height = TRUERES #separate variables
RESIZE =  width/1920 #scaling of images
SCORE          = 0 #initial score

main_dir = os.path.split(os.path.abspath(__file__))[0]

#Classes for the objects

class Background(pygame.sprite.Sprite):
    def __init__(self, image_files, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.images = image_files
        self.image = self.images[0]
        self.index = 1
        self.count = 0
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
    def update(self):
        self.count += 1
        if self.count > 10:
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            self.count = 0

class Enemy(pygame.sprite.Sprite):
    """Class for the Bayonet enemy that runs toward the player"""
    images = []
    def __init__(self):
         pygame.sprite.Sprite.__init__(self, self.containers)
    def update(self):
        return

class EnemyBullet(pygame.sprite.Sprite):
    """Class for the bullet that the player must dodge"""
    def __init__(self, bulletimage):
         pygame.sprite.Sprite.__init__(self, self.containers)
         self.image = bulletimage
    def update(self):
        return

class MunitionBox(pygame.sprite.Sprite):
    """Class for the munition box that empties as the player shoots"""
    images = []
    def __init__(self):
         pygame.sprite.Sprite.__init__(self, self.containers)
    def update(self):
        return

class Player(pygame.sprite.Sprite):
    """Class for the player character that jumps, ducks and shoots"""
    images = []
    def __init__(self):
         pygame.sprite.Sprite.__init__(self, self.containers)
    def update(self):
        return

class PlayerBullet(pygame.sprite.Sprite):
    """Class for the player's bullet that kills the running enemy"""
    def __init__(self):
         pygame.sprite.Sprite.__init__(self, self.containers)
         self.image = bulletimage
    def update(self):
        return


def main():

    CURRENTMENU = 0 #0 is opening, 1 is about, 2 is difficulty and 3 is game

    # Initialize pygame
    pygame.mixer.init()
    if pygame.mixer and not pygame.mixer.get_init():
        print ('Warning, no sound')
        pygame.mixer = None
    font = pygame.font.Font(main_dir + '\media\\BUILDER.ttf', int(height / 10))
    arrow = pygame.font.Font(main_dir + '\media\\8-BIT WONDER.ttf', int(height / 15))
    # Set the display mode
    screen = pygame.display.set_mode(TRUERES,pygame.FULLSCREEN)

    #Load images, assign to sprite classes
    #(do this before the classes are used, after screen setup
    menu = Background(load_images(
        'Unbenannt1.png', 'Unbenannt2.png', 'Unbenannt3.png') ,[0,0])
    difficulty = Background(load_images(
        'difficulty1.png', 'difficulty2.png', 'difficulty3.png') ,[0,0])
    #decorate the game window
    icon = load_image('icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Shooting Hills')
    pygame.mouse.set_visible(0)

    #load the sound effects
    hurt_sound = load_sound('hurt.mp3')
    shoot_sound = load_sound('shoot.mp3')
    jump_sound = load_sound('jump.mp3')
    button_sound = load_sound('button.mp3')

    #play the bgmusic
    if pygame.mixer:
        music = [os.path.join(
            main_dir+'\media\\', 'koeniggratzer.mp3'), os.path.join(
                main_dir+'\media\\', 'erika.mp3'), os.path.join(
                    main_dir+'\media\\', 'funkerlied.mp3'), os.path.join(
                    main_dir+'\media\\', 'fundo.mp3')]
        pygame.mixer.music.load(music[0])
        pygame.mixer.music.play(-1)

    # Initialize Game Groups
    enemies = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    ammobox = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()
    lastalien = pygame.sprite.GroupSingle()
    
    #assign default groups to each sprite class
    menu.containers = all
    difficulty.containers = all

    clock = pygame.time.Clock()
    
    #set fonts
    startSurface = font.render('START', False, (0, 0, 0))
    aboutSurface = font.render('ABOUT', False, (0, 0, 0))
    backSurface = font.render('BACK', False, (0, 0, 0))
    easySurface = font.render('EASY', False, (0, 0, 0))
    mediumSurface = font.render('MEDIUM', False, (0, 0, 0))
    hardSurface = font.render('HARD', False, (0, 0, 0))
    quitSurface = font.render('QUIT', False, (0, 0, 0))

    running = True
    arrowindex = 0
    while running:
        #create the background, tile the bgd image
        if CURRENTMENU == 0:
            screen.blit(menu.image, menu.rect)
            screen.blit(arrowsSurface,(width*23/40,(height*65/96 + (height*8/96 * arrowindex))))
            screen.blit(startSurface,(width*24/40,height*64/96))
            screen.blit(aboutSurface,(width*24/40,height*72/96))
            screen.blit(quitSurface,(width*24/40,height*80/96))
            pygame.display.flip()
             # clear/erase the last drawn sprites
            all.clear(screen, menu)

            #update all the sprites
            menu.update()
        
            #draw the scene
            dirty = all.draw(screen)
            pygame.display.update(dirty)
        if CURRENTMENU == 2:
            screen.blit(difficulty.image, difficulty.rect)
            if arrowindex < 3:
                screen.blit(arrowsSurface,((width*4/40 + width*12*arrowindex/40),height*51/96))
            else:
                screen.blit(arrowsSurface,((width*4/40 + width*25*(arrowindex-3)/40),height*80/96))
            screen.blit(easySurface,(width*5/40,height*50/96))
            screen.blit(mediumSurface,(width*17/40,height*50/96))
            screen.blit(hardSurface,(width*30/40,height*50/96))
            screen.blit(quitSurface,(width*5/40,height*80/96))
            screen.blit(backSurface,(width*30/40,height*80/96))
            pygame.display.flip()
            # clear/erase the last drawn sprites
            all.clear(screen, difficulty)

            #update all the sprites
            difficulty.update()
        
            #draw the scene
            dirty = all.draw(screen)
            pygame.display.update(dirty)

        #get input
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if CURRENTMENU == 0:
                   if event.key == pygame.K_DOWN or (
                    event.key == pygame.K_UP):
                        if event.key == pygame.K_UP and arrowindex != 0:
                            arrowindex -= 1
                        if event.key == pygame.K_DOWN and arrowindex != 2:
                            arrowindex += 1
                   if event.key == pygame.K_SPACE:
                       if arrowindex == 0:
                           CURRENTMENU = 2
                           arrowindex = 0
                           break
                       elif arrowindex == 1:
                           CURRENTMENU = 1
                           arrowindex = 0
                           break
                       elif arrowindex == 2:
                           running = False
                           break
                   if event.key == pygame.K_ESCAPE:
                       running = False
                       break
                if CURRENTMENU == 2:
                   if event.key == pygame.K_LEFT or (
                    event.key == pygame.K_RIGHT):
                        if event.key == pygame.K_RIGHT and arrowindex != 4:
                            arrowindex += 1
                        if event.key == pygame.K_LEFT and arrowindex != 0:
                            arrowindex -= 1
                   if event.key == pygame.K_ESCAPE:
                       CURRENTMENU = 0
                       arrowindex = 0
                       break
            elif event.type == pygame.QUIT:
                running = False
                break


        #cap the framerate
        clock.tick(30)

    pygame.quit()
#General functions for loading media files


def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir+'\media\\', file)
    try:
        surface = pygame.image.load(file)
        surfacewidth, surfaceheight = surface.get_rect().size
        surface = pygame.transform.scale(surface, (int(surfacewidth * RESIZE), int(surfaceheight * RESIZE)))
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()

def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs

class dummysound:
    def play(self): pass
def get_arrows(menu, index):
    arrowsSurface = arrow.render('[       ]', False, (0, 0, 0))
def load_sound(file):
    if not pygame.mixer: return dummysound()
    file = os.path.join(main_dir+'\media\\'+file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print ('Warning, unable to load, %s' % file)
    return dummysound()

if __name__ == '__main__': main()