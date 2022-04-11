import pygame, sys, random, time


class Crosshair(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()

        self.image = assets[picture_path]
        self.rect = self.image.get_rect()
        self.rect.width = 10
        self.rect.height = 10
        self.shotSound = pygame.mixer.Sound("PEW.mp3")
        self.count = 0

    def shoot(self):
        global text
        if not game_over:
            self.shotSound.play()

            if pygame.sprite.spritecollide(crosshair, TargetGroup, True):
                self.count += 1
                text = font.render(str(len(TargetGroup.sprites())), True, (255, 255, 255))

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class Target(pygame.sprite.Sprite):

    def __init__(self, picture_path, pos_x, pos_y, vel_min, vel_max, direction, probability):
        super().__init__()
        self.image = assets[picture_path]
        self.rect = self.image.get_rect()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_min = vel_min
        self.vel_max = vel_max
        self.vel = random.randint(vel_min, vel_max)
        self.direction = "right"
        self.direction_options = direction
        self.probability = probability
    def random_direction(self):
        if ((self.pos_x > screenWidth + 300) or (self.pos_x < -300) or (self.pos_y > screenHeight + 300) or (
                self.pos_y < -300)):

            # Enemy targets
            if ENEMIES:
                self.enemy_target(random.randint(0,  self.probability))

            # Directions
            self.direction = random.choice(self.direction_options)
            self.vel = random.randint(self.vel_min, self.vel_max)
            if self.direction == "right":
                self.pos_x = -300
                self.pos_y = random.randrange(0, screenHeight)
                self.vel = abs(self.vel)
                self.pos_x += self.vel

            elif self.direction == "left":
                self.pos_x = screenWidth + 300
                self.pos_y = random.randrange(0, screenHeight)
                self.vel = -abs(self.vel)
                self.pos_x += self.vel

            elif self.direction == "down":
                self.pos_y = -300
                self.pos_x = random.randrange(0, screenWidth)
                self.vel = abs(self.vel)
                self.pos_y += self.vel

            elif self.direction == "up":
                self.pos_y = screenHeight + 300
                self.pos_x = random.randrange(0, screenWidth)
                self.vel = -abs(self.vel)
                self.pos_y += self.vel

        if (self.direction == "right") or (self.direction == "left"):
            self.pos_x += self.vel

        elif (self.direction == "down") or (self.direction == "up"):
            self.pos_y += self.vel

    def enemy_target(self, probability):

        pygame.sprite.Sprite.remove(self, TargetEnemyGroup)
        self.image = assets["dante"]
        if probability == 0:
            TargetEnemyGroup.add(self)
            self.image = assets["dante(purple)"]

    def light_up(self):
        if pygame.sprite.collide_rect(crosshair, self) and not game_over:
            self.image = assets["dante(LightBlue)"]
        elif self.image == assets["dante(LightBlue)"]:
            self.image = assets["dante"]

    def update(self):

        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.image.get_width(), self.image.get_height())
        self.random_direction()
        self.light_up()


def createTargetGroup():
    new_target_group = pygame.sprite.Group()
    for target in range(15):
        new_target = Target("dante", screenWidth + 100, random.randrange(-125, screenHeight), 3, 8, ["right"], 10)
        new_target_group.add(new_target)
    return new_target_group


def wave1():
    for target in range(random.randint(5, 10)):
        new_target = Target("dante", screenWidth + 100, random.randrange(-125, screenHeight), 4, 10, ["left", "right"], 8)
        TargetGroup.add(new_target)
        all_sprites_list.add(new_target)

def wave2():
    for target in range(random.randint(10, 20)):
        new_target = Target("dante", screenWidth + 100, random.randrange(-125, screenHeight), 5, 11, ["left", "right", "down"], 7)
        TargetGroup.add(new_target)
        all_sprites_list.add(new_target)
def wave3():
    for target in range(random.randint(20, 35)):
        new_target = Target("dante", screenWidth + 100, random.randrange(-125, screenHeight), 6, 12, ["left", "right", "down", "up"], 6)
        TargetGroup.add(new_target)
        all_sprites_list.add(new_target)
def wave4():
    for target in range(random.randint(35, 50)):
        new_target = Target("dante", screenWidth + 100, random.randrange(-125, screenHeight), 7, 13, ["left", "right", "down", "up"], 5)
        TargetGroup.add(new_target)
        all_sprites_list.add(new_target)
def wave5():
    for target in range(random.randint(50, 70)):
        new_target = Target("dante", screenWidth + 100, random.randrange(-125, screenHeight), 8, 14, "right", 4)
        TargetGroup.add(new_target)
        all_sprites_list.add(new_target)

def create_cross_group():
    crosshairGroup = pygame.sprite.GroupSingle()
    crosshairGroup.add(crosshair)
    return crosshairGroup


# game settings
ENEMIES = True
game_over = False

# General Setup
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
assets = {}

# Game Screen
(screenWidth, screenHeight) = (1500, 900)
screen = pygame.display.set_mode((screenWidth, screenHeight))
background_colour = (0, 0, 0)
screen.fill(background_colour)
pygame.display.set_caption('game')
background = pygame.image.load("BG (2).png").convert_alpha()

# Crosshair
assets["fish"] = pygame.image.load("fish.png").convert_alpha()
crosshair = Crosshair("fish")
crosshairGroup = create_cross_group()
pygame.mouse.set_visible(False)

