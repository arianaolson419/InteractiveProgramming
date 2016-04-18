import pygame
from pygame.locals import QUIT, KEYDOWN
import time
from random import choice


class PyGameBrickBreakerView(object):
    """ Provides a view of the brick breaker model in a pygame
        window """
    def __init__(self, model, size):
        """ Initialize with the specified model """
        self.model = model
        self.screen = pygame.display.set_mode(size)


    def draw(self):
        """ Draw the game to the pygame window """
        # draw all the bricks to the screen
        self.screen.fill(pygame.Color('black'))
        for brick in self.model.bricks:
            r = pygame.Rect(brick.left,
                            brick.top,
                            brick.width,
                            brick.height)
            pygame.draw.rect(self.screen, pygame.Color('red'), r)
        pygame.draw.circle(self.screen,
                           pygame.Color('white'),
                           (self.model.ball.center_x, self.model.ball.center_y),
                           self.model.ball.radius)

        r = pygame.Rect(self.model.paddle.left,
                        self.model.paddle.top,
                        self.model.paddle.width,
                        self.model.paddle.height)
        pygame.draw.rect(self.screen, pygame.Color('orange'), r)
        pygame.display.update()


class BrickBreakerModel(object):
    """ Represents the game state for brick breaker """
    def __init__(self, width, height):
        self.height = height
        self.width = width

        self.BRICK_WIDTH = 20
        self.BRICK_HEIGHT = 10
        self.MARGIN = 5
        self.GRID_BOTTOM = height/2
        self.BALL_RADIUS = 10

        self.bricks = []
        for left in range(self.MARGIN,
                          self.width - self.MARGIN - self.BRICK_WIDTH,
                          self.MARGIN + self.BRICK_WIDTH):
            for top in range(self.MARGIN, self.GRID_BOTTOM, self.MARGIN + self.BRICK_HEIGHT):
                self.bricks.append(Brick(left,
                                         top,
                                         self.BRICK_WIDTH,
                                         self.BRICK_HEIGHT))
        self.ball = Ball(width/2, height - 40, self.BALL_RADIUS)
        self.paddle = Paddle(width/2, height - 15)

    def update(self):
        """ Update the model state """
        self.ball.update()


class Paddle(object):
    """ Represents the paddle in the game """
    def __init__(self, left, top):
        self.left = left
        self.top = top
        self.width = 40
        self.height = 10


class Ball(object):
    """ Represents a ball in my brick breaker game """
    def __init__(self, center_x, center_y, radius):
        """ Create a ball object with the specified geometry """
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.velocity_x = 0         # pixels / frame
        self.velocity_y = -5         # pixels / frame

    def update(self):
        """ Update the position of the ball due to time passing """
        self.center_x += self.velocity_x
        self.center_y += self.velocity_y


class Brick(object):
    """ Represents a brick in my brick breaker game """
    def __init__(self, left, top, width, height):
        """ Initializes a Brick object with the specified
            geometry and color """
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        #self.color = color


class PyGameKeyboardController(object):
    def __init__(self, model):
        self.model = model



    
    def handle_event(self,event):
        """ Look for left and right keypresses to
            modify the x position of the paddle """
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_LEFT:
            self.model.paddle.left -= 10
        if event.key == pygame.K_RIGHT:
            self.model.paddle.left += 10

if __name__ == '__main__':
    pygame.init()
    size = (640, 480)

    model = BrickBreakerModel(size[0], size[1])
    view = PyGameBrickBreakerView(model, size)
    controller = PyGameKeyboardController(model)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            else:
                controller.handle_event(event)
        model.update()
        view.draw()
        time.sleep(.001)