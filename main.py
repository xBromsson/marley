import pygame
import random
from sys import exit

class Player():
    def __init__(self):
        self.health = 40
        self.opponent = None
        self.soldiers = 2
        self.mages = 2
        self.builders = 2
        self.swords = 6
        self.crystals = 6
        self.bricks = 6
        self.stack = []
        self.hand = []

class RedCastle(Player):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("graphics/castle_red.png").convert_alpha()
        self.active_surf = pygame.image.load("graphics/castle_red_turn.png").convert_alpha()
        self.rect = self.surf.get_rect(topleft=(50, 250))


    def blit_castle(self):
        if g.active_player == redplayer:
            g.screen.blit(self.active_surf, self.rect)
        else:
            g.screen.blit(self.surf, self.rect)

    def blit_cards(self):
        for i, card in enumerate(self.hand):
            card.move_to(((i + .5) * (g.width / len(self.hand))), 525)
            card.blit()

    def refresh_hand(self):
        while len(self.hand) < 5:
            self.hand.append(g.deck.pop(0))

    def play_card(self):
        if g.discard[0].type == "mage":
            self.crystals -= g.discard[0].cost
        if g.discard[0].type == "soldier":
            self.swords -= g.discard[0].cost
        if g.discard[0].type == "builder":
            self.bricks -= g.discard[0].cost
        pass

    def upkeep(self):
        self.swords += self.soldiers
        self.crystals += self.mages
        self.bricks += self.builders
        if self.stack:
            for x in self.stack:
                x.stackability()

class BlueCastle(Player):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("graphics/castle_blue.png").convert_alpha()
        self.active_surf = pygame.image.load("graphics/castle_blue_turn.png").convert_alpha()
        self.rect = self.surf.get_rect(topright=(850,250))

    def blit_castle(self):
        if g.active_player == blueplayer:
            g.screen.blit(self.active_surf, self.rect)
        else:
            g.screen.blit(self.surf, self.rect)

    def blit_cards(self):
        for i, card in enumerate(self.hand):
            card.move_to(100 + (i * (g.width / len(self.hand))), 525)
            card.blit()

    def refresh_hand(self):
        while len(self.hand) < 5:
            self.hand.append(g.deck.pop(0))

    def play_card(self):
        if g.discard[0].type == "mage":
            self.crystals -= g.discard[0].cost
        if g.discard[0].type == "soldier":
            self.swords -= g.discard[0].cost
        if g.discard[0].type == "builder":
            self.bricks -= g.discard[0].cost
        pass

    def upkeep(self):
        self.swords += self.soldiers
        self.crystals += self.mages
        self.bricks += self.builders
        if self.stack:
            for x in self.stack:
                x.stackability()

class Timer():
    def __init__(self, ms):
        self.start_time = pygame.time.get_ticks()
        self.wait = False
        self.ms = ms

    def log_time(self):
        self.start_time = pygame.time.get_ticks()
        print(self.start_time)
        self.wait = True

    def check(self):
        self.elapsed = pygame.time.get_ticks() - self.start_time
        if self.elapsed >= self.ms:
            self.wait = False