# Target
assets["dante"] = pygame.image.load("dante.png").convert_alpha()
assets["dante(LightBlue)"] = pygame.image.load("dante(LightBlue).png").convert_alpha()
assets["dante(purple)"] = pygame.image.load("dante(purple).png").convert_alpha()
TargetGroup = createTargetGroup()
TargetEnemyGroup = pygame.sprite.Group()

# allSprites
all_sprites_list = pygame.sprite.Group(TargetGroup, crosshairGroup)

# Text

font = pygame.font.Font('freesansbold.ttf', 40)
bigFont = pygame.font.Font('freesansbold.ttf', 150)
text = font.render(str(len(TargetGroup.sprites())), True, (255, 255, 255))
textRect = text.get_rect()
textRect.center = [30, 30]
textLose = bigFont.render("DED", True, (255, 0, 0))
textRectLose = textLose.get_rect()
textRectLose.center = [screenWidth // 2, screenHeight // 2]


def reset():
    global wave1bool, wave2bool, wave3bool, wave4bool, wave5bool
    global game_over, crosshair, crosshairGroup, TargetEnemyGroup, TargetGroup, all_sprites_list
    game_over = False
    crosshair = Crosshair("fish")
    TargetEnemyGroup = pygame.sprite.Group()
    crosshairGroup = create_cross_group()
    TargetGroup = createTargetGroup()
    all_sprites_list = pygame.sprite.Group(TargetGroup, crosshairGroup)
    wave1bool = True
    wave2bool = True
    wave3bool = True
    wave4bool = True
    wave5bool = True


# Main Loop
def menu():
    # Title
    assets["TITLE"] = pygame.image.load("TITLE.png").convert_alpha()
    title_img = assets["TITLE"]
    title_rect = title_img.get_rect()
    title_rect.center = [screenWidth // 2, screenHeight // 4]
    c = screen.blit(title_img, title_rect)
    # Exit game button
    assets["EXIT_BUTTON"] = pygame.image.load("EXIT_BUTTON.png").convert_alpha()
    button_exit_img = assets["EXIT_BUTTON"]
    button_exit_img_rect = button_exit_img.get_rect()
    button_exit_img_rect.bottomright = (screenWidth, screenHeight)
    a = screen.blit(button_exit_img, button_exit_img_rect)

    # Start game button
    assets["START_BUTTON"] = pygame.image.load("START_BUTTON (2).png").convert_alpha()
    assets["START_BUTTON2"] = pygame.image.load("pixil-frame-0 (3).png").convert_alpha()
    assets["START_BUTTON3"] = pygame.image.load("START_BUTTON_MOUSE_POS.png").convert_alpha()

    button_start_img = assets["START_BUTTON"]
    button_start_img_rect = button_start_img.get_rect()
    button_start_img_rect.center = (screenWidth // 2, screenHeight * 3 / 5)
    b = screen.blit(button_start_img, button_start_img_rect)

    menu_running = True
    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                crosshair.shoot()
                if b.collidepoint(pygame.mouse.get_pos()):
                    button_start_img = assets["START_BUTTON2"]

            if event.type == pygame.MOUSEBUTTONUP:
                button_start_img = assets["START_BUTTON"]

                if a.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()

                if b.collidepoint(pygame.mouse.get_pos()):
                    game()
                    pass

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game()
                    pass

        a = screen.blit(button_exit_img, button_exit_img_rect)
        b = screen.blit(button_start_img, button_start_img_rect)
        c = screen.blit(title_img, title_rect)

        # Group Update
        crosshair.update()
        crosshairGroup.draw(screen)

        # Screen Update
        pygame.display.update()
        screen.blit(background, (0, 0))
        # screen.fill((0, 0, 0))


def game():
    global game_over, text
    running = True
    wave1bool = True
    wave2bool = True
    wave3bool = True
    wave4bool = True
    wave5bool = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                crosshair.shoot()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset()
                if event.key == pygame.K_ESCAPE:
                    menu()
                    pass
        if pygame.sprite.groupcollide(crosshairGroup, TargetEnemyGroup, False, False, collided=None):
            print('collide with bad')
            game_over = True
            crosshairGroup.sprite.kill()
        if len(TargetGroup.sprites()) < 3 and wave1bool:
            wave1()
            wave1bool = False
        elif len(TargetGroup.sprites()) < 4 and wave2bool and wave1bool == False:
            wave2()
            wave2bool = False
        elif len(TargetGroup.sprites()) < 5 and wave3bool and wave1bool == False and wave2bool == False:
            wave3()
            wave3bool = False
        elif len(TargetGroup.sprites()) < 6 and wave4bool and wave1bool == False and wave2bool == False and wave3bool == False:
            wave4()
            wave4bool = False
        elif len(TargetGroup.sprites()) < 7 and wave5bool and wave1bool == False and wave2bool == False and wave3bool == False and wave4bool == False:
            wave5()
            wave5bool = False


        # Group Update
        all_sprites_list.draw(screen)
        TargetGroup.update()
        crosshair.update()

        if game_over:
            screen.blit(textLose, textRectLose)
        screen.blit(text, textRect)

        # Screen Update
        pygame.display.update()
        #screen.blit(background, (0, 0))
        screen.fill((0, 0, 0))
        # Time
        clock.tick(60)
        print(clock.get_fps())


menu()
