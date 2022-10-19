import pygame

class Player(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super().__init__()
    # On recupere l'image
    self.sprite_sheet = pygame.image.load('player.png')

    # On recupere la portion du sprite
    self.image = self.get_image(0, 0)

    # On retire le BG du calque
    self.image.set_colorkey([0, 0, 0])

    # On donne la position du sprite
    self.rect = self.image.get_rect()

    # On definit la position sur le background
    self.position = [x, y]

    # On definit un dictionnaire conenant les images du joueur
    self.images = {
      'down': self.get_image(0, 0),
      'up': self.get_image(0, 96),
      'left': self.get_image(0, 32),
      'right': self.get_image(0, 64)
    }

    # On definit les pieds du joueur
    self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)

    # Variable de sauvegarde de l'ancienne position
    self.old_position = self.position.copy()

    # On definit une variable speed
    self.speed = 3


  # Fonciton de sauvegarde de position
  def save_location(self): self.old_position = self.position.copy()

  # Deplacements
  def move_right(self): self.position[0] += self.speed
  def move_left(self): self.position[0] -= self.speed
  def move_up(self): self.position[1] -= self.speed
  def move_down(self): self.position[1] += self.speed

  # Animation des deplacements
  def change_animation(self, name):
    self.image = self.images[name]
    self.image.set_colorkey((0, 0, 0))

  # Action lorsque le joueur entre en collision
  def move_back(self):
    self.position = self.old_position
    self.rect.topleft = self.position
    self.feet.midbottom = self.rect.midbottom



  def update(self):
    self.rect.topleft = self.position
    self.feet.midbottom = self.rect.midbottom

  def get_image(self, x, y):
    image = pygame.Surface([32, 32])
    image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32)) # Absorber et extraire un morceau du sprite
    return image