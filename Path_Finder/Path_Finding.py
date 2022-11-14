from pycat.core import Window,Sprite,Point,Color,KeyCode
from bfs import BFS
import random
from pycat.base.event import MouseEvent
from pycat.base import MouseButton

window = Window(width=800,height=800)
start_block = None
end_block = None

def Find_Empty_Cell(position):
    for c in window.get_sprites_with_tag("cell"):
        if c.distance_to(position)<2:
            return c
    return None

class Cell(Sprite):
    def on_create(self):
        self.add_tag("cell")
        self.is_barrier = random.choice([False,False,False,True,False,True,True])
        if self.is_barrier:
            self.image = "block.png"
        else:
            self.image = "ground.png"
    def get_neighbors(self):
        neighbors = []
        right = Find_Empty_Cell(self.position + Point(64,0))
        left = Find_Empty_Cell(self.position - Point(64,0))
        up = Find_Empty_Cell(self.position + Point(0,64))
        down = Find_Empty_Cell(self.position - Point(0,64))
        if right and self.is_barrier == False:
            neighbors.append(right)
        if left and self.is_barrier == False:
            neighbors.append(left)
        if up and self.is_barrier == False:
            neighbors.append(up)
        if down and self.is_barrier == False:
            neighbors.append(down)
        return neighbors        
    def on_click(self,mouse_event:MouseEvent):
        if mouse_event.button == MouseButton.RIGHT:
            global end_block
            if end_block == None and self.is_barrier == False:
                end_block = self
                end_block.color = Color.GREEN
        if mouse_event.button == MouseButton.LEFT:
            global start_block        
            if start_block == None and self.is_barrier == False:
                start_block = self
                start_block.color = Color.RED

for i in range(64,64*12+1,64):
    for j in range(64,64*10+1,64):
        grid = window.create_sprite(Cell,x = i,y = j)

class Agent(Sprite):
    def on_create(self):
        self.path = None
        self.index = 1
        self.image = "NotAScam.jpg"
        self.scale = 0.05
        self.layer = 1
    def on_update(self, dt):
        if self.index >= len(self.path):
            self.delete()
            return
        self.target_cell = self.path[self.index]
        self.point_toward_sprite(self.target_cell)
        self.move_forward(1)
        if self.distance_to(self.target_cell)<2:
            self.index+=1

bfs = BFS()
class Manager(Sprite):
    def on_update(self, dt):
        global start_block
        global end_block
        if window.is_key_down(KeyCode.S) and start_block != None and end_block != None:
            path = bfs.solve(start = start_block,end = end_block)
            if path == []:
                for c in window.get_sprites_with_tag("cell"):
                    c.color = Color.PURPLE
            else:
                agent = window.create_sprite(Agent)
                agent.position = start_block.position
                path.reverse()
                agent.path = path
                for p in path:
                    if p != start_block and p != end_block:
                        p.color = Color.BLUE
        if window.is_key_down(KeyCode.R):
            for c in window.get_sprites_with_tag("cell"):
                c.delete()
            for i in range(64,64*12+1,64):
                for j in range(64,64*10+1,64):
                    grid = window.create_sprite(Cell,x = i,y = j)
            start_block = None
            end_block = None
                    
window.create_sprite(Manager)           

window.run()