from pygame import *
from random import randint
window = display.set_mode((700, 500))
display.set_caption('Шутер')

background = transform.scale(image.load('galaxy.jpg'), (700, 500))
class GameSprite (sprite.Sprite):
    def __init__(self,player_image,player_x,player_y, player_speed, player_width, player_height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y ))
    
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT]and self.rect.x > 0:
            self.rect.x -= 10 
        if keys_pressed[K_RIGHT]and self.rect.x < 595:
            self.rect.x += 10 





    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15, 20, 15)
        bullets.add(bullet)
lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 635:
            global lost 
            self.rect.x = randint(80, 700 - 80)
            self.rect.y = -65
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0: 
            self.kill()

class asteroids(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 635:

            self.rect.x = randint(80, 700 - 80)
            self.rect.y = - 65


game = True
finish = False
clock = time.Clock()
FPS = 60
mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play() 
player = Player('rocket.png', 100, 400, 10, 65, 100)
bullets = sprite.Group()
monsters = sprite.Group()
meteor_shower = sprite.Group()
font.init()
font1 = font.SysFont('Arial',36)
lose = font1.render(
    'YOU LOSE', True, (255, 0, 0)
)
win = font1.render(
    'YOU WIN', True, (0, 255, 0)
)
for i in range(3):
    meteor = asteroids('asteroid.png', randint(0, 635), -65, randint(1, 3), 100, 65)
    meteor_shower.add(meteor)
for i in range(5): 
    enemy = Enemy('ufo.png', randint(0, 635), -65, randint(1, 3), 100, 65)
    monsters.add(enemy)
monster_counter = 0
while game:  
    if finish != True:
        window.blit(background,(0, 0))
        player.update()
        player.reset()
        monsters.draw(window)
        monsters.update()
        meteor_shower.draw(window)
        meteor_shower.update()
        bullets.draw(window)
        bullets.update() 
        text_win = font1.render('Монстров убито:' +str(monster_counter), 1, (255,255,255))
        text_lose = font1.render('Пропущено:' +str(lost), 1, (255, 255, 255))
        window.blit(text_win, (0, 30))
        window.blit(text_lose, (0, 0))
        if sprite.spritecollide(player, monsters, False) or lost >3:
            finish = True
            window.blit(lose, (300, 350))
        sprites_list = sprite.groupcollide(
            monsters, bullets, True, True
        )
        if sprite.spritecollide(player, meteor_shower, False):
            finish = True
            window.blit(lose, (300, 350))
        for monster in sprites_list:
            monster_counter += 1
            enemy = Enemy('ufo.png', randint(0, 635), -65, 5, 100, 65)
            monsters.add(enemy)
        if monster_counter >= 10:
            finish = True
            window.blit(win, (300, 250)) 
    for e in event.get():
        if e.type == QUIT: 
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                    
    display.update()
    clock.tick(FPS)
