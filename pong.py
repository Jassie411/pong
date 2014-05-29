import pygame, sys, random
from pygame.locals import *

pygame.init()

#Define helper functions
#Spawn ball function
def spawn_ball(direction = random.choice('01')):
    #direction should always be left if AI is enabled for paddle2.
    #0 is left, 1 is right
    if direction == 0:
        return (random.uniform(1.0, 3.0) * -1, random.uniform(1.0, 3.0) * -1)
    elif direction == 1:
        return (random.uniform(1.0, 3.0), random.uniform(1.0, 3.0) * -1)

#Select canvas size. Will be useful when I make UI
def canvas_size(str_size, width = 300, height = 200):
    #All sizes are multiples of 300 for width, and 200 for height
    if str_size == 'small':
        return (width * 2, height * 2)
    #Medium is simply width * 3
    elif str_size == 'medium':
        return (width * 3, height * 2)
    #Large will be a thing when I add support for a second ball

#Classes
#Canvas class. Handles gutter info, canvas size, static lines, and eventually images(maybe)
class Canvas:
    def __init__(self, name, size, gutter_width, color, line_color):
        self.name = name
        self.size = size
        self.gutter_width = gutter_width
        self.line_width = 2
        self.line_color = line_color
        self.width, self.height = self.size
        self.center = (self.width // 2, self.height // 2)
        self.half_width, self.half_height = self.center
        self.canvas_color = color

    def draw(self, canvas):
        pygame.draw.line(canvas, self.line_color, (self.gutter_width, 0), (self.gutter_width, self.height), self.line_width)
        pygame.draw.line(canvas, self.line_color, (self.width - self.gutter_width, 0), (self.width - self.gutter_width, self.height), self.line_width)
        pygame.draw.line(canvas, self.line_color, (self.half_width, 0), (self.half_width, self.height), self.line_width)

#Ball class
class Ball:
    def __init__(self, pos, vel, radius, color):
        self.pos = pos
        self.pos_x = int(self.pos[0])
        self.pos_y = int(self.pos[1])
        self.vel = vel
        self.radius = radius
        self.direction = 0
        self.color = color
        self.new_pos = (0, 0)

    def spawn_ball(self):
        #Reset ball position to center, and select a random velocity
        self.pos = my_canvas.center
        self.vel = spawn_ball(self.direction)

    def update(self):
        #Update ball's position
        self.pos = (self.pos[0] + self.vel[0], self.pos[1] + self.vel[1])
        self.pos_x = int(self.pos[0])
        self.pos_y = int(self.pos[1])

        #Check for vertical collisions
        #if ball.pos - radius hits ceiling or if ball.pos + radius hits the floor
        if (self.pos[1] - self.radius <= 0) or (self.pos[1] + self.radius >= my_canvas.height):
            self.new_vel
            self.vel = (self.vel[0], self.vel[1] * -1)

        #Check for collisions with gutter and with paddles
        #Check for collision with left paddle or gutter
        if self.pos[0] - self.radius <= my_canvas.gutter_width:
            if (self.pos[1] < paddle1.pos[0][1]) and (self.pos[1] > paddle1.pos[2][1]):
                self.vel = (self.vel[0] * -1.05, self.vel[1])
                paddle2.ai_ball_coming = True
            else:
                self.direction = "right"
                paddle2.ai_ball_coming = True
                self.spawn_ball()
                my_gui.score2 += 1
        #Check for collision with right paddle or gutter
        if self.pos[0] + self.radius >= my_canvas.width - my_canvas.gutter_width:
            if (self.pos[1] < paddle2.pos[0][1]) and (self.pos[1] > paddle2.pos[2][1]):
                self.vel = (self.vel[0] * -1.05, self.vel[1])
                paddle2.ai_ball_coming = False
            else:
                paddle2.ai_ball_coming = False
                self.direction = "left"
                self.spawn_ball()
                my_gui.score1 += 1
        #If my_gui.paused: Set color to black, pos to center, and velocity to 0. Else, set color to white.
        if my_gui.paused:
            self.color = (0, 0, 0)
            self.pos = my_canvas.center
            self.vel = (0, 0)
        else:
            self.color = (255, 255, 255)

    def draw(self, canvas):
        pygame.draw.circle(canvas, self.color, (self.pos_x, self.pos_y), 20)

#Class for paddles
class Paddle:
    def __init__(self, pos_init, width, height, color, ai = True):
        self.pos_init = pos_init
        self.vel = 0
        self.width = width
        self.height = height
        self.half_height = height // 2
        self.pos = ((self.pos_init[0], self.pos_init[1] - self.half_height), (self.pos_init[0] + self.width, self.pos_init[1] - self.half_height),
                    (self.pos_init[0] + self.width, self.pos_init[1] + self.half_height), (self.pos_init[0], self.pos_init[1] + self.half_height))
        self.color = color
        self.line_width = 1
        self.ai = ai
        self.ai_ball_coming = False

    #Updates paddle pos, only if paddle will say on screen
    def update(self):
        #Updates paddle's position. This will be cleaner
        if (self.pos[3][1] - self.vel >= self.height) and self.vel < 0:
            self.pos_init = (self.pos_init[0], self.pos_init[1] + self.vel)
            self.pos = ((self.pos_init[0], self.pos_init[1] - self.half_height), (self.pos_init[0] + self.width, self.pos_init[1] - self.half_height),
                        (self.pos_init[0] + self.width, self.pos_init[1] + self.half_height), (self.pos_init[0], self.pos_init[1] + self.half_height))
        elif (self.pos[0][1] + self.vel <= my_canvas.height - self.height) and self.vel > 0:
            self.pos_init = (self.pos_init[0], self.pos_init[1] + self.vel)
            self.pos = ((self.pos_init[0], self.pos_init[1] - self.half_height), (self.pos_init[0] + self.width, self.pos_init[1] - self.half_height),
                        (self.pos_init[0] + self.width, self.pos_init[1] + self.half_height), (self.pos_init[0], self.pos_init[1] + self.half_height))

        #AI for paddle2
        if self.ai:
            if self.ai_ball_coming:
                if (my_ball.pos[1] > self.pos[0][1]) and (my_ball.pos[1] < self.pos[2][1]):
                    self.vel = 0
                elif (my_ball.pos[1] < self.pos[0][1] - 25):
                    self.vel = -7
                elif (my_ball.pos[1] > self.pos[3][1] + 25):
                    self.vel = 7

    def draw(self, canvas):
        pygame.draw.polygon(canvas, self.color, self.pos)

#Class for GUI. Keeps track of score, if the game is paused, and will eventually have a timer
class GUI:
    def __init__(self):
        self.score1 = 0
        self.score2 = 0
        self.time = 0
        self.paused = False

    def draw(self, canvas):
        font = pygame.font.Font(None, 56)
        canvas.blit(font.render(str(self.score1), True, (255, 255, 255)), (my_canvas.width * 0.33, 45))
        canvas.blit(font.render(str(self.score2), True, (255, 255, 255)), (my_canvas.width * 0.66, 45))


fpsClock = pygame.time.Clock()
my_canvas = Canvas("Pygame Pong", canvas_size("medium"), 8, (150, 150, 150), (255, 255, 255))
my_gui = GUI()
my_ball = Ball(my_canvas.center, spawn_ball(0), 20, (255, 255, 255))
paddle1 = Paddle((0, my_canvas.half_height), my_canvas.gutter_width, 78, my_canvas.line_color, False)
paddle2 = Paddle((my_canvas.width - my_canvas.gutter_width, my_canvas.half_height), my_canvas.gutter_width, 78, my_canvas.line_color)
canvas = pygame.display.set_mode(my_canvas.size)
pygame.display.set_caption(my_canvas.name)

while True:
    canvas.fill(my_canvas.canvas_color)
    my_gui.draw(canvas)
    my_canvas.draw(canvas)
    my_ball.update()
    my_ball.draw(canvas)
    paddle1.update()
    paddle2.update()
    paddle1.draw(canvas)
    paddle2.draw(canvas)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                paddle2.vel = -7
            elif event.key == K_DOWN:
                paddle2.vel = 7
            if event.key == K_w:
                paddle1.vel = -7
            elif event.key == K_s:
                paddle1.vel = 7
            if event.key == K_SPACE:
                if my_gui.paused == False:
                    my_gui.paused = True
                elif my_gui.paused == True:
                    my_gui.paused = False
                    my_ball.spawn_ball()
                    my_ball.direction = 'left'
            if event.key == K_ESCAPE:
                pygame.quit()
        elif event.type == KEYUP:
            if event.key == K_UP or event.key == K_DOWN:
                paddle2.vel = 0
            if event.key == K_w or event.key == K_s:
                paddle1.vel = 0

    pygame.display.update()
    fpsClock.tick(60)
