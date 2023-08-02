import arcade
from dataclasses import dataclass
import math
import random


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CIRCLE_RADIUS = 25

def clamp(a, min, max):
    if a < min: return min
    elif a > max: return max
    else: return a

@dataclass
class Vector:
    x: float
    y: float

    def __add__(self, v):
        return Vector(self.x+v.x, self.y+v.y)
    def __sub__(self, v):
        return Vector(self.x-v.x, self.y-v.y)
    def dist(self, v):
        return math.sqrt((self-v).dot(self-v))
    def dot(self, v):
        return self.x*v.x + self.y*v.y
    def __truediv__(self, a):
        return Vector(self.x/a, self.y/a)
    def __mul__(self, a):
        return  Vector(self.x*a, self.y*a)
    def length(self):
        return math.sqrt(self.dot(self))
    def normalized(self):
        if self.length() < .00001:
            return self
        return self/self.length()

@dataclass
class Circle:
    position: Vector
    velocity: Vector
    radius: float
    color: int

colors = [arcade.color.WHITE_SMOKE, arcade.color.BABY_BLUE, arcade.color.RACKLEY, arcade.color.ALABAMA_CRIMSON]

class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, "Simple Arcade Game")
        self.left = self.right = self.up = self.down = False
        self.player = Circle(Vector(SCREEN_WIDTH//2,SCREEN_HEIGHT//2), Vector(0,0), 20, 0)
        self.entities = [self.player]

        for i in range(100):
            self.entities.append(Circle(Vector(random.randrange(SCREEN_WIDTH), random.randrange(SCREEN_HEIGHT)),
                                        Vector(random.randrange(100), random.randrange(100)),
                                        random.randrange(10,20),
                                        random.randrange(1,len(colors))))

    def on_draw(self):
        arcade.start_render()
        for e in self.entities:
            arcade.draw_circle_filled(e.position.x, e.position.y, e.radius, colors[e.color])
    

    def on_update(self, delta_time):
        speed = 200
        vel = Vector(0,0)
        if self.left:
            vel.x = -1
        if self.right:
            vel.x = 1
        if self.up:
            vel.y = 1
        if self.down:
            vel.y = -1
        
        vel = vel.normalized()
        self.player.velocity = vel * speed

        for e in self.entities:
            e.position += e.velocity * delta_time

            if e.position.x < 0 or e.position.x >= SCREEN_WIDTH:
                e.velocity.x = -e.velocity.x
                e.position.x = clamp(e.position.x, 0, SCREEN_WIDTH-1)
            if e.position.y < 0 or e.position.y >= SCREEN_HEIGHT:
                e.velocity.y = -e.velocity.y
                e.position.y = clamp(e.position.y, 0, SCREEN_HEIGHT-1)
        
        

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.left = True
        elif key == arcade.key.RIGHT:
            self.right = True
        elif key == arcade.key.UP:
            self.up = True
        elif key == arcade.key.DOWN:
            self.down = True

        # Keep the circle within the screen boundaries
        # if self.circle_x < CIRCLE_RADIUS:
        #     self.circle_x = CIRCLE_RADIUS
        # elif self.circle_x > SCREEN_WIDTH - CIRCLE_RADIUS:
        #     self.circle_x = SCREEN_WIDTH - CIRCLE_RADIUS
        # if self.circle_y < CIRCLE_RADIUS:
        #     self.circle_y = CIRCLE_RADIUS
        # elif self.circle_y > SCREEN_HEIGHT - CIRCLE_RADIUS:
        #     self.circle_y = SCREEN_HEIGHT - CIRCLE_RADIUS
    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.LEFT:
            self.left = False
        elif key == arcade.key.RIGHT:
            self.right = False
        elif key == arcade.key.UP:
            self.up = False
        elif key == arcade.key.DOWN:
            self.down = False 

def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()

if __name__ == "__main__":
    main()