import pygame
import random
import sys

pygame.init()

# Создание окна
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Space crusader ")

# Загрузка заднего фона и иконки
background = pygame.image.load("images/back.jpg")
icon = pygame.image.load("images/icom.png")
pygame.display.set_icon(icon)


# Создание персонажа
class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("images/ct.png"), (107, 64))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 7

    def update(self):
        # Обработка движения персонажа
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen.get_width():
            self.rect.x += self.speed

    def collide_with_asteroid(self, asteroids):
        """Проверка коллизии со спрайтами астероидов"""
        if pygame.sprite.spritecollide(self, asteroids, False):
            font = pygame.font.Font("font/PublicPixel-z84yD.ttf", 60)
            game_over_text = font.render("GAME OVER!", True, (255, 0, 0))
            restart_text = font.render("Restart?", True, (255, 255, 255))
            game_over_rect = game_over_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2-30))
            restart_rect = restart_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 60))
            screen.blit(game_over_text, game_over_rect)
            screen.blit(restart_text, restart_rect)
            pygame.display.update()
            # Ожидание нажатия клавиши для перезапуска игры
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            waiting = False
                            restart_game()
                            break


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.width = 10
        self.rect.height = 30
        self.rect.x = random.randint(1, 750)
        self.rect.y = random.randint(-500, -50)
        self.speed = random.randint(4, 8)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.kill()


def restart_game():
    """Функция перезагрузки игры"""
    all_sprites.empty()
    asteroids_group.empty()
    for _ in range(5):
        asteroid = Asteroid(asteroid_image)
        asteroids_group.add(asteroid)
        all_sprites.add(asteroid)
    character.rect.x = 400
    character.rect.y = 425
    all_sprites.add(character)


# Отображение заднего фона
screen.blit(background, (0, 0))

# Создание спрайта персонажа
all_sprites = pygame.sprite.Group()
character = Character(400, 425)
all_sprites.add(character)

# Создание астероидов
asteroids_group = pygame.sprite.Group()
asteroid_image = pygame.image.load("images/asteroid.png")
for _ in range(5):
    asteroid = Asteroid(asteroid_image)
    asteroids_group.add(asteroid)
    all_sprites.add(asteroid)

# Основной цикл игры
paused = False
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Обработка событий клавиатуры
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = True
            elif event.key == pygame.K_RETURN:
                paused = False

    # При паузе - отображение надписи "PAUSE"
    if paused:
        font = pygame.font.Font("font/PublicPixel-z84yD.ttf", 60)
        pause_text = font.render("PAUSE", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(pause_text, pause_rect)
        pygame.display.update()
        continue  # Пропустить обновление игровых объектов

    # Обновление и отрисовка спрайтов
    all_sprites.update()
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    character.collide_with_asteroid(asteroids_group)  # Проверка коллизии
    pygame.display.update()

    # Создание новых астероидов со случайной частотой
    if random.randint(2, 40) < 3:
        asteroid = Asteroid(asteroid_image)
        asteroids_group.add(asteroid)
        all_sprites.add(asteroid)

    # Ограничение частоты кадров
    clock.tick(60)

# Завершение работы Pygame
pygame.quit()