from pycat.core import Window,Point,Sprite,Color,KeyCode
from pycat.extensions.ldtk import LdtkLayeredLevel
from breath_first_search import BreathFirstSearch
from enum import Enum
import random

window = Window(width=1024)
map = {}

def get_cell(position : Point):
    return map.get((int(position.x),int(position.y)),None)

level = LdtkLayeredLevel.from_file(
    ldtk_file_path="level.ldtk",
    level_id="Level_0",
    image_path="level/png/",
    layer_ordering={
        "Tiles":-1
    }
)
level.render(window)

class Pacman(Sprite):
    def on_create(self):
        self.position = Point(32+64*9,32+64*4)
        self.layer = 1
        self.target = None
        self.image = "pacman.png"
    def on_update(self, dt):
        if self.target:
            self.point_toward_sprite(self.target)
            self.move_forward(4)
            if self.distance_to(self.target)<1:
                self.target = None
        else:
            if window.is_key_pressed(KeyCode.LEFT):
                self.target = get_cell(Point(self.x-64,self.y))
            if window.is_key_pressed(KeyCode.RIGHT):
                self.target = get_cell(Point(self.x+64,self.y))
            if window.is_key_pressed(KeyCode.UP):
                self.target = get_cell(Point(self.x,self.y+64))
            if window.is_key_pressed(KeyCode.DOWN):
                self.target = get_cell(Point(self.x,self.y-64))
            if not self.target:
                self.move_forward(64)
                self.target = get_cell(self.position)
                self.move_forward(-64)
    def get_current_cell(self):
        if not self.target:
            return get_cell(self.position)
        if self.target:
            return self.target 
            
class Ghost_State(Enum):
    CHASING = 1
    DAZING = 2
    GOHOME = 3
    RESTING = 4

class LWD(Sprite):
    def on_create(self):
        self.scale = 16
    def on_update(self, dt):
        if self.is_touching_sprite(pacman):
            self.delete()
class BWD(Sprite):
    def on_create(self):
        self.scale = 32
    def on_update(self, dt):
        if self.is_touching_sprite(pacman):
            ghost.state = Ghost_State.DAZING
            self.delete()

class Cell(Sprite):
    def on_create(self):
        self.scale = 32
        self.opacity = 0
        self.layer = 0
        self.add_tag("cell")
    def get_empty_neighbors(self):
        neighbors = []
        for i in [Point(64,0), Point(-64,0), Point(0,64), Point(0,-64)]:
            if get_cell(self.position+i):
                neighbors.append(get_cell(self.position+i))
        return neighbors
    def __str__(self):
        return str(int((self.x-32)/64))+","+str(int((self.y-32)/64))

for i in range(32, 1024, 64):
    for j in range(32, 640, 64):
        cell = window.create_sprite(Cell, x=i, y=j)
        if cell.is_touching_any_sprite_with_tag("ldtk_wall"):
            cell.delete()
        else:
            map[int(cell.x),int(cell.y)]= cell

for c in window.get_sprites_with_tag("cell"):
    t_position = c.position
    createe = [LWD,LWD,LWD,LWD,LWD,LWD,LWD,LWD,LWD,LWD,BWD]
    things_being_create = random.choice(createe)
    dot = window.create_sprite(things_being_create)
    dot.position = t_position

class Ghost(Sprite):
    def on_create(self):
        self.image = "ghost1.png"
        self.target = None
        self.layer = 1
        self.state = Ghost_State.CHASING
    def on_update(self, dt):
        if self.state == Ghost_State.CHASING:
            self.chasing()
        if self.state == Ghost_State.DAZING:
            self.dazed(dt)
        if self.state == Ghost_State.GOHOME:
            self.going_home()
        if self.state == Ghost_State.RESTING:
            self.resting(dt)
    def chasing(self):
        if not self.target:
            bfs = BreathFirstSearch()
            path = bfs.solve(get_cell(self.position),pacman.get_current_cell())
            if len(path) >1:
                self.target = path[1]
        if self.target:
            self.point_toward_sprite(self.target)
            self.move_forward(2)
            if self.distance_to(self.target)<=1:
                self.target = None
    def dazed(self,dt):
        if self.target:
            self.point_toward_sprite(self.target)
            self.move_forward(2)
            if self.distance_to(self.target)<=1:
                self.target = None
        self.timer = 0
        self.timer += dt
        if self.timer >= 3:
            self.state = Ghost_State.CHASING
        if self.is_touching_sprite(pacman):
            self.state = Ghost_State.GOHOME
            self.target = None
    def going_home(self):
        self.color = Color.RED
        if not self.target:
            bfs = BreathFirstSearch()
            path = bfs.solve(get_cell(self.position),get_cell(Point(32+64*7,32+64*7)))
            if len(path) >1:
                self.target = path[1]
        if self.target:
            self.point_toward_sprite(self.target)
            self.move_forward(2)
            if self.distance_to(self.target)<=1:
                self.target = None
        if self.position == Point(32+64*7,32+64*7):
            self.state = Ghost_State.RESTING
    def resting(self,dt):
        self.rest_time = 0
        self.rest_time+=dt
        if self.rest_time >=3:
            self.state = Ghost_State.CHASING
        
        

ghost = window.create_sprite(Ghost,x = 32+64*7,y = 32+64*7)
pacman = window.create_sprite(Pacman)
window.run()