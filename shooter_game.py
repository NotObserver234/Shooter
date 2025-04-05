from pygame import *
from random import randint
from time import time as timer

# Инициализация окна
window = display.set_mode((700, 500))
display.set_caption('Шутер') 
bg = transform.scale(image.load("galaxy.jpg"), (700, 500)) 

# Звуки
mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.3)
mixer.music.play(-1)
fire_sound = mixer.Sound('fire.ogg')

# Класс для игровых спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, w, h, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < 395:
            self.rect.y += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 595:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 620)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

def reset_game():
    global scored, lost, finish, bullets, monsters, player, lives
    scored = 0
    lost = 0
    finish = False
    lives = 3
    bullets.empty()
    monsters.empty()
    for i in range(5):
        monster = Enemy('ufo.png', randint(0, 620), -40, 80, 50, randint(1, 3))
        monsters.add(monster)
    player = Player("rocket.png", 50, 300, 65, 65, 5)

# Переменные
lives = 3
scored = 0
lost = 0
bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()
player = Player("rocket.png", 50, 300, 65, 65, 5)

for i in range(5):
    monster = Enemy('ufo.png', randint(0, 620), -40, 80, 50, randint(1, 3))
    monsters.add(monster)

for i in range(5):
    asteroid = Enemy('asteroid.png', randint(0, 620), -40, 80, 50, randint(1, 3))
    asteroids.add(asteroid)

num_fire = 0
rel_time = False


game = True
finish = False
font.init()
font = font.SysFont('Arial', 40)
win = font.render('YOU WIN', True, (0, 255, 0))
fail = font.render('YOU LOSE', True, (255, 0, 0))

# Игровой цикл
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE and not finish:
                if num_fire <5 and rel_time ==False:
                    fire_sound.play()
                    player.fire()
                    num_fire += 1

                if num_fire >= 5 and rel_time ==False:
                    last_time = timer()
                    rel_time = True
            if e.key == K_r and finish:
                reset_game()

    if not finish:
        window.blit(bg, (0, 0))
        if rel_time:
            now_time = timer()
            if now_time - last_time <3:
                reload = font.render("Reloading...",True,(150,0,0))
                window.blit(reload,(250,400))
            else:
                num_fire = 0
                rel_time = False
        player.reset()
        player.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()

        score = font.render("Очки:" + str(scored), 1, (255, 255, 255))
        text_lose = font.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        lives_text = font.render("Жизни:" + str(lives), 1, (255, 255, 255))
        window.blit(text_lose, (30, 30))
        window.blit(lives_text, (30, 110))
        window.blit(score, (30, 70))

        if sprite.groupcollide(bullets, monsters, True, True):
            scored += 1
            monster = Enemy('ufo.png', randint(0, 620), -40, 80, 50, randint(1, 3))
            monsters.add(monster)

        if scored == 10:
            finish = True
            window.blit(win, (350, 250))

        if sprite.spritecollide(player, monsters, True) and lives != 0:
            lives -= 1

        if lives == 0 or lost > 5:
            finish = True
            window.blit(fail, (350, 250))

    display.update()
    time.delay(10)





