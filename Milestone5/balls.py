import simplegui, random
from user305_o32FtUyCKk_0 import Vector

#constants
WIDTH = 600
HEIGHT = 400
NUM_BALLS = 5
MAX_SPEED = 5

def randCol():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return "rgb({}, {}, {})".format(r, g, b)

def randPos():
    return Vector(random.randint(0, WIDTH),
                random.randint(0, HEIGHT))

def randVel():
    return Vector(random.randint(-MAX_SPEED, MAX_SPEED), 
                random.randint(-MAX_SPEED, MAX_SPEED))

def randBall():
    return Ball(randPos(),
                randVel(),
                30,
                randCol())

class Ball:
    def __init__(self, pos, vel, radius, color):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.color = color
    
    def update(self):
        self.pos.add(self.vel)
    
    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(),
                            self.radius,
                            1,
                            self.color,
                            self.color)

class Interaction:
    def __init__(self, balls):
        self.balls = balls
        self.in_collision = set()
    
    def hit(self, b1, b2):
        sep_vec = b1.pos.copy().subtract(b2.pos)
        return sep_vec.length() < b1.radius + b2.radius
    
    def bounce(self, b1, b2):
        sep_vec = b1.pos.copy().subtract(b2.pos)

        unit = sep_vec.copy().normalize()
        v1_par = b1.vel.get_proj(unit)
        v1_perp = b1.vel.copy().subtract(v1_par)
        v2_par = b2.vel.get_proj(unit)
        v2_perp = b2.vel.copy().subtract(v2_par)

        b1.vel = v2_par + v1_perp
        b2.vel = v1_par + v2_perp
    
    def collide(self, b1, b2):
        if self.hit(b1, b2):
            b1vb2 = (b1, b2) in self.in_collision
            b2vb1 = (b2, b1) in self.in_collision
            if not b1vb2 and not b2vb1:
                self.bounce(b1, b2)
                self.in_collision.add((b1, b2))
        else:
            self.in_collision.discard((b1, b2))
            self.in_collision.discard((b2, b1))


        
    def update(self):
        for ball in self.balls:
            ball.update()
        for ball1 in self.balls:
            for ball2 in self.balls:
                if ball1 != ball2:
                    self.collide(ball1, ball2)
    
    def draw(self, canvas):
        self.update()
        for ball in self.balls:
            ball.draw(canvas)

balls = [randBall() for i in range(NUM_BALLS)]
interaction = Interaction(balls)

frame = simplegui.create_frame("Balls", WIDTH, HEIGHT)
frame.set_draw_handler(interaction.draw)
frame.start()