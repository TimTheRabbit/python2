from pycat.core import Window,Sprite,Label,Color,Point,Scheduler,KeyCode,RotationMode
from pycat.extensions.ldtk import LdtkLayeredLevel
import pyglet

window = Window(width=1024,height=512)
level = LdtkLayeredLevel.from_file(
    ldtk_file_path="level.ldtk",
    level_id="Level_0",
    image_path="level/png/",
    layer_ordering={
        "Tiles":-1
    }
)
level.render(window,scale=2,debug_entities=False)

end_cond = False

class Win_Label(Label):
    def on_create(self):
        self.is_visible = False
        self.font_size = 50
        self.text = ""

class WrapSprite(Sprite):
    def wrap(self):
        if self.y == window.height:
            self.y = 0
        elif self.y == 0:
            self.y = window.height
class Player(WrapSprite):
    def on_create(self):
        self.keep_hold = 0
        self.holding = False
        self.layer = 0
        self.scale = 0.01
        self.bullet = 0
        self.get_SP = 0
        self.SP = False
        self.rotation_mode = RotationMode.MIRROR
        self.joy_x = 0
        self.joy_y = 0
        self.button = None
    def drop_power(self):
        if self.holding == True:
            print(str(self.tags)+' dropped the power')
            power.random()
            self.holding = False
    def set_key(self,up,down,left,right,shoot,pick_up,super_power):
        self.up_key = up
        self.down_key = down
        self.left_key = left
        self.right_key = right
        self.shoot_key = shoot
        self.pick_key = pick_up
        self.super = super_power
    def check_player_collision(self, push_direction):
        if 'p1' in self.tags and self.is_touching_any_sprite_with_tag("p2"):
            p2.position+=push_direction*50
            if p2.is_touching_any_sprite_with_tag("ldtk_wall"):
                p2.position+=push_direction*-50
            print("p1 collide with p2")
            p2.drop_power()
        if 'p2' in self.tags and self.is_touching_any_sprite_with_tag("p1"):
            p1.position+=push_direction*50
            if p1.is_touching_any_sprite_with_tag("ldtk_wall"):
                p1.position+=push_direction*-50
            print("p2 collide with p1")
            p1.drop_power()
    def shoot(self):
        if self.bullet > 0 and self.holding == False:
            self.bullet -= 1
            my_bullet = window.create_sprite(Bullet_Shooting)
            my_bullet.position = self.position
            my_bullet.rotation = self.rotation
            if "p1" in self.tags:
                my_bullet.add_tag("p1b")
                p1_bullet.text = "Left Bullet: "+str(round(p1.bullet,1))
            elif "p2" in self.tags:
                my_bullet.add_tag("p2b")
                p2_bullet.text = "Left Bullet: "+str(round(p2.bullet,1))
            my_bullet.add_tag("bullet")
    def super_power(self):
        if self.get_SP >= 1:
            if "p1" in self.tags:
                print("p1 super")
                if p2.keep_hold > 0:
                    p2.keep_hold *= 0.5
                    p2h.text = "Keeping Time: "+str(round(p2.keep_hold,1))
                    self.get_SP = 0
                else:
                    p2.bullet *= 0.5
                    p2_bullet.text = "Left Bullet: "+str(round(p2.bullet,1))
                    self.get_SP = 0
            elif "p2" in self.tags:
                print("p2 super")
                if p1.keep_hold > 0:
                    p1.keep_hold *= 0.5
                    p1h.text = "Keeping Time: "+str(round(p1.keep_hold,1))
                    self.get_SP = 0
                else:
                    p1.bullet *= 0.5
                    p1_bullet.text = "Left Bullet: "+str(round(p1.bullet,1))
                    self.get_SP = 0
    def change_bar_costume(self,target_sprite):
        if self.get_SP == 0:
            target_sprite.scale_x = 0
        if self.get_SP <= 0.05 and self.get_SP > 0.02:
            target_sprite.scale_x = 0.03
        elif self.get_SP <= 0.075 and self.get_SP > 0.05:
            target_sprite.scale_x = 0.07
        elif self.get_SP <= 0.1 and self.get_SP > 0.075:
            target_sprite.scale_x = 0.1
        elif self.get_SP <= 0.15 and self.get_SP > 0.1:
            target_sprite.scale_x = 0.15
        elif self.get_SP <= 0.2 and self.get_SP > 0.15:
            target_sprite.scale_x = 0.2
        elif self.get_SP <= 0.25 and self.get_SP > 0.2:
            target_sprite.scale_x = 0.25
        elif self.get_SP <= 0.33 and self.get_SP > 0.25:
            target_sprite.scale_x = 0.3    
        elif self.get_SP <= 0.4 and self.get_SP > 0.33:
            target_sprite.scale_x = 0.4
        elif self.get_SP <= 0.45 and self.get_SP > 0.4:
            target_sprite.scale_x = 0.45
        elif self.get_SP <= 0.5 and self.get_SP > 0.45:
            target_sprite.scale_x = 0.5
        elif self.get_SP <= 0.55 and self.get_SP > 0.5:
            target_sprite.scale_x = 0.55
        elif self.get_SP <= 0.6 and self.get_SP > 0.55:
            target_sprite.scale_x =0.6
        elif self.get_SP <= 0.75 and self.get_SP > 0.6:
            target_sprite.scale_x = 0.75
        elif self.get_SP <= 0.8 and self.get_SP > 0.75:
            target_sprite.scale_x = 0.8
        elif self.get_SP <= 0.85 and self.get_SP > 0.8:
            target_sprite.scale_x = 0.85
        elif self.get_SP <= 0.9 and self.get_SP > 0.85:
            target_sprite.scale_x = 0.9
        elif self.get_SP <= 0.95 and self.get_SP > 0.9:
            target_sprite.scale_x = 0.97
    def on_joyaxis_motion(self,joystick,axis,value):
        if axis == "x":
            self.joy_x = value
        if axis == "y":
            self.joy_y = value
    def on_joybutton_press(self,joystick,button):
        print("button: ",button)
        self.button = button
    def on_update(self, dt):
        global end_cond
        if end_cond== True:
            self.delete()
        self.wrap()
        if window.is_key_down(self.super) or self.button == 0:
            self.super_power()
            self.button = None
        if self.get_SP < 1:
            if "p1" in self.tags:
                self.change_bar_costume(color_bar1)
                color_bar1.x = 100 - (100-color_bar1.width)*0.5
            elif "p2" in self.tags:
                self.change_bar_costume(color_bar2)
                color_bar2.x = 874 + (100-color_bar2.width)*0.5
        else:
            print(str(self.tags) + " SP set to true" )
            if "p1" in self.tags:
                color_bar1.scale_x = 1
                color_bar1.x = 100 - (100-color_bar1.width)*0.5
            elif "p2" in self.tags:
                color_bar2.scale_x = 1
                color_bar2.x = 874 + (100-color_bar2.width)*0.5
        if window.is_key_pressed(self.up_key) or self.joy_y < -0.2:
            self.y+=10
            if self.get_SP<1:
                self.get_SP += 0.0008
            if self.is_touching_any_sprite_with_tag("ldtk_wall"):
                self.y -= 10
                self.drop_power()
            self.check_player_collision(Point(0,1))
        elif window.is_key_pressed(self.down_key) or self.joy_y > 0.2:
            self.y -= 10
            if self.get_SP<1:
                self.get_SP += 0.0008
            if self.is_touching_any_sprite_with_tag("ldtk_wall"):
                self.y += 10
                self.drop_power()
            self.check_player_collision(Point(0,-1))
        elif window.is_key_pressed(self.left_key) or self.joy_x < -0.2:
            self.x -= 10
            if self.get_SP<1:
                self.get_SP += 0.0008
            self.rotation = 180
            if self.is_touching_any_sprite_with_tag("ldtk_wall"):
                self.x += 10
                self.drop_power()
            self.check_player_collision(Point(-1,0))
        elif window.is_key_pressed(self.right_key) or self.joy_x > 0.2:
            self.x += 10
            if self.get_SP<1:
                self.get_SP += 0.0008
            self.rotation = 0
            if self.is_touching_any_sprite_with_tag("ldtk_wall"):
                self.x -= 10
                self.drop_power()
            self.check_player_collision(Point(1,0))
        if window.is_key_down(self.shoot_key) or self.button == 1:
            self.shoot()
            self.button = None
        if self.keep_hold >= 10:
            print("one win")
            win_l = window.create_label(Win_Label)
            win_l.position = self.position
            if "p1" in self.tags:
                win_l.is_visible =True
                win_l.color = Color.BLUE
                win_l.text = "P1 win the great battle!!!" 

                end_cond = True  
            else:
                win_l.is_visible =True
                win_l.color = Color.RED
                win_l.text = "P2 win the great battle!!!"  

                end_cond = True