class Card():
    def __init__(self):
        self.playable = False
        pass

    def move_to(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

    def blit(self):
        # if not self.rect.collidepoint(mouse_pos):
        g.screen.blit(self.surf, self.rect)
        if self.cost > g.active_player.swords and self.type == "soldier":
            self.surf.set_alpha(100)
            self.playable = False
        elif self.cost > g.active_player.crystals and self.type == "mage":
            self.surf.set_alpha(100)
            self.playable = False
        elif self.cost > g.active_player.bricks and self.type == "builder":
            self.surf.set_alpha(100)
            self.playable = False
        else:
            self.playable = True
            self.surf.set_alpha(255)

        # if self.rect.collidepoint(mouse_pos):
        #     self.rect.centery = 300
        #     screen.blit(pygame.transform.scale2x(self.surf),self.rect)

class Mage(Card):
    def __init__(self):
        super().__init__()
        self.type = "mage"

class Soldier(Card):
    def __init__(self):
        super().__init__()
        self.type = "soldier"

class Builder(Card):
    def __init__(self):
        super().__init__()
        self.type = "builder"

class Catapult(Soldier):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(f'graphics/catapult.png').convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 12

    def ability(self):
        g.active_player.opponent.health -= 15

class Warrior(Soldier):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(f'graphics/warrior.png').convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 4


    def ability(self):
        g.active_player.opponent.health -= 7

class King(Soldier):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(f'graphics/king.png').convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 8


    def ability(self):
        g.active_player.opponent.health -= 10

class Archer(Soldier):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(f'graphics/archer.png').convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 5


    def ability(self):
        g.active_player.opponent.swords -= random.randrange(5)
        g.active_player.opponent.crystals -= random.randrange(5)
        g.active_player.opponent.bricks -= random.randrange(5)

class Fire(Soldier):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(f'graphics/fire.png').convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 5
        self.fire = 3

    def ability(self):
        g.active_player.opponent.stack.append(g.discard[0])


    def stackability(self):
        if self.fire > 0:
            g.active_player.health -= 2
            self.fire -= 1

class SpellBook(Mage):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(f'graphics/spellbook.png').convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 12
        #self.draw = 3

    def ability(self):
        g.active_player.hand.append(random.choice(g.deck))
        g.active_player.hand.append(random.choice(g.deck))

    # def stackability(self):
    #     if self.draw > 0:
    #         g.active_player.hand.append(g.deck.pop(0))
    #         self.draw -= 1

class Confusion(Mage):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(f'graphics/confusion.png').convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 15

    def ability(self):
        g.active_player.opponent.hand.remove(random.choice(g.active_player.opponent.hand))
        g.active_player.opponent.hand.remove(random.choice(g.active_player.opponent.hand))

class Dragon(Mage):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(f'graphics/dragon.png').convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 25


    def ability(self):
        g.active_player.opponent.health -= 35

class Wizard(Mage):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(f'graphics/wizard.png').convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 8


    def ability(self):
        g.active_player.mages += 1

class Scroll(Mage):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(f'graphics/scroll.png').convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 8


    def ability(self):
        g.active_player.hand.insert(0, random.choice(g.active_player.opponent.hand))

class Gate(Builder):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(f'graphics/gate.png').convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 7


    def ability(self):
        g.active_player.health += 10

class BlackSmith(Builder):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(f'graphics/blacksmith.png').convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 8


    def ability(self):
        g.active_player.soldiers += 1

class Castle(Builder):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(f'graphics/castle.png').convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 12


    def ability(self):
        g.active_player.health += 15

class Cart(Builder):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(f'graphics/cart.png').convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 12


    def ability(self):
        g.active_player.swords += 10
        g.active_player.crystals += 10
        g.active_player.bricks += 10

class Kingdom(Builder):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(f'graphics/kingdom.png').convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 17


    def ability(self):
        g.active_player.health += 20







def blit_things():
    redplayer.blit_castle()
    blueplayer.blit_castle()
    g.active_player.blit_cards()

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Seige')
        self.run = True
        self.state = "upkeep"
        self.start = False
        self.width = 900
        self.height = 600
        self.discard = []
        self.deck = []
        self.clouds_list = []
        self.active_player = None
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.Font(None, 50)
        self.seige_title = self.title_font.render("Seige", True, (64, 64, 64))
        self.seige_title_rect = self.seige_title.get_rect(center=(450, 150))
        self.paragraph_font = pygame.font.Font(None, 25)
        self.instruction_surf = self.paragraph_font.render("Press Enter To Start", True, (64, 64, 64))
        self.instruction_rect = self.instruction_surf.get_rect(center=(450, 225))
        self.health_font = pygame.font.Font(None, 40)
        self.bg_surf = pygame.image.load('graphics/background.png').convert_alpha()
        self.bg_rect = self.bg_surf.get_rect()
        self.cloud_surf = pygame.image.load('graphics/cloud_1.png').convert_alpha()
        self.cloud_rect = self.cloud_surf.get_rect(center=(925,random.randrange(25,250)))
        self.discard_surf = pygame.image.load('graphics/card_back.png').convert_alpha()
        self.discard_rect = self.discard_surf.get_rect(center= (450, 250))

    def setup(self):

        self.active_player = redplayer

    def handle_inputs(self):
        #global game.state
        for i, card in enumerate(g.active_player.hand):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if card.rect.collidepoint(mouse_pos) and event.button == 1 and card.playable == True:
                    g.discard.insert(0, g.active_player.hand.pop(i))
                    #self.hand.insert(i, deck.pop(0))
                    g.state = "play"
                    timer.log_time()
                    timer2.log_time()
                if card.rect.collidepoint(mouse_pos) and event.button == 3:
                    g.active_player.hand.pop(i)
                    #self.hand.insert(i, deck.pop(0))
                    g.state = "clean"
                    timer.log_time()
                    timer2.log_time()
        return g.state

    def display_home_screen(self):
        self.screen.fill('white')
        self.screen.blit(self.seige_title, self.seige_title_rect)
        self.screen.blit(self.instruction_surf, self.instruction_rect)

    def determine_opponent(self):
        redplayer.opponent = blueplayer
        blueplayer.opponent = redplayer

    def display_game_screen(self):
        self.screen.blit(self.bg_surf, self.bg_rect)
        self.screen.blit(self.cloud_surf, self.cloud_rect)
        self.screen.blit(self.seige_title, self.seige_title_rect)

        self.cloud_rect.x -= 1
        if self.cloud_rect.x < -100:
            self.cloud_rect.x = random.randrange(901,925)
            self.cloud_rect.y = random.randrange(10,250)

    def blit_cloud(self):
        if self.clouds_list:
            for x, each_cloud_rect in enumerate(self.clouds_list):
                each_cloud_rect.x -= 1
                self.screen.blit(self.cloud_surf, each_cloud_rect)

                if each_cloud_rect.x < -100:
                    g.clouds_list.pop(x)


    def display_stats(self):
        # player 1
        self.redplayer_health_surf = self.health_font.render((str(redplayer.health)), True, (64, 64, 64))
        self.redplayer_health_rect = self.redplayer_health_surf.get_rect(center=(50, 200))
        self.screen.blit(self.redplayer_health_surf, self.redplayer_health_rect)

        self.redplayer_sword_surf = self.health_font.render((str(redplayer.swords)), True, (64, 64, 64))
        self.redplayer_sword_rect = self.redplayer_sword_surf.get_rect(center=(25, 225))
        self.screen.blit(self.redplayer_sword_surf, self.redplayer_sword_rect)

        self.redplayer_crystal_surf = self.health_font.render((str(redplayer.crystals)), True, (64, 64, 64))
        self.redplayer_crystal_rect = self.redplayer_crystal_surf.get_rect(center=(25, 250))
        self.screen.blit(self.redplayer_crystal_surf, self.redplayer_crystal_rect)

        self.redplayer_brick_surf = self.health_font.render((str(redplayer.bricks)), True, (64, 64, 64))
        self.redplayer_brick_rect = self.redplayer_brick_surf.get_rect(center=(25, 275))
        self.screen.blit(self.redplayer_brick_surf, self.redplayer_brick_rect)

        self.redplayer_soldier_surf = self.health_font.render((str(redplayer.soldiers)), True, (64, 64, 64))
        self.redplayer_soldier_rect = self.redplayer_soldier_surf.get_rect(center=(75, 225))
        self.screen.blit(self.redplayer_soldier_surf, self.redplayer_soldier_rect)

        self.redplayer_mages_surf = self.health_font.render((str(redplayer.mages)), True, (64, 64, 64))
        self.redplayer_mages_rect = self.redplayer_mages_surf.get_rect(center=(75, 250))
        self.screen.blit(self.redplayer_mages_surf, self.redplayer_mages_rect)

        self.redplayer_builders_surf = self.health_font.render((str(redplayer.builders)), True, (64, 64, 64))
        self.redplayer_builders_rect = self.redplayer_builders_surf.get_rect(center=(75, 275))
        self.screen.blit(self.redplayer_builders_surf, self.redplayer_builders_rect)

        # player 2
        self.blueplayer_health_surf = self.health_font.render((str(blueplayer.health)), True, (64, 64, 64))
        self.blueplayer_health_rect = self.blueplayer_health_surf.get_rect(center=(850, 200))
        self.screen.blit(self.blueplayer_health_surf, self.blueplayer_health_rect)

        self.blueplayer_sword_surf = self.health_font.render((str(blueplayer.swords)), True, (64, 64, 64))
        self.blueplayer_sword_rect = self.blueplayer_sword_surf.get_rect(center=(825, 225))
        self.screen.blit(self.blueplayer_sword_surf, self.blueplayer_sword_rect)

        self.blueplayer_crystal_surf = self.health_font.render((str(blueplayer.crystals)), True, (64, 64, 64))
        self.blueplayer_crystal_rect = self.blueplayer_crystal_surf.get_rect(center=(825, 250))
        self.screen.blit(self.blueplayer_crystal_surf, self.blueplayer_crystal_rect)

        self.blueplayer_brick_surf = self.health_font.render((str(blueplayer.bricks)), True, (64, 64, 64))
        self.blueplayer_brick_rect = self.blueplayer_brick_surf.get_rect(center=(825, 275))
        self.screen.blit(self.blueplayer_brick_surf, self.blueplayer_brick_rect)

        self.blueplayer_soldier_surf = self.health_font.render((str(blueplayer.soldiers)), True, (64, 64, 64))
        self.blueplayer_soldier_rect = self.blueplayer_soldier_surf.get_rect(center=(875, 225))
        self.screen.blit(self.blueplayer_soldier_surf, self.blueplayer_soldier_rect)

        self.blueplayer_mages_surf = self.health_font.render((str(blueplayer.mages)), True, (64, 64, 64))
        self.blueplayer_mages_rect = self.blueplayer_mages_surf.get_rect(center=(875, 250))
        self.screen.blit(self.blueplayer_mages_surf, self.blueplayer_mages_rect)

        self.blueplayer_builders_surf = self.health_font.render((str(blueplayer.builders)), True, (64, 64, 64))
        self.blueplayer_builders_rect = self.blueplayer_builders_surf.get_rect(center=(875, 275))
        self.screen.blit(self.blueplayer_builders_surf, self.blueplayer_builders_rect)

    def build_deck(self):
        self.soldier_cards = [Catapult() for x in range(20)] + [King() for x in range(20)] + [Warrior() for x in range(20)] + [Archer() for x in range(20)] + [Fire() for x in range(20)]
        self.mage_cards = [SpellBook() for x in range(20)] + [Confusion() for x in range(20)] + [Dragon() for x in range(20)] + [Wizard() for x in range(20)] + [Scroll() for x in range(20)]
        self.builder_cards = [Gate() for x in range(20)] + [BlackSmith() for x in range(20)] + [Castle() for x in range(20)] + [Cart() for x in range(20)] + [Kingdom() for x in range(20)]
        self.deck = self.soldier_cards + self.mage_cards + self.builder_cards
        random.shuffle(self.deck)

    def apply_abilities(self):
        self.discard[0].ability()

    def next_player_active(self):
        self.active_player = self.active_player.opponent

    def display_discard(self):
        if self.discard:
            self.screen.blit(self.discard[0].surf, self.discard_rect)

    def draw_hands(self):
        while len(redplayer.hand) < 5:
            redplayer.hand.append(self.deck.pop(0))
        while len(blueplayer.hand) < 5:
            blueplayer.hand.append(self.deck.pop(0))

    def display_time(self):
        self.current_time = int(pygame.time.get_ticks() / 1000)
        self.time_surf = self.paragraph_font.render((str(current_time)), True, (64, 64, 64))
        self.time_rect = self.time_surf.get_rect(center=(450, 75))
        g.screen.blit(time_surf, time_rect)
        return self.current_time

    def event_ticker(self):
        self.event_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.event_timer, 5000)


