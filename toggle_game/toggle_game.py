from pycat.core import Window,Sprite,Color
import random

window=Window(width=1000,height=1000)

def complete_check():
    for i in range(1,9):
        for j in range(1,9):
            if grid[i][j].color == Color.WHITE:
                return False
    print("finish")
    return True

class Square(Sprite):
    def on_create(self):
        self.color = Color.RED
        self.scale = 100

    def on_left_click(self):
        print(i+1,j)
        grid[self.i+1][self.j].toggle()
        grid[self.i-1][self.j].toggle()
        grid[self.i][self.j+1].toggle()
        grid[self.i][self.j-1].toggle()
        complete_check()
        
    def toggle(self):
        if self.color == Color.RED:
            self.color = Color.WHITE
        else:
            self.color = Color.RED

class UnSquare(Sprite):
    def on_create(self):
        self.color = Color.PURPLE
        self.scale = 100
    def toggle(self):
        pass


grid = []
for i in range(10):
    grid.append([None]*10)

for i in range(10):
    for j in range(10):
        if i == 0 or i == 9 or j == 0 or j == 9:
            unsquare = window.create_sprite(UnSquare)
            grid[i][j] = unsquare
            unsquare.x = i*100+25
            unsquare.y = j*100+25

        else:
            square = window.create_sprite(Square)
            grid[i][j] = square
            square.x = i*100+25
            square.y = j*100+25
            square.i = i
            square.j = j
for i in range(10):
    a = random.randint(1,9) 
    b = random.randint(1,9)
    grid[a][b].on_left_click()


    

window.run()