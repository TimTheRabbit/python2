from turtle import speed
from pycat.core import Window,Point,Sprite,Color,KeyCode,Scheduler
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
    NOTHING = 5

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
            ghosts = window.get_sprites_with_tag("ghost")
            for g in ghosts:
                g.state = Ghost_State.DAZING
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
    createe = [LWD,LWD,LWD,LWD,LWD,LWD,LWD,LWD,LWD,LWD,BWD,LWD,LWD,LWD,LWD,LWD,LWD,LWD,LWD,LWD,LWD]
    things_being_create = random.choice(createe)
    dot = window.create_sprite(things_being_create)
    dot.position = t_position

class Ghost(Sprite):
    def on_create(self):
        self.speed:float
        self.start_position:Point
        self.rester = 0
        self.target = None
        self.add_tag("ghost")
        self.layer = 1
        self.timer = 0
        self.rest_time:float
        self.state = Ghost_State.NOTHING 
        self.color = Color.WHITE       
    def start(self):
        self.state = Ghost_State.CHASING   
    def on_update(self, dt):
        if self.state == Ghost_State.CHASING:
            self.timer = 0
            self.rest_time = 0
            self.chasing()
        if self.state == Ghost_State.DAZING:
            self.dazed()
            self.timer += dt
        if self.state == Ghost_State.GOHOME:
            self.going_home()
            self.timer = 0
        if self.state == Ghost_State.RESTING:
            self.resting()
            self.rest_time += dt
            print(self.rest_time)
    def chasing(self):
        self.color = Color.WHITE
        if not self.target:
            bfs = BreathFirstSearch()
            path = bfs.solve(get_cell(self.position),pacman.get_current_cell())
            if len(path) >1:
                self.target = path[1]
        if self.target:
            self.point_toward_sprite(self.target)
            self.move_forward(self.speed)
            if self.distance_to(self.target)<=1:
                self.target = None
    def dazed(self):
        self.color = Color.BLUE
        if self.target:
            self.point_toward_sprite(self.target)
            self.move_forward(2)
            if self.distance_to(self.target)<=1:
                pacpos = pacman.position
                self.finding_dazing_target()
                self.pro_target = (get_cell(Point(32+64*self.daze_x,32+64*self.daze_y)))
                if self.pro_target and self.pro_target.distance_to(pacpos)>128:
                    bfs = BreathFirstSearch()
                    path = bfs.solve(get_cell(self.position),self.pro_target)
                    if len(path) >1:
                        self.target = path[1]
        if self.timer >= self.rester:
            self.state = Ghost_State.CHASING
        if self.is_touching_sprite(pacman):
            self.state = Ghost_State.GOHOME
    def finding_dazing_target(self):
        self.daze_x = random.randint(1,14)
        self.daze_y = random.randint(1,7)
    def going_home(self):
        self.color = Color.GREEN
        if not self.target:
            print("solving")
            bfs = BreathFirstSearch()
            path = bfs.solve(get_cell(self.position),get_cell(self.start_position))
            if len(path) > 1:
                self.target = path[1]
        if self.target:
            print("moving")
            self.point_toward_sprite(self.target)
            self.move_forward(self.speed*2)
            if self.distance_to(self.target)<=1:
                self.target = None
        if self.distance_to(self.start_position) <=2:
            self.rotation = 0
            self.state = Ghost_State.RESTING            
    def resting(self):
        if self.rest_time >=self.rester:
            self.state = Ghost_State.CHASING        

pinky = window.create_sprite(Ghost,x = 32+64*7,y = 32+64*7)
Scheduler.wait(2,pinky.start)
blinky = window.create_sprite(Ghost,x = 32+64*6,y = 32+64*7)
blinky.state = Ghost_State.CHASING
pinky.speed = 2
pinky.rester = 3
pinky.image = "ghost1.png"
blinky.image = "ghost2.png"
pinky.start_position = pinky.position
blinky.start_position = blinky.position
blinky.rester = 2
blinky.speed = 4
pacman = window.create_sprite(Pacman)
window.run()