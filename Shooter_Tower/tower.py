from pycat.core import Window,Sprite,Label,KeyCode
import random

window = Window()

image = ["PNG/shipBeige_damage1.png","PNG/shipBlue_damage1.png","PNG/shipGreen_damage1.png","PNG/shipPink_damage1.png"]
image2 = ["PNG/shipBeige_damage1.png","PNG/shipBlue_damage1.png","PNG/shipGreen_damage1.png","PNG/shipPink_damage1.png"]
tower_key = [KeyCode.A,KeyCode.S,KeyCode.D,KeyCode.F]
spawner_y = [110,240,370,500]
random.shuffle(spawner_y)
tower_x = [350,600,850,1100]


class Spawner(Sprite):
    def on_create(self):
        self.x = 0+self.width*0.5
        self.y = spawner_y.pop()
        self.timer = 0
        self.image = image.pop()
        self.next_spawn = random.randint(3,6)
    def on_update(self, dt):
        self.timer += dt
        if self.timer > self.next_spawn:
            target = window.create_sprite(Target_UFO)
            target.position = self.position
            target.image = self.image
            self.timer = 0
            self.next_spawn = random.randint(3,6)



class Target_UFO(Sprite):
    def on_create(self):
        self.scale = 0.5
        self.add_tag("Target")
    def on_update(self, dt):
        self.x += 6
        if self.x >= 1280:
            self.delete()
            manager.life -= 1
            life.text = "Left Chance: "+str(manager.life)


class Tower(Sprite):
    def on_create(self):
        self.x = tower_x.pop()
        self.y = 1
        self.image = image2.pop()
        self.originimg = self.image
        self.is_move = False
        self.key = tower_key.pop()
        self.scale = 0.75
    def on_update(self, dt):
        if self.is_move:
            self.y += 15
            if self.image == "PNG/shipBeige_damage1.png":
                self.image = "PNG/shipBeige_manned.png"
            elif self.image == "PNG/shipBlue_damage1.png":
                self.image = "PNG/shipBlue_manned.png"
            elif self.image == "PNG/shipGreen_damage1.png":
                self.image = "PNG/shipGreen_manned.png"
            elif self.image == "PNG/shipPink_damage1.png":
                self.image = "PNG/shipPink_manned.png"
            for sprite in self.get_touching_sprites_with_tag("Target"):
                if sprite.image == self.originimg:
                    sprite.delete()
                    self.y = 1
                    self.is_move = False
                    self.image = self.originimg
                    manager.life += 1
                    manager.gets += 1
            if self.y>=640:
                self.y = 1
                self.is_move = False
                self.image = self.originimg
                manager.life -= 2
                life.text = "Left Chance: "+str(manager.life)
        else:
            if window.is_key_down(self.key):
                self.is_move = True
                manager.shots += 1

class Manager(Sprite):
    def on_create(self):
        self.opacity = 0
        self.life = 30
        self.time = 0
        self.shots = 0
        self.gets = 0
    def on_update(self, dt):
        self.time+= dt
        if self.life <=0:
            self.score = self.gets/self.shots*self.time
            if self.score == 0:
                self.grade = "F"
            elif self.score <= 10:
                self.grade = "E"
            elif self.score <= 35:
                self.grade = "D"
            elif self.score <= 50:
                self.grade = "C"
            elif self.score <= 65:
                self.grade = "B"
            elif self.score <= 80:
                self.grade = "A"
            elif self.score <= 100:
                self.grade = "A+"
            else:
                self.grade = "S"
            print (self.grade)
            window.close()
    

window.create_sprite(Spawner)
window.create_sprite(Spawner)
window.create_sprite(Spawner)
window.create_sprite(Spawner)
window.create_sprite(Tower)
window.create_sprite(Tower)
window.create_sprite(Tower)
window.create_sprite(Tower)
manager = window.create_sprite(Manager)
life = window.create_label(text = "Left Chance: "+str(manager.life) ,x = 100,y = 540)

window.run()