class Power(Sprite):
    def on_create(self):
        self.image = "target.png"
        self.time = 0
        self.layer = 0
        self.scale = 0.035
        self.goto_random_position_in_region(32+128,32+128,1024-128,512-128)
    def on_update(self, dt):
        global end_cond
        if end_cond== True:
            self.delete()
        if self.is_touching_any_sprite_with_tag("p1") and (window.is_key_down(p1.pick_key) or p1.button == 2):
            p1.holding=True
            p1.button = None
        if self.is_touching_any_sprite_with_tag("p2") and (window.is_key_down(p2.pick_key) or p2.button == 2):
            p2.holding=True  
            p2.button = None         
        if p1.holding ==True:
            p1.keep_hold+=dt
            p1h.text = "Keeping Time: "+str(round(p1.keep_hold,1))
            self.position = p1.position
            self.layer =1
        if p2.holding ==True:
            p2.keep_hold+=dt
            self.position = p2.position
            p2h.text = "Keeping Time: "+str(round(p2.keep_hold,1))
            self.layer =1
    def random(self):
        print('sending power to random position')
        self.goto_random_position_in_region(32+128,32+128,1024-128,512-128)
        while(self.is_touching_any_sprite_with_tag("p1") or self.is_touching_any_sprite_with_tag("p2")):
            self.goto_random_position_in_region(32+128,32+128,1024-128,512-128)
