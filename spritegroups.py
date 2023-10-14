import pygame

# Player and enemy ships
player_ship_group = pygame.sprite.GroupSingle()
enemy_group = pygame.sprite.Group()

# Bullet groups - members are added os needed
player_bullet_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()

# Explosions
explosion_group = pygame.sprite.Group()

# Powerups and their effects
powerup_group = pygame.sprite.Group()
heart_and_sparks_group = pygame.sprite.Group()
