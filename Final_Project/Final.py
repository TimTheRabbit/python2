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
    def on_update(self, dt):
        if self.y >= window.height +self.y*0.5:
            self.y = 0-self.y*0.5
        elif self.y <= 0-self.y*0.5:
            self.y = window.height +self.y*0.5

class Moveable_Wall(WrapSprite):
    pass

class Player1(WrapSprite):
    def on_create(self):
        self.image = "P1"
        self.keep_hold = 0
        self.bullet = 0
        self.get_SP = 0
        self.SP = False
        self.rotation_mode = RotationMode.MIRROR
        self.speed = 5
    def on_update(self, dt):
        self.get_SP += 0.000000001
        if window.is_key_pressed(KeyCode.W):
            self.move_forward(self.speed)
        elif window.is_key_pressed(KeyCode.S):
            self.move_forward(self.speed)
        if window.is_key_pressed(KeyCode.A):
            self.rotation -= 15
        if window.is_key_pressed(KeyCode.D):
            self.rotation += 15

class Player2(WrapSprite):
    def on_create(self):
        self.image = "P2"
        self.keep_hold = 0
        self.bullet = 0
        self.get_SP = 0
        self.SP = False
        self.rotation_mode = RotationMode.MIRROR
class Target(Sprite):
    pass
class Bullet(Sprite):
    pass

window.create_sprite(Player1,x =64,y = 160)
window.run()