from os import remove
from numpy import append
from pycat.core import Window,Sprite,Color
import random
window = Window(width=700,height=750)

solution = [Color.RED,Color.BLUE,Color.GREEN,Color.YELLOW,Color.CYAN,Color.AMBER,Color.PURPLE]
random.shuffle(solution)
pegs = []

class Peg(Sprite):
    def on_create(self):
        self.color_list = [Color.RED,Color.BLUE,Color.GREEN,Color.YELLOW,Color.CYAN,Color.AMBER,Color.PURPLE]
        self.color = Color.WHITE
        self.scale = 0.7
        self.is_clickable = True
        self.image = "enemy_E.png"
    def on_left_click(self):
        if self.is_clickable:
            self.color = self.color_list[0]
            self.color_list.append(self.color_list[0])
            self.color_list.remove(self.color_list[0])

target_y = 700
class Check_Button(Sprite):
    def on_create(self):
        self.position = (550,50)
        self.scale = 0.5
        self.image = "icon_plusSmall.png"
    def on_left_click(self):
        self.compare()
    def compare(self):
        get_right = 0
        get_right_color = 0
        for i in range(5):
            self.clone(pegs[i].x,pegs[i].color)  
            if pegs[i].color == solution[i]:
                get_right += 1
            else:
                for j in range(5):
                    if pegs[i].color == solution[j]:
                        get_right_color += 1                       
        print(get_right)
        global target_y
        window.create_label(text = str(get_right,x = 450,y = target_y))
        window.create_label(text = str(get_right_color,x = 550,y = target_y))
        #self.create_pin(get_right,get_right_color)
        target_y -= 50
        if target_y < 100:
            window.close()
    def clone(self,x,tar_color):
        clone = window.create_sprite(Peg)
        clone.is_clickable = False
        clone.color = tar_color
        clone.scale = 0.3
        global target_y
        clone.position = (x,target_y)
        clone.image = "station_A.png"
    #def create_pin(self,get_right,get_color):
        # pins = []
        # global target_y
        # for x in range(450,500):
        #     for y in range(target_y+15,target_y-15):
        #         create_obj = window.create_sprite(Pin,x = x,y = y)
        #         pins.append(create_obj)
        # for _ in range(get_right):
        #     pins[0].color = Color.RED
        #     pins.remove(pins[0])
        # for _ in range(get_color):
        #     pins[0].color = Color.WHITE
        #     pins.remove(pins[0])


        
#class Pin(Sprite):
    #def on_create(self):
     #   self.scale = 0.1
      #  self.image = "icon_exclamationSmall.png"






window.create_sprite(Check_Button)
peg1 = window.create_sprite(Peg)
peg1.position = (50,50)
pegs.append(peg1)
peg2 = window.create_sprite(Peg)
peg2.position = (150,50)
pegs.append(peg2)
peg3 = window.create_sprite(Peg)
peg3.position = (250,50)
pegs.append(peg3)
peg4 = window.create_sprite(Peg)
peg4.position = (350,50)
pegs.append(peg4)
peg5 = window.create_sprite(Peg)
peg5.position = (450,50)
pegs.append(peg5)
window.run()