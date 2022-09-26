import random
from pycat.core import Window,Sprite,Scheduler,Point,RotationMode
window = Window(draw_sprite_rects = True)
clicked_cards = []
images = ["1.png","2.png","3.png","4.png"]*6
total_tries = 0
get_right = 0
success_percentage = 0
grade = "null"
random.shuffle(images)
class Startbutton(Sprite):
    def on_create(self):
        self.color = (200,200,255)
        self.scale = 10
        self.x = 1000
        self.y = 200
    def on_left_click(self):
        for card in window.get_sprites_with_tag("card"):
            card.is_shuffling = True
class Card(Sprite):
    def on_create(self):
        self.opacity = 0
        self.is_animating = False
        self.is_shuffling = False
        self.target_point = Point(100,100)
        self.add_tag("card")
        self.rotation_mode = RotationMode.NO_ROTATION

    def on_left_click(self):
        if len(clicked_cards) < 2 and self not in clicked_cards:
            clicked_cards.append(self)
            print(clicked_cards)
            self.opacity = 255
    
        
    def on_update(self, dt):
        if self.is_shuffling:
            self.point_toward(self.target_point)
            self.move_forward(5)
            if self.distance_to(self.target_point)<10:
                self.is_shuffling = False
        if self.is_animating == True:
            self.rotation+=10
            self.scale -= 0.1
            self.opacity -= 10
            self.x += 10
            if self.opacity <= 10:
                self.delete()
class Check_Button(Sprite):
    def on_create(self):
        self.color = (0,0,255)
        self.scale = 50
        self.x = 1000
        self.y = 300
        self.game_time = 0
        self.is_finish = False
    def on_left_click(self):
        if len(clicked_cards) == 2:
            if clicked_cards[0].image == clicked_cards[1].image:
                clicked_cards[0].is_animating = True
                clicked_cards[1].is_animating = True
                global get_right
                get_right += 1
                global total_tries
                total_tries += 1
                print(get_right)
                print(total_tries)
            else:
                clicked_cards[0].opacity = 0
                clicked_cards[1].opacity = 0
                total_tries += 1
                print(total_tries)
            clicked_cards.clear()

    def on_update(self, dt):
        global get_right
        if get_right >= 12:
            self.is_finish = True
            if self.is_finish:
                global total_tries
                global success_percentage
                success_percentage = get_right/total_tries * 100
                global grade
                if success_percentage <= 1:
                    grade = "F"
                elif success_percentage <= 10:
                    grade = "E"
                elif success_percentage <= 20:
                    grade = "D"
                elif success_percentage <= 35:
                    grade = "C"
                elif success_percentage <= 50:
                    grade = "B"
                elif success_percentage <= 60:
                    grade = "B+"
                elif success_percentage <= 75:
                    grade = "A"
                elif success_percentage <= 85:
                    grade = "A+"
                elif success_percentage <= 90:
                    grade="S"
                elif success_percentage == 100:
                    grade = "G"
                global grade_shower
                grade_shower.text = "grade: "+grade    

for x in [100,200,300,400,500,600]:
    for y in [100,200,300,400]:
        card = window.create_sprite(Card,x = 650,y = 500,scale = 1,image = images.pop())
        card.target_point = Point(x,y)
window.create_sprite(Startbutton)        
window.create_sprite(Check_Button)
grade_shower = window.create_label(text = "grade: "+grade ,x = 640 ,y = 500)
window.run()