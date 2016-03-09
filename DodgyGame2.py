import pygame
from pygame.locals import QUIT
import time
from random import *
import cv2
import numpy as np

class SkyModel(object):
    '''Represents the game state for Dodgy Game'''
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.BIRD_Y = 0
        self.USER_X = 250
        self.RADIUS = 10
        self.bird = Bird(randint(1,500), self.BIRD_Y , self.RADIUS)
        self.user = User(self.USER_X, 500, 80)
        


    def update(self):
        '''Update the model state'''
        self.bird.update()


class View(object):
    """ Provides a view of the Dodgy Game model in a pygame
        window """
    def __init__(self, model, size):
        """ Initialize with the specified model """
        self.model = model
        self.screen = pygame.display.set_mode(size)
        self.end = pygame.image.load('gameover.png')
        self.eyes = pygame.transform.scale(pygame.image.load('eyes.png'), (self.model.user.radius, self.model.user.radius))
        self.ostrich = pygame.transform.scale(pygame.image.load('ostrich.png'), (self.model.bird.radius, self.model.bird.radius))



    def draw(self):
        """ Draw the game to the pygame window """
        self.screen.fill(pygame.Color(135, 206, 250))   #sky

        pygame.draw.circle(self.screen, #'bird'
                           self.model.bird.color,
                           (self.model.bird.center_x, self.model.bird.center_y),
                           self.model.bird.radius)
        self.ostrich = pygame.transform.scale(pygame.image.load('ostrich.png'), (self.model.bird.radius * 2, self.model.bird.radius * 2))
        self.screen.blit(self.ostrich, (self.model.bird.center_x - self.model.bird.radius, self.model.bird.center_y - self.model.bird.radius))


        pygame.draw.circle(self.screen, #player
                           pygame.Color('white'),
                           (self.model.user.center_x, self.model.user.center_y),
                           self.model.user.radius)
        self.screen.blit(self.eyes, (self.model.user.center_x -40, self.model.user.center_y-80))
        
        if (self.model.bird.center_x + self.model.bird.radius >= self.model.user.center_x - self.model.user.radius)  and \
         (self.model.bird.center_y + self.model.bird.radius >= self.model.user.center_y - (self.model.user.radius -20)) and \
         (self.model.bird.center_x - self.model.bird.radius <= self.model.user.center_x + self.model.user.radius -20 )  and \
         (self.model.bird.center_y + self.model.bird.radius >= self.model.user.center_y - (self.model.user.radius -20)):
            #determining if a collision happened
            self.screen.blit(self.end, (0,0))
            
            

        pygame.display.update()




class Bird(object):
    """ Represents a bird in dodging game """
    def __init__(self, center_x, center_y, radius, color = pygame.Color('yellow')):
        """ Create a ball object with the specified geometry """
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.growth = 2     #rate that the bird gets bigger as it gets 'closer'
        self.color = color
    
    def update(self):
        """ Update the position of the ball due to time passing """
        self.radius += self.growth
        
        if self.center_y < 500:
            #if the bird has not reached the bottom of the screen
            self.center_y += 25
            
        else:
            #restart position at top of screen
            self.center_y = 0
            self.radius = 10
            self.center_x = randint(0, 500) 
            
        


class User(object):
    """ Represents the user in my dodging game """
    def __init__(self, center_x, center_y, radius):
        """ Create a ball object with the specified geometry """
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius



class Movement(object):
    def __init__(self, model):
        self.model = model
        self.MOVE = pygame.USEREVENT + 1
        move_event = pygame.event.Event(self.MOVE)
        pygame.time.set_timer(self.MOVE, 1) #this event occurs every millisecond
        self.cap = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier('/home/arianaolson/haarcascade_frontalface_alt.xml')
    def handle_event(self, event):
        '''uses the position of player's face to control the user'''
        for (x,y,w,h) in faces:
            self.model.user.center_x = 500-(2*x)
                
                



if __name__ == '__main__':
    pygame.init()
    size = (500, 500)

    model = SkyModel(size[0], size[1])
    view = View(model, size)
    movement = Movement(model)
    running = True
    
    while running:
        ret, frame = movement.cap.read()
        faces = movement.face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            else:
                movement.handle_event(event)
        model.update()
        view.draw()
        time.sleep(.01)
    movement.cap.release()     
    cv2.destroyAllWindows()

   