g = Game()
redplayer = RedCastle()
blueplayer = BlueCastle()
g.setup()
g.determine_opponent()
g.build_deck()
timer = Timer(1000)
timer2 = Timer(3000)
g.draw_hands()
g.event_ticker()

# USEREVENT Timer


#game_time = 0


#main game loop
while g.run:
    g.clock.tick(60)
    #loops through all possible events within pygame
    #now we can check event occurances within that loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                g.start = True
            if event.key == pygame.K_g:
                redplayer.health = 0
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos

        if g.start:
            if timer.wait and timer2.wait == False:
                g.active_player.handle_inputs()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    g.start = True
        if event.type == g.event_timer:
            g.clouds_list.append(g.cloud_surf.get_rect(center=(random.randrange(915,950),random.randrange(25,250))))
            print(g.clouds_list)
            pass

    if g.start:

        g.display_game_screen()
        timer.check()
        timer2.check()
        g.blit_cloud()
        g.display_discard()
        g.display_stats()
        blit_things()

        if g.state == "upkeep":
            g.active_player.upkeep()
            g.state = "start"
        if g.state == "start":
            g.state = g.handle_inputs()
        if g.state == "play":
            g.active_player.play_card()
            g.apply_abilities()
            g.state = "clean"
        if g.state == "clean":
            if timer.wait == False:
                g.active_player.refresh_hand()
                if timer2.wait == False:
                    g.clouds_list.append(g.cloud_surf.get_rect())
                    g.next_player_active()
                    g.state = "upkeep"

        if redplayer.health <= 0 or blueplayer.health <= 0:
            g.state = "gameover"

        if redplayer.health >= 100 or blueplayer.health >= 100:
            g.state = "gameover"

    elif g.start == False or g.state == "gameover":
        g.display_home_screen()

    pygame.display.update()
    #tells the while run loop to not run faster than 60 times per second