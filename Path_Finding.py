from pycat.core import Window,Sprite,Point,Color
from bfs import BFS
import random

window = Window()

def Find_Empty_Cell(position):
    for c in window.get_sprites_with_tag("cell"):
        if c.distance_to(position)<2:
            return c
    return None

class Cell(Sprite):
    def on_create(self):
        self.add_tag("cell")
        self.is_barrier = random.choice([False,False,True])
        if self.is_barrier:
            self.image = "ground.png"
        else:
            self.image = "block.png"
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
        print(neighbors)
        return neighbors

for i in range(64,769,64):
    for j in range(64,705,64):
        grid = window.create_sprite(Cell,x = i,y = j)


start_block = Find_Empty_Cell(Point(64,128))
start_block.color = Color.RED
end_block = Find_Empty_Cell(Point(704,256))
end_block.color = Color.GREEN

bfs = BFS()
bfs.solve(start = start_block,end = end_block)
print(bfs.solve(start = start_block,end = end_block))
path = bfs.path_finding()
for p in path:
    if p != start_block and p != end_block:
        p.color = Color.BLUE

window.run()