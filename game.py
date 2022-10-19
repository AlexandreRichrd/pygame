import pygame, pytmx, pyscroll

from player import Player

class Game:
  def __init__(self):

    # Creer la fenetre du jeu
    self.screen = pygame.display.set_mode((800, 600)) # self = objet courant
    pygame.display.set_caption("Jeu python")

    #charger la carte (tmx)
    tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
    self.map_name = 'carte'
    map_data = pyscroll.data.TiledMapData(tmx_data)
    map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
    map_layer.zoom = 2

    # Generer un joueur
    player_position = tmx_data.get_object_by_name("player")
    self.player = Player(player_position.x, player_position.y)

    # definir une liste qui va stocker les rectangles de collision
    self.walls = []

    for obj in tmx_data.objects:
      if obj.name == "collision":
        self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))


    # Dessiner le groupe de calques
    self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
    self.group.add(self.player)

    # Definir event entrer maison
    enter_house = tmx_data.get_object_by_name('enter_house')
    self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)


  def handle_input(self):
    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_UP]:
      self.player.move_up()
      self.player.change_animation('up')
    elif pressed[pygame.K_DOWN]:
      self.player.move_down()
      self.player.change_animation('down')
    elif pressed[pygame.K_LEFT]:
      self.player.move_left()
      self.player.change_animation('left')
    elif pressed[pygame.K_RIGHT]:
      self.player.move_right()
      self.player.change_animation('right')

  def switch_to_house(self):
    # Charger la carte (tmx)
    tmx_data = pytmx.util_pygame.load_pygame('house.tmx')

    map_data = pyscroll.data.TiledMapData(tmx_data)
    map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
    map_layer.zoom = 2

    # definir une liste qui va stocker les rectangles de collision
    self.walls = []

    for obj in tmx_data.objects:
      if obj.name == "collision":
        self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))


    # Dessiner le groupe de calques
    self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
    self.group.add(self.player)

    # Definir event sortie maison
    self.map_name = 'house'
    enter_house = tmx_data.get_object_by_name('exit_house')
    self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

    # recuperer le point de spawn
    spawn_house_point = tmx_data.get_object_by_name('spawn_house')
    self.player.position[0] = spawn_house_point.x
    self.player.position[1] = spawn_house_point.y - 20

  def switch_to_world(self):
    #charger la carte (tmx)
    tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
    self.map_name = 'carte'
    map_data = pyscroll.data.TiledMapData(tmx_data)
    map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
    map_layer.zoom = 2

    # definir une liste qui va stocker les rectangles de collision
    self.walls = []

    for obj in tmx_data.objects:
      if obj.name == "collision":
        self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))


    # Dessiner le groupe de calques
    self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
    self.group.add(self.player)

    # Definir event entree maison
    enter_house = tmx_data.get_object_by_name('enter_house')
    self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

    # recuperer le point de spawn
    spawn_house_point = tmx_data.get_object_by_name('enter_house_exit')
    self.player.position[0] = spawn_house_point.x
    self.player.position[1] = spawn_house_point.y


  def update(self):
    self.group.update()

    # Verification entree dans la maison
    if self.player.feet.colliderect(self.enter_house_rect) and self.map_name == 'carte':
      self.switch_to_house()
    elif self.player.feet.colliderect(self.enter_house_rect) and self.map_name == 'house':
      self.switch_to_world()


    # Verification de la collision
    for sprite in self.group.sprites():
      if sprite.feet.collidelist(self.walls) > -1 :
        sprite.move_back()



  def run(self):

    clock = pygame.time.Clock()

    # boucle du jeu
    running = True

    while running:

      self.player.save_location()
      self.handle_input()
      self.update()
      self.group.center(self.player.rect.center)
      self.group.draw(self.screen) # Dessin des layer
      pygame.display.flip() # actualisation du display

      for event in pygame.event.get():

        # Si la fenetre est fermee
        if event.type == pygame.QUIT:
          running = False
      clock.tick(60)
    pygame.quit()