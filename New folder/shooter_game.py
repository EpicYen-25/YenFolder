from pygame import *
#for enemy
from time import time as timer
from random import randint

#Variables
score = 0
lost = 0
goal = 31
max_lost = 31
lives = 3

#Parent Class
class GameSprite(sprite.Sprite):
    def __init__ (self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#Child Class
class Player (GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -20)
        bullets.add(bullet)

#Child class for Enemy
class Enemy (GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(90, win_width-90)
            self.rect.y = 0
            lost = lost + 1
        
#Bullet child class
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        #disappears if reaches the edge of window
        if self.rect.y < 0:
                self.kill()   #kill => remove from sprite



#Fonts and Captions
font.init()
displayText = font.SysFont("Arial", 40)
endText = font.SysFont("Arial", 85)
win = endText.render("YOU WIN!", True, (215, 153, 242))
lose = endText.render("YOU LOSE!", True, (215, 153, 242))

#Images
img_bk = "space.jpg"
img_hero = "ship.png"
img_enemy = "rocky.png"
img_bullet = "bullet.png"
space = "space.ogg"


#Create music/sound
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

fire_sound = mixer.Sound("fire.ogg") 

#Window
win_width = 900
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("The Shooting Game")

bk = transform.scale(image.load(img_bk), (win_width, win_height))

#Create Sprites
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

UFOs = sprite.Group()
for i in range(1, 8):
    ufo = Enemy(img_enemy, randint(75, win_width -75), -40, 80, 50, randint(1, 5))
    UFOs.add(ufo)

bullets = sprite.Group()

#Game Loop
game = True
finish = False
rel_time = False
num_fire = 0

FPS = 60
clock = time.Clock()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                    if num_fire < 100 and rel_time == False:
                        num_fire = num_fire + 1
                        fire_sound.play()
                        ship.fire()
                    if num_fire >= 100 and rel_time == False:
                        last_time = timer()
                        rel_time = True


    if not finish:

        window.blit(bk, (0,0))

        bullets.update()
        bullets.draw(window)

        #Reload
        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = endText.render("Wait, reloading .....", 1, (150, 0, 0))
                window.blit(reload, (180, 200))
            else:
                num_fire = 0
                rel_time = False

        ship.update()
        ship.reset()

        #Enemies
        UFOs.update()
        UFOs.draw(window)


        #Text
        SCORE = displayText.render("Score: " + str(score), 1, (210,196,240))
        window.blit(SCORE, (10, 20))

        MISSED = displayText.render("Missed: "+ str(lost), 1, (210,196,240))
        window.blit(MISSED, (10, 50))

        LIVES = displayText.render("Lives: "+ str(lives), 1, (210,196,240)) 
        window.blit(LIVES, (600, 0))

        #check for collision
        collides = sprite.groupcollide(UFOs, bullets, True, True)
        for c in collides:
            score = score + 1
            ufo = Enemy(img_enemy, randint(80, win_width -80), -40, 80, 50, randint(1, 5))
            UFOs.add(ufo)

        if sprite.spritecollide(ship, UFOs, False) and lives != 0:
            lives = lives - 1

        if lives == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (180, 200))

        if score >= goal:
            finish = True
            window.blit(win, (290, 200))


        display.update()
        clock.tick(FPS)

    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        lives = 3
        for b in bullets:
            b.kill()
        for m in UFOs:
            m.kill()

        time.delay(3000)
        for i in range(1, 6):
            ufo = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            UFOs.add(ufo)