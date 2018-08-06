#import basic modules
import pygame
from pygame.locals import *
import random
from classes import *
import os.path

pygame.init()
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
print(width, height)

#game constants
MAX_SHOTS      = 2      #most player bullets onscreen
ENEMY_ODDS     = 10     #chances a new alien appears
SCREENRECT     = Rect(0, 0, width, height) #variable screen size
RESIZE =  width/1920 #scaling of images
SCORE          = 0 #initial score

main_dir = os.path.split(os.path.abspath(__file__))[0]

def main():
    # Initialize pygame
    if pygame.mixer and not pygame.mixer.get_init():
        print ('Warning, no sound')
        pygame.mixer = None

    # Set the display mode
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, pygame.FULLSCREEN, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, pygame.FULLSCREEN, bestdepth)

    #Load images, assign to sprite classes
    #(do this before the classes are used, after screen setup

    #img = load_image('player1.gif')
    #Player.images = [img, pygame.transform.flip(img, 1, 0)]
    #img = load_image('explosion1.gif')
    #Explosion.images = [img, pygame.transform.flip(img, 1, 1)]
    #Alien.images = load_images('alien1.gif', 'alien2.gif', 'alien3.gif')
    #Bomb.images = [load_image('bomb.gif')]
    #Shot.images = [load_image('shot.gif')]

    #decorate the game window
    icon = load_image('icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Shooting Hills')
    pygame.mouse.set_visible(0)

    #load the sound effects
    background = load_sound('koeniggratzer.mp3')
    shoot_sound = load_sound('car_door.wav')
    if pygame.mixer:
        music = os.path.join(main_dir+'\media\\', 'koeniggratzer.mp3')
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)




def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir+'\media\\', file)
    try:
        surface = pygame.image.load(file)
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
    file = main_dir + '\media\\' + file
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print ('Warning, unable to load, %s' % file)
    return dummysound()
if __name__ == '__main__': main()