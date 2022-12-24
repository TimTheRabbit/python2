from pycat.core import Window,Sprite,Label,Color,Point,Scheduler,KeyCode,RotationMode
from pycat.extensions.ldtk import LdtkLayeredLevel

window = Window(width=1024,height=512)

level = LdtkLayeredLevel.from_file(
    ldtk_file_path="level.ldtk",
    level_id="Level_0",
    image_path="level/png/",
    layer_ordering={
        "Tiles":-1
    }
)
level.render(window,scale=2,debug_entities=True)

class WrapSprite(Sprite):
    def wrap(self):
        if self.y == window.height:
            self.y = 0
        elif self.y == 0:
            self.y = window.height
class Moveable_Wall(Sprite):
    pass
class Player1(WrapSprite):
    def on_create(self):
        self.keep_hold = 0
        self.holding = False
        self.layer = 0
        self.scale = 0.01
        self.bullet = 0
        self.get_SP = 0
        self.SP = False
        self.rotation_mode = RotationMode.MIRROR
    def drop_power(self):
        if self.holding == True:
            power.random()
            self.holding = False
    def set_key(self,up,down,left,right,shoot):
        self.up_key = up
        self.down_key = down
        self.left_key = left
        self.right_key = right
        self.shoot_key = shoot
    def player_collide(self):
        for t in self.tags:
            if t == "p1":       
                if self.is_touching_any_sprite_with_tag("p2"):
                    p2.y+=10
                    self.drop_power()
            if t == "p2":       
                if self.is_touching_any_sprite_with_tag("p1"):
                    p1.y+=10
                    self.drop_power()
    def shoot(self):
        if self.bullet > 0:
            self.bullet -= 1
            my_bullet = window.create_sprite(Bullet_Shooting)
            print("shoot")
            my_bullet.position = self.position
            my_bullet.rotation = self.rotation
            if "p1" in self.tags:
                my_bullet.add_tag("p1")
            elif "p2" in self.tags:
                my_bullet.add_tag("p1")
            my_bullet.add_tag("bullet")
    def on_update(self, dt):
        self.wrap()
        self.get_SP += 0.000000001
        if window.is_key_pressed(self.up_key):
            self.y+=10
            if self.is_touching_any_sprite_with_tag("ldtk_wall"):
                print("touching")
                self.y -= 10
                self.drop_power()
            self.player_collide()
        elif window.is_key_pressed(self.down_key):
            self.y -= 10
            if self.is_touching_any_sprite_with_tag("ldtk_wall"):
                self.y += 10
                print("touching")
                self.drop_power()
            self.player_collide()
        if window.is_key_pressed(self.left_key):
            self.x -= 10
            self.rotation = 180
            if self.is_touching_any_sprite_with_tag("ldtk_wall"):
                print("touching")
                self.x += 10
                self.drop_power()
            self.player_collide()
        if window.is_key_pressed(self.right_key):
            self.x += 10
            self.rotation = 0
            if self.is_touching_any_sprite_with_tag("ldtk_wall"):
                print("touching")
                self.x -= 10
                self.drop_power()
            self.player_collide()
        if window.is_key_down(self.shoot_key):
            self.shoot()
        if self.keep_hold >= 50:
            window.close()       

class Target(Sprite):
    def on_create(self):
        self.image = "target.png"
        self.time = 0
        self.layer = 0
        self.scale = 0.035
        self.goto_random_position_in_region(32+128,32+128,1024-128,512-128)
    def on_update(self, dt):
        if self.is_touching_any_sprite_with_tag("p1"):
            p1.holding=True
        if self.is_touching_any_sprite_with_tag("p2"):
            p2.holding=True           
        if p1.holding ==True:
            p1.keep_hold+=dt
            self.position = p1.position
            self.layer =1
        if p2.holding ==True:
            p2.keep_hold+=dt
            self.position = p2.position
            self.layer =1
    def random(self):
        self.goto_random_position_in_region(32+128,32+128,1024-128,512-128)
class Bullet_Collection(Sprite):
    def on_create(self):
        self.image = "BULLET.png"
        self.scale = 0.05
        self.goto_random_position()
        self.time =0
    def on_update(self, dt):
        self.time+=dt
        if self.time>=5:
            self.delete()
        if self.is_touching_any_sprite_with_tag("p1"):
            p1.bullet += 10
            print(p1.bullet)
            print(p2.bullet)
            self.delete()
        if self.is_touching_any_sprite_with_tag("p2"):
            p2.bullet += 10
            print(p1.bullet)
            print(p2.bullet)
            self.delete()
class Bullet_Shooting(Sprite):
    def on_create(self):
        self.image = "BULLET.png"
        self.scale = 0.01
        self.time = 0
    def on_update(self,dt):
        self.time += dt
        self.move_forward(50)
        if self.is_touching_any_sprite_with_tag("ldtk_wall"):
            self.delete()
        if self.time >= 10:
            self.delete()
        if "p1" in self.tags:
            if self.is_touching_any_sprite_with_tag("p2"):
                p2.drop_power()
                self.delete()
                print("p2 got shot")
        if "p2" in self.tags:
            if self.is_touching_any_sprite_with_tag("p1"):
                p1.drop_power()
                print("p1 got shot")
                self.delete()
def Spawn_Bullet():
    window.create_sprite(Bullet_Collection)
Scheduler.update(Spawn_Bullet,5)

power = window.create_sprite(Target)
p1 = window.create_sprite(Player1,x =64,y = 160)
p1.image = "P1.png"
p1.add_tag("p1")
p1.set_key(KeyCode.W,KeyCode.S,KeyCode.A,KeyCode.D,KeyCode.Z)
p2 = window.create_sprite(Player1,x =960,y = 380)
p2.image = "P2.png"
p2.rotation = 180
p2.add_tag("p2")
p2.set_key(KeyCode.UP,KeyCode.DOWN,KeyCode.LEFT,KeyCode.RIGHT,KeyCode.NUM_0)
window.run()