class Bullet_Collection(Sprite):
    def on_create(self):
        global end_cond
        if end_cond== True:
            self.delete()
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
            p1_bullet.text = "Left Bullet: "+str(round(p1.bullet,1))
            self.delete()
        if self.is_touching_any_sprite_with_tag("p2"):
            p2.bullet += 10
            p2_bullet.text = "Left Bullet: "+str(round(p2.bullet,1))
            self.delete()
class Bullet_Shooting(Sprite):
    def on_create(self):
        self.image = "BULLET.png"
        self.scale = 0.01
        self.time = 0
    def on_update(self,dt):
        self.time += dt
        self.move_forward(10)
        if self.is_touching_any_sprite_with_tag("ldtk_wall"):
            self.delete()
        if self.time >= 10:
            self.delete()
        if "p1b" in self.tags:
            if self.is_touching_any_sprite_with_tag("p2"):
                print('p1 bullet touched p2')
                if p2.holding == True:
                    p2.drop_power()
                else:
                    print(p2.get_SP)
                    p2.get_SP *= 0.5
                    print(p2.get_SP)
                self.delete()
        if "p2b" in self.tags:
            if self.is_touching_any_sprite_with_tag("p1"):
                if p1.holding == True:
                    p1.drop_power()
                else:
                    print(p1.get_SP)
                    p1.get_SP *= 0.5
                    print(p1.get_SP)
                self.delete()

def Spawn_Bullet():
    window.create_sprite(Bullet_Collection)
Scheduler.update(Spawn_Bullet,5)
if end_cond== True:
    Scheduler.cancel_update(Spawn_Bullet)

#joysticks set up
joysticks = pyglet.input.get_joysticks()


power = window.create_sprite(Power)
#p1 set up
p1 = window.create_sprite(Player,x =64,y = 160)
if len(joysticks) >= 1:
    joysticks[0].open()
    joysticks[0].push_handlers(p1)
p1.image = "P1.png"
p1.add_tag("p1")
p1.set_key(
    up=KeyCode.W,
    down=KeyCode.S,
    left = KeyCode.A,
    right = KeyCode.D,
    shoot = KeyCode.SPACE,
    pick_up = KeyCode.Z,
    super_power= KeyCode.X)
#p2 set up
p2 = window.create_sprite(Player,x =960,y = 380)
if len(joysticks) >= 2:
    joysticks[1].open()
    joysticks[1].push_handlers(p2)
p2.image = "P2.png"
p2.rotation = 180
p2.add_tag("p2")
p2.set_key(
    up = KeyCode.UP,
    down = KeyCode.DOWN,
    left = KeyCode.LEFT,
    right = KeyCode.RIGHT,
    shoot = KeyCode.NUM_0,
    pick_up = KeyCode.P,
    super_power = KeyCode.L)
#label set up
p1h = window.create_label(text = "Keeping Time: "+str(round(p1.keep_hold,1)),x = 0+32,y = 512-32)
p1_bullet = window.create_label(text = "Left Bullet: "+str(round(p1.bullet,1)),x = 0+32,y = 512-64)
p1h.font_size = 15
p1_bullet.font_size = 15
p2h = window.create_label(text = "Keeping Time: "+str(round(p1.keep_hold,1)),x = 1024-200,y = 0+64)
p2_bullet = window.create_label(text = "Left Bullet: "+str(round(p2.bullet,1)),x = 1024-200,y = 0+96)
p2h.font_size = 15
p2_bullet.font_size = 15
#bars
bar1 = window.create_sprite(x = 0+100,y = 512-100)
bar1.image = "for_p1.png"
bar1.layer = 0
bar2 = window.create_sprite(x = 1024-150,y = 0+120)
bar2.image = "for_p2.png"
color_bar1 = window.create_sprite(x = 0+100,y = 512-100)
color_bar1.layer = 1
color_bar1.image = "bar_p1.png"
color_bar2 = window.create_sprite(x = 1024-150,y = 0+120)
color_bar2.layer = 1
color_bar2.image = "bar_p2.png"
window.run()