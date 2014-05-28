import pygame, sys, random
from pygame.locals import *

pygame.init()
#pygame.display.init()
#pygame.font.init()

#Define helper functions
#Picks the direction for the first ball spawn
def random_direction():
    d = random.randint(0, 1)
    if d == 0:
        return "left"
    else:
        return "right"

#Uses random_direction and decides how fast the first ball travels
#It is also used in Ball class to pick velocity for every ball that spawns after
def spawn_ball(direction):
    velocity = [0, 0]
    if direction == "left":
        velocity[0] = (random.randrange(120, 240) / 60.0) * -1
        velocity[1] = (random.randrange(60, 180) / 60.0) * -1
    elif direction == "right":
        velocity[0] = random.randrange(120, 240) / 60.0
        velocity[1] = (random.randrange(60, 180) / 60.0) * -1
    return velocity

#Can be used to determine the size of the Pong table
def canvas_size(sl, width = 300, height = 200):
    if sl == "small":
        return (width * 2, height * 2)
    elif sl == "large":
        return (width * 3, height * 2)

#Classes
#Canvas class. Handles gutter info, canvas size, and static lines
class Canvas:
    def __init__(self, name, size, gutter_width, color, line_color):
        self.name = name
        self.size = size
        self.gutter_width = gutter_width
        self.line_width = 2
        self.line_color = line_color
        self.width = self.size[0]
        self.height = self.size[1]
        self.canvas_color = color
        self.center = [self.width // 2, self.height // 2]

    def get_name(self):
        return self.name
    def get_size(self):
        return self.size
    def get_width(self):
        return self.width
    def get_half_width(self):
        return self.width // 2
    def get_height(self):
        return self.height
    def get_half_height(self):
        return self.height // 2
    def get_center(self):
        return self.center
    def get_color(self):
        return self.canvas_color
    def get_gutter_width(self):
        return self.gutter_width
    def get_line_color(self):
        return self.line_color

    def draw(self, canvas):
            pygame.draw.line(canvas, self.line_color, (0 + self.gutter_width, 0), (0 + self.gutter_width, self.height), self.line_width)
            pygame.draw.line(canvas, self.line_color, (self.width - self.gutter_width, 0), (self.width - self.gutter_width, self.height), self.line_width)
            pygame.draw.line(canvas, self.line_color, (self.width // 2, 0), (self.width // 2, self.height), self.line_width)

#Ball Class
class Ball:
    def __init__(self, pos, vel, radius, color):
        self.pos = [pos[0], pos[1]]
        self.pos_x = int(self.pos[0])
        self.pos_y = int(self.pos[1])
        self.vel = [vel[0], vel[1]]
        self.radius = radius
        self.direction = 'left'
        self.color = color

    def set_color(self, color):
        self.color = color

    def spawn_ball(self):
        self.pos = [my_canvas.get_half_width(), my_canvas.get_half_height()]
        self.vel = spawn_ball(self.direction)

    def get_vel(self):
        return self.vel

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos_x = int(self.pos[0])
        self.pos_y = int(self.pos[1])
        
        #Check for vertical collisions
        if self.pos[1] - self.radius <= 0:
            self.vel[1] = self.vel[1] * -1
        elif self.pos[1] + self.radius >= my_canvas.get_height():
            self.vel[1] = self.vel[1] * -1
            
        #Check for collisions with gutter and with paddles
        if self.pos[0] - self.radius <= my_canvas.get_width() - my_canvas.get_width() + my_canvas.get_gutter_width():
            if (self.pos[1] < paddle1.get_pos()[0][1]) and (self.pos[1] > paddle1.get_pos()[2][1]):
                self.vel[0] *= -1.05
                paddle2.ai_ball_coming = True
            else:
                self.direction = "right"
                paddle2.ai_ball_coming = True
                self.spawn_ball()
                my_gui.score2 += 1
        if self.pos[0] + self.radius >= my_canvas.get_width() - my_canvas.get_gutter_width():
            if (self.pos[1] < paddle2.get_pos()[0][1]) and (self.pos[1] > paddle2.get_pos()[2][1]):
                self.vel[0] *= -1.05
                paddle2.ai_ball_coming = False
            else:
                paddle2.ai_ball_coming = False
                self.direction = "left"
                self.spawn_ball()
                my_gui.score1 += 1

        if my_gui.paused:
            self.set_color((0, 0, 0))
            self.pos = my_canvas.get_center()
            self.vel = [0, 0]
        else:
            self.set_color((255, 255, 255))
            

    def draw(self, canvas):
        pygame.draw.circle(canvas, self.color, [self.pos_x, self.pos_y], 20)

#Class for Paddles
class Paddle:
    def __init__(self, pos, width, height, color, ai = True):
        self.pos = pos
        self.vel = 0
        self.width = width
        self.height = height
        self.color = color
        self.line_width = 1
        self.ai = ai
        self.ai_ball_coming = False

    #Updates paddle position, only if the paddle will stay on the screen
    def update(self):
        age = 0

        if (self.pos[0][1] + self.vel >= self.height) and self.vel < my_canvas.get_height() - my_canvas.get_height():
            self.pos[0][1] += self.vel
            self.pos[1][1] += self.vel
            self.pos[2][1] += self.vel
            self.pos[3][1] += self.vel
        elif (self.pos[3][1] + self.vel <= my_canvas.get_height() - self.height) and self.vel > my_canvas.get_height() - my_canvas.get_height():
            self.pos[0][1] += self.vel
            self.pos[1][1] += self.vel
            self.pos[2][1] += self.vel
            self.pos[3][1] += self.vel

        #AI for paddle2
        if self.ai == True:
            if self.ai_ball_coming == True:
                while age < 50:
                    if (my_ball.pos[1] > self.pos[0][1]) and (my_ball.pos[1] < self.pos[2][1]):
                        self.vel = 0
                        age += 0.1
                    elif (my_ball.pos[1] < self.pos[0][1] - 25):
                        self.vel = -7
                        age += 0.1
                    elif (my_ball.pos[1] > self.pos[3][1] + 25):
                        self.vel = 7
                        age += 0.1
                        
    def draw(self, canvas):
        pygame.draw.polygon(canvas, self.color, self.pos)

    def set_vel(self, new_vel):
        self.vel = new_vel

    def get_pos(self):
        return self.pos
    
#Class for GUI. Keeps track of score, if the game is paused, and will eventually have a timer
class GUI:
    def __init__(self):
        self.score1 = 0
        self.score2 = 0
        self.time = 0
        self.paused = False

    def draw(self, canvas):
        #font = pygame.font.Font('arial.ttf', 56)
        font = pygame.font.Font(None, 56)
        canvas.blit(font.render(str(self.score1), True, (255, 255, 255)), (my_canvas.get_width() * 0.33, 45))
        canvas.blit(font.render(str(self.score2), True, (255, 255, 255)), (my_canvas.get_width() * 0.66, 45))

            


fpsClock = pygame.time.Clock()
my_canvas = Canvas("Pygame Pong", canvas_size("large"), 8, (150, 150, 150), (255, 255, 255))
my_gui = GUI()
my_ball = Ball(my_canvas.get_center(), spawn_ball(random_direction()), 20, (255, 255, 255))
paddle1 = Paddle([[0, my_canvas.get_half_height() + 40], 
                  [8, my_canvas.get_half_height() + 40], 
                  [8, my_canvas.get_half_height() - 40], 
                  [0, my_canvas.get_half_height() - 40]], my_canvas.get_gutter_width(), 79, my_canvas.get_line_color())
paddle2 = Paddle([[my_canvas.get_width() - 8, my_canvas.get_half_height() + 40], 
                  [my_canvas.get_width(), my_canvas.get_half_height() + 40], 
                  [my_canvas.get_width(), my_canvas.get_half_height() - 40], 
                  [my_canvas.get_width() - 8, my_canvas.get_half_height() - 40]], my_canvas.get_gutter_width(), 79, 
                  my_canvas.get_line_color())

canvas = pygame.display.set_mode(my_canvas.get_size())
pygame.display.set_caption(my_canvas.get_name())

while True:
    canvas.fill(my_canvas.get_color())
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
                paddle2.set_vel(-7)
            elif event.key == K_DOWN:
                paddle2.set_vel(7)
            if event.key == K_w:
                paddle1.set_vel(-7)
            elif event.key == K_s:
                paddle1.set_vel(7)
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
                paddle2.set_vel(0)
            if event.key == K_w or event.key == K_s:
                paddle1.set_vel(0)

    pygame.display.update()
    fpsClock.tick(60)
