import random
from pycat.core import Window,Sprite,RotationMode,Scheduler,KeyCode,Color,Label
window = Window(width=1200 ,height=600,enforce_window_limits= False)

class WrapSprite(Sprite):
    def wrapping(self):
        if self.x >= window.width + self.width*0.5:
            self.x  = 0 - self.width *0.5
        elif self.x <= 0 - self.width*0.5:
            self.x  = window.width + self.width *0.5

        elif self.y >= window.height + self.width*0.5:
            self.y  = 0 - self.width *0.5
        elif self.y <= 0 - self.width*0.5:
            self.y  = window.height+self.width *0.5

class Ship(WrapSprite):
    def on_create(self):
        self.speed = 0
        self.image = "ship_idle.png"
        self.position = 600,300
        self.rotation_mode = RotationMode.MIRROR
        self.add_tag("ship")
        self.score = 0
    def on_update(self, dt):
        self.speed *= 0.99
        self.move_forward(self.speed)
        if window.is_key_pressed(KeyCode.SPACE):
            self.speed = min(self.speed+0.08,10.01)
        if window.is_key_pressed(KeyCode.M):
            self.speed = max(self.speed-0.08,-10.01)
        if window.is_key_pressed(KeyCode.LEFT):
            self.rotation += -5
        if window.is_key_pressed(KeyCode.RIGHT):
            self.rotation += 5
        self.wrapping()
        if self.speed >= 1 >= -1 :
            self.image = "ship_thrust.png"
        else:
            self.image = "ship_idle.png"
        if window.is_key_down(KeyCode.S):
            bullet = window.create_sprite(Bullet)
            bullet.position = self.position
            bullet .rotation = self.rotation

        
class Bullet(Sprite):
    def on_create(self):
        self.image = "ufo.png"
        self.add_tag("bullet")
        self.scale = 0.5
    def on_update(self, dt):
        self.move_forward(10)
        if self.is_touching_window_edge():
            self.delete()

astroid_image = ["big1.png","big2.png","big3.png"]
astroid_image_two = ["med1.png","med2.png","med3.png"]
astroid_image_three = ["small1.png","small2.png","small3.png"]
def Spawn_astroid():
    astroid = window.create_sprite(Astroid)
    dice = random.randint(0,1)
    if dice ==1 :
        astroid.position = (0 - astroid.width * 0.5 ,random.randint(0,600))
    if dice == 0:
        astroid.position = (0 - astroid.height * 0.5 ,random.randint(0,1200))
    astroid.point_toward_sprite(ship)
    rotation_mult = random.randint(0,1)
    astroid.rotation = astroid.rotation ** rotation_mult
    astroid.image = random.choice(astroid_image)

class Freezingpickup(Sprite):
    def on_create(self):
        self.goto_random_position()
        self.image = "NotAScam.jpg"
        self.scale = 0.05
    def on_update(self, dt):
        if self.is_touching_any_sprite_with_tag("ship"):
            self.is_visible = False
            global astroid_speed
            astroid_speed = 1
            Scheduler.wait(5,self.Defrozen)
            

    def Defrozen(self):
        global astroid_speed
        astroid_speed = 10
        self.is_visible = True
        self.goto_random_position()

class Pop_Big(Label):
    def on_create(self):
        self.text = "200"    
        self.is_growing = True
    def on_update(self, dt):
        if self.is_growing and self.font_size<=50:
            self.font_size +=1  
        elif self.is_growing and self.font_size>50:
            self.is_growing = False
        elif not self.is_growing:
            self.font_size -= 1
            if self.font_size<0:
                self.delete()
class Pop_Med(Label):
    def on_create(self):
        self.text = "200"    
        self.is_growing = True
    def on_update(self, dt):
        if self.is_growing and self.font_size<=50:
            self.font_size +=1  
        elif self.is_growing and self.font_size>50:
            self.is_growing = False
        elif not self.is_growing:
            self.font_size -= 1
            if self.font_size<0:
                self.delete()
class Pop_Small(Label):
    def on_create(self):
        self.text = "200"    
        self.is_growing = True
    def on_update(self, dt):
        if self.is_growing and self.font_size<=50:
            self.font_size +=1  
        elif self.is_growing and self.font_size>50:
            self.is_growing = False
        elif not self.is_growing:
            self.font_size -= 1
            if self.font_size<0:
                self.delete()

astroid_speed = 10
class Astroid(WrapSprite):
    def on_create(self):
        self.color=Color.random_rgb()
    def on_update(self, dt):
        global astroid_speed
        self.move_forward(astroid_speed)
        self.wrapping()

        if self.is_touching_any_sprite_with_tag("ship"):
            pass

        for b in self.get_touching_sprites_with_tag("bullet"):
            b.delete()
            if "big" in self.image:
                for rotation in (90,-90):
                    astroid = window.create_sprite(Astroid)
                    astroid.position = self.position
                    astroid.rotation = rotation + self.rotation
                    astroid.image = random.choice(astroid_image_two)
                    ship.score += 200
                    score_label.text = "Score: "+str(ship.score)
                    pop_big = window.create_label(Pop_Big)
                    pop_big.position = self.position
                    
            elif "med" in self.image:
                for rotation in (90,-90):
                    astroid = window.create_sprite(Astroid)
                    astroid.position = self.position
                    astroid.rotation = rotation + astroid.rotation
                    astroid.image = random.choice(astroid_image_three)       
                    ship.score +=  400
                    score_label.text = "Score: "+str(ship.score)
                    pop_med = window.create_label(Pop_Med)
                    pop_med.position = self.position
            ship.score += 600
            score_label.text = "Score: "+str(ship.score)
            pop_small = window.create_label(Pop_Small)
            pop_small.position = self.position
            self.delete()
            



Scheduler.update(Spawn_astroid,5)
ship = window.create_sprite(Ship)
score_label = window.create_label(x = 320,y=570,text = "Hello dear astros,you haven't ever hit an asteroid!!")
window.create_label(x = 320,y=600,text = "World Record : 314159265358979323846264338141421260 ")
window.create_sprite(Freezingpickup)
window.run()