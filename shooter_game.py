#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer

display.set_caption('игра Шутер')
window = display.set_mode((700, 500))
back = transform.scale(image.load('galaxy.jpg'), (700, 500))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)
mixer.music.set_volume(0.1)



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 700:
            self.rect.x = randint(80, 420)
            self.rect.y = 0
            lost += 1
            
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill

num_fire = 0
rel_time = False
bullets = sprite.Group()
lives = 3
score = 0
lost = 0
font.init()
font2 = font.SysFont('Arial', 36)

win = font2.render('YOU WIN', True, (255, 255, 255)) 
lose = font2.render('YOU LOSE', True, (180, 0, 0)) 
fire_sound = mixer.Sound('fire.ogg')

player = Player('rocket.png', 25, 425, 60, 60, 8)
monsters = sprite.Group()
asteroids = sprite.Group()
sprites_list = [monsters, bullets]

for i in range(3):
    asteroid = Enemy('asteroid.png', randint(80, 420), -40, 80, 60, randint(2, 4))
    asteroids.add(asteroid)

for i in range(5):
    monster = Enemy('ufo.png', randint(80, 420), -40, 80, 60, randint(2, 4))
    monsters.add(monster)

bullet = Bullet
finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    fire_sound.play()
                    player.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    last_time = timer()
        
            

            


    if not finish:
        window.blit(back, (0, 0))
        player.update()
        player.reset()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Перезарядка', True, (150,0,0))
                window.blit(reload, (250, 400))
            else:
                num_fire = 0
                rel_time = False

        text_lives = font2.render('Жизни: ' + str(lives), True, (255, 255, 255))
        window.blit(text_lives, (550, 10))
        text_lose = font2.render('Пропущено: ' + str(lost), True, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        text_score = font2.render('Счёт: ' + str(score), True, (255, 255, 255))
        window.blit(text_score, (10, 10))

        if sprite.groupcollide(monsters, bullets, True, True):
            score += 1           
            monster = Enemy('ufo.png', randint(80, 420), -40, 80, 60, randint(2, 4))
            monsters.add(monster)
                     
        if  score > 20:
            window.blit(win, (250, 250))
            finish = True
        if sprite.spritecollide(player, monsters, False): 
            window.blit(lose, (250, 250))
            finish = True   
        if sprite.spritecollide(player, asteroids, True):
            lives -= 1    
        if lives < 1:
            window.blit(lose, (250, 250))
            finish = True    

    display.update()
    time.delay(30)