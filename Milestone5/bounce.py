import simplegui, math
from user305_o32FtUyCKk_0 import Vector

class Wall:
    def __init__(self, x, border, color):
        self.x = x
        self.border = border
        self.color = color
        self.normal = Vector(1,0)
        self.edge_r = x + self.border
        self.edge_l = x - self.border
        
        self.inputx = str(input("Enter either 'l' or 'r': "))
        if self.inputx != 'l' and self.inputx != 'r':
            print("Error wrong character")
       
    def draw(self, canvas):
        if self.inputx == 'l': 
            self.x = 0
        elif self.inputx == 'r':
            self.x = 600
        else:
            canvas.draw_text('Error wrong character', 
                             (CANVAS_WIDTH/2, CANVAS_HEIGHT/2), 
                             20, 'Red')
        canvas.draw_line((self.x, 0),
                         (self.x, CANVAS_HEIGHT),
                         self.border*2+1,
                         self.color)
           
            
    def hit_l(self, ball):
        h = (ball.offset_l() <= self.x + self.border) 
        return h
    
    def hit_r(self, ball):
        h = (ball.offset_r() >= self.x - self.border)
        return h
    

class Ball:
    def __init__(self, pos, vel, radius, border, color):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.border = 1
        self.color = color

    def offset_l(self):
        return self.pos.x - self.radius
    
    def offset_r(self):
        return self.pos.x + self.radius

    def update(self):
        self.pos.add(self.vel)

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(),
                           self.radius,
                           self.border,
                           self.color,
                           self.color)

    def bounce(self, normal):
        self.vel.reflect(normal)

class Interaction:
    def __init__(self, wall, ball):
        self.ball = ball
        self.wall = wall
        self.in_collision = False

    def update(self):
        self.ball.update()
        if self.wall.inputx == 'l': 
            if self.wall.hit_l(self.ball):
                if not self.in_collision:
                    self.ball.bounce(self.wall.normal)
                    self.in_collision = True
            else:
                self.in_collision = False
        if self.wall.inputx == 'r':
            if self.wall.hit_r(self.ball):
                if not self.in_collision:
                    self.ball.bounce(self.wall.normal)
                    self.in_collision = True
            else:
                self.in_collision = False
        

    def draw(self, canvas):
        self.update()
        self.ball.draw(canvas)
        self.wall.draw(canvas)

# The canvas dimensions
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400

# Initial position and velocity of the ball
p = Vector(300,100)
v = Vector(4,1)

# Creating the objects

b = Ball(p, v, 20, 10, 'blue')
w = Wall(600, 5, 'red')
i = Interaction(w, b)


# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("ball-wall", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(i.draw)

# Start the frame animation
frame.start()
