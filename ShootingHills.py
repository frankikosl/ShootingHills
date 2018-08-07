#import basic modules
import pygame
from pygame.locals import *
import random
import os.path
import ctypes

pygame.init()
ctypes.windll.user32.SetProcessDPIAware()

#game constants
MAX_SHOTS      = 2      #most player bullets onscreen
ENEMY_ODDS     = 10     #chances a new alien appears
TRUERES = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)) #screen resolution
width, heigth = TRUERES
RESIZE =  width/1920 #scaling of images
SCORE          = 0 #initial score

main_dir = os.path.split(os.path.abspath(__file__))[0]

#Classes for the objects

class Background(pygame.sprite.Sprite):
    def __init__(self, image_files, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.images = image_files
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
    def update(self):
        return

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
    # Initialize pygame
    pygame.mixer.init()
    if pygame.mixer and not pygame.mixer.get_init():
        print ('Warning, no sound')
        pygame.mixer = None

    # Set the display mode
    screen = pygame.display.set_mode(TRUERES,pygame.FULLSCREEN)

    #Load images, assign to sprite classes
    #(do this before the classes are used, after screen setup
    menu = Background(load_images(
        'Unbenannt1.png', 'Unbenannt2.png', 'Unbenannt3.png') ,[0,0])
    #decorate the game window
    icon = load_image('icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Shooting Hills')
    pygame.mouse.set_visible(0)

    #create the background, tile the bgd image
    screen.blit(menu.image, menu.rect)
    pygame.display.flip()

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
    
    clock = pygame.time.Clock()
    
    running = True
    while running:
        #get input
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
            elif event.type == pygame.QUIT:
                running = False
                break
        # clear/erase the last drawn sprites
        all.clear(screen, menu)

        #update all the sprites
        all.update()
            
        #draw the scene
        dirty = all.draw(screen)
        pygame.display.update(dirty)

        #cap the framerate
        clock.tick(40)
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