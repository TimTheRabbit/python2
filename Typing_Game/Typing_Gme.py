from pycat.core import Window,Sprite,Label,KeyCode,Scheduler
from pycat.base.event import KeyEvent
import random
window = Window()

words = ["gnoy","ekim","imt","david","honjnos"]

class Typable_Label(Label):
    def on_create(self):
        window.subscribe(on_key_press = self.on_key_press_handler)
        self.text = random.choice(words)
        self.delete_enemy = False
    def on_update(self, dt: float):
        if self.text == "":
            self.delete_enemy = True
            
    def on_key_press_handler(self,key:KeyEvent):
        if len(self.text)>0 and self.text[0] == key.character:
            self.text = self.text [1:]
class Enemy(Sprite):
    def on_create(self):
        self.scale = 25
        self.label = window.create_label(Typable_Label)
        
    def on_update(self, dt):
        self.label.position = self.position
        self.point_toward_sprite(typer)
        self.move_forward(1)
        if self.label.delete_enemy == True:
            self.label.delete()
            self.delete()
        if self.is_touching_sprite(typer):
            self.delete()
            self.label.delete()
            
class Typer(Sprite):
    def on_create(self):
        self.scale_x = 100
        self.scale_y = 50
        self.x = 640
        self.y = 320
        self.color = 200,200,200
            

def create_enemy():
    window.create_sprite(Enemy)

    
     
Scheduler.update(create_enemy,3)
#enemy = window.create_sprite(Enemy)
typer = window.create_sprite(Typer)
#window.create_label(Typable_Label)
window.run()