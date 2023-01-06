import pygame
from pygame.locals import *
import math

# init
panel_corner = pygame.image.load('assets/panel_corner.png')
panel_top = pygame.image.load('assets/panel_top.png')
panel_record = pygame.image.load('assets/record.png')

pygame.init()

display_info = pygame.display.Info()
screen_w = 320
screen_h = 240
center_w = screen_w / 2
center_h = screen_h / 2
aspect_ratio = '4:3'


display_screen = pygame.display.set_mode([screen_w, screen_h])
screen = pygame.Surface((screen_w, screen_h))

scale_ratio = screen_w / 1024
print('Using scaling ratio', scale_ratio)

running = True

# To align things properly on all setups, we must align things based on a 1024x768 resolution and then fit it to whatever res we are running in
# all programming for UI placement should assume the resolution is 1024x768.
# Thus the middle width coordinate is 512 X. Objects are placed on a grid of this size,
# but are actually rendered a the native resolution selected. This is to offer as much
# clarity as possible at every resolution. 

def scale_x(x):
    return x * (screen_w / 1024)
    
def scale_y(y):
    return y * (screen_h / 768)

def blit_image(image, x, y, scale):
    distance_from_center = math.dist((x,), (center_w,))
    newx = scale_x(x)
    newy = scale_y(y)
    rect = image.get_rect()
    image = pygame.transform.smoothscale(image, ((image.get_width() * scale) * scale_ratio, (image.get_height() * scale) * scale_ratio))
    screen.blit(image, (newx, newy))
    
def draw_center(image, x, y, scale):
    image_center_x = x - ((image.get_width() * scale) / 2)
    image_center_y = y - ((image.get_height()  * scale) / 2)
    blit_image(image, image_center_x, image_center_y, scale)

def ui_corners():
    draw_center(panel_top, 512, 50, 0.5)
    draw_center(panel_record, 512, 384, 0.3)

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        #elif event.type == VIDEORESIZE:
    
   
    screen.fill('black')
    ui_corners()
    screen_w, screen_h = screen.get_size()

    scaled_screen = pygame.transform.smoothscale(screen, display_screen.get_size())
    display_screen.blit(scaled_screen, (0, 0))
    
    # flip display. Render
    pygame.display.flip()



# Shutdown.
pygame.quit()