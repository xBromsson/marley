#!/usr/bin/env python3

import pygame
import random
from sys import exit


class Player:
    def __init__(self):
        self.health = 30
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
        self.active_surf = pygame.image.load(
            "graphics/castle_red_turn.png"
        ).convert_alpha()
        self.rect = self.surf.get_rect(topleft=(50, 250))

    def blit_castle(self):
        if g.active_player == g.redplayer:
            g.screen.blit(self.active_surf, self.rect)
        else:
            g.screen.blit(self.surf, self.rect)

    def blit_cards(self):
        for i, card in enumerate(self.hand):
            card.move_to(((i + 1) * (g.width / (len(self.hand) + 1))), 525)
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
        self.active_surf = pygame.image.load(
            "graphics/castle_blue_turn.png"
        ).convert_alpha()
        self.rect = self.surf.get_rect(topright=(850, 250))

    def blit_castle(self):
        if g.active_player == g.blueplayer:
            g.screen.blit(self.active_surf, self.rect)
        else:
            g.screen.blit(self.surf, self.rect)

    def blit_cards(self):
        for i, card in enumerate(self.hand):
            card.move_to(((i + 1) * (g.width / (len(self.hand) + 1))), 525)
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


class Timer:
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


class Card:
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
        self.surf = pygame.image.load("graphics/catapult.png").convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 12

    def ability(self):
        g.active_player.opponent.health -= 15


class Warrior(Soldier):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("graphics/warrior.png").convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 4

    def ability(self):
        g.active_player.opponent.health -= 7


class King(Soldier):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("graphics/king.png").convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 8

    def ability(self):
        g.active_player.opponent.health -= 10


class Archer(Soldier):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("graphics/archer.png").convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 5

    def ability(self):
        g.active_player.opponent.swords -= random.randrange(5)
        g.active_player.opponent.crystals -= random.randrange(5)
        g.active_player.opponent.bricks -= random.randrange(5)


class Fire(Soldier):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("graphics/fire.png").convert_alpha()
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
        self.surf = pygame.image.load("graphics/spellbook.png").convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 12
        # self.draw = 3

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
        self.surf = pygame.image.load("graphics/confusion.png").convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 15

    def ability(self):
        g.active_player.opponent.hand.remove(
            random.choice(g.active_player.opponent.hand)
        )
        g.active_player.opponent.hand.remove(
            random.choice(g.active_player.opponent.hand)
        )


class Dragon(Mage):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("graphics/dragon.png").convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 25

    def ability(self):
        g.active_player.opponent.health -= 35


class Wizard(Mage):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("graphics/wizard.png").convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 8

    def ability(self):
        g.active_player.mages += 1


class Scroll(Mage):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("graphics/scroll.png").convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 8

    def ability(self):
        g.active_player.hand.insert(0, random.choice(g.active_player.opponent.hand))


class Gate(Builder):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("graphics/gate.png").convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 7

    def ability(self):
        g.active_player.health += 10


class BlackSmith(Builder):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("graphics/blacksmith.png").convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 8

    def ability(self):
        g.active_player.soldiers += 1


class Castle(Builder):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("graphics/castle.png").convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 12

    def ability(self):
        g.active_player.health += 15


class Cart(Builder):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("graphics/cart.png").convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 12

    def ability(self):
        g.active_player.swords += 10
        g.active_player.crystals += 10
        g.active_player.bricks += 10


class Kingdom(Builder):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("graphics/kingdom.png").convert_alpha()
        self.rect = self.surf.get_rect()
        self.cost = 17

    def ability(self):
        g.active_player.health += 20


class Game:
    def __init__(self):
        self.init_game()

    def init_game(self):
        pygame.init()
        pygame.display.set_caption("Seige")

        # create and set variables for the game
        self.run = True
        self.state = "home"
        self.start = False
        self.displayed_gameover_message = False
        self.winner = ""
        self.width = 900
        self.height = 600
        self.discard = []
        self.deck = []
        self.active_player = None
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.redplayer = RedCastle()
        self.blueplayer = BlueCastle()
        self.setup()
        self.determine_opponent()
        self.build_deck()
        self.draw_hands()
        self.event_ticker()

        # FONTS
        self.title_font = pygame.font.Font(None, 50)
        self.health_font = pygame.font.Font(None, 40)
        self.stat_font = pygame.font.Font(None, 30)
        self.paragraph_font = pygame.font.Font(None, 25)

        # create rectangle for game title
        self.seige_title = self.title_font.render("SEIGE", True, (64, 64, 64))
        self.seige_title_rect = self.seige_title.get_rect(center=(450, 100))

        # create rectangle for game instructions on start screen
        self.instruction_surf = self.paragraph_font.render(
            "Press Enter To Start", True, (64, 64, 64)
        )
        self.instruction_rect = self.instruction_surf.get_rect(center=(450, 225))

        # create rectangle for game screen background
        self.bg_surf = pygame.image.load("graphics/background.png").convert_alpha()
        self.bg_rect = self.bg_surf.get_rect()

        # create rectangle for discard location
        self.discard_surf = pygame.image.load("graphics/card_back.png").convert_alpha()
        self.discard_rect = self.discard_surf.get_rect(center=(450, 250))

        # create rectangles for housing the end game modal
        self.end_message_surf = pygame.Surface((400, 250))
        self.end_message_surf.fill((255, 255, 255))
        self.end_message_rect = self.end_message_surf.get_rect(center=(450, 300))
        self.end_message_bg_surf = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA
        )
        self.end_message_bg_surf.fill((255, 255, 255, 128))
        self.end_message_bg_rect = self.end_message_bg_surf.get_rect(center=(450, 300))

        # Text for buttons
        self.playAgainTextSurf = self.paragraph_font.render(
            ("Play Again"), True, (0, 0, 0)
        )
        self.playAgainTextRect = self.playAgainTextSurf.get_rect(center=(390, 350))

        self.quitGameTextSurf = self.paragraph_font.render(
            ("Quit Game"), True, (0, 0, 0)
        )
        self.quitGameTextRect = self.quitGameTextSurf.get_rect(center=(510, 350))

        # button rectangles for end screen
        self.playAgainSurf = pygame.Surface((100, 50))
        self.playAgainSurf.fill((128, 128, 128))
        self.playAgainRect = self.playAgainSurf.get_rect(center=(390, 350))

        self.quitGameSurf = pygame.Surface((100, 50))
        self.quitGameSurf.fill((128, 128, 128))
        self.quitGameRect = self.quitGameSurf.get_rect(center=(510, 350))

        # references to icon images
        self.sword_icon_surf = pygame.image.load(
            "graphics/sword_icon.png"
        ).convert_alpha()

        self.crystal_icon_surf = pygame.image.load(
            "graphics/crystal_icon.png"
        ).convert_alpha()

        self.hammer_icon_surf = pygame.image.load(
            "graphics/hammer_icon.png"
        ).convert_alpha()

        self.soldier_icon_surf = pygame.image.load(
            "graphics/soldier_icon.png"
        ).convert_alpha()

        self.wizard_icon_surf = pygame.image.load(
            "graphics/wizard_icon.png"
        ).convert_alpha()

        self.builder_icon_surf = pygame.image.load(
            "graphics/builder_icon.png"
        ).convert_alpha()

    def setup(self):
        self.active_player = self.redplayer

    def reset(self):
        self.init_game()
        self.state = "home"

    def handlePlayAgain(self):
        self.reset()

    def blit_things(self):
        self.redplayer.blit_castle()
        self.blueplayer.blit_castle()
        self.active_player.blit_cards()

    def handle_inputs(self):
        # global game.state
        for i, card in enumerate(g.active_player.hand):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (
                    card.rect.collidepoint(mouse_pos)
                    and event.button == 1
                    and card.playable is True
                ):
                    g.discard.insert(0, g.active_player.hand.pop(i))
                    # self.hand.insert(i, deck.pop(0))
                    g.state = "stack"
                    timer.log_time()
                    timer2.log_time()
                if card.rect.collidepoint(mouse_pos) and event.button == 3:
                    g.active_player.hand.pop(i)
                    # self.hand.insert(i, deck.pop(0))
                    g.state = "clean"
                    timer.log_time()
                    timer2.log_time()
        return g.state

    def display_home_screen(self):
        self.screen.fill("white")
        self.screen.blit(self.seige_title, self.seige_title_rect)
        self.screen.blit(self.instruction_surf, self.instruction_rect)

    # Text for displaying who wins
    def renderWinner(self):
        self.winnerMessageSurf = self.stat_font.render(
            (self.winner + " is the winner!"), True, (64, 64, 64)
        )
        self.winnerMessageRect = self.winnerMessageSurf.get_rect(center=(450, 275))

    def determine_opponent(self):
        self.redplayer.opponent = self.blueplayer
        self.blueplayer.opponent = self.redplayer

    def determine_winner(self):
        if self.redplayer.health <= 0:
            self.winner = "Blue Player"
        elif self.blueplayer.health <= 0:
            self.winner = "Red Player"
        elif self.redplayer.health >= 100:
            self.winner = "Red Player"
        elif self.blueplayer.health >= 100:
            self.winner = "Red Player"

    def display_game_screen(self):
        self.screen.blit(self.bg_surf, self.bg_rect)
        self.screen.blit(self.seige_title, self.seige_title_rect)

    def display_end_game_screen(self):
        print("inside end game")
        self.screen.blit(self.end_message_bg_surf, self.end_message_bg_rect)
        self.screen.blit(self.end_message_surf, self.end_message_rect)
        self.screen.blit(self.winnerMessageSurf, self.winnerMessageRect)
        self.screen.blit(self.playAgainSurf, self.playAgainRect)
        self.screen.blit(self.playAgainTextSurf, self.playAgainTextRect)
        self.screen.blit(self.quitGameSurf, self.quitGameRect)
        self.screen.blit(self.quitGameTextSurf, self.quitGameTextRect)

    def display_stats(self):
        #######################
        # RED PLAYER STATS
        #######################

        # HEALTH STAT
        self.redplayer_health_surf = self.health_font.render(
            (str(self.redplayer.health)), True, (64, 64, 64)
        )
        self.redplayer_health_rect = self.redplayer_health_surf.get_rect(
            center=(215, 285)
        )
        self.screen.blit(self.redplayer_health_surf, self.redplayer_health_rect)

        # SWORD STATS
        # swords icon
        self.redplayer_sword_icon_rect = self.sword_icon_surf.get_rect(center=(75, 225))
        self.screen.blit(self.sword_icon_surf, self.redplayer_sword_icon_rect)
        # swords number
        self.redplayer_sword_surf = self.stat_font.render(
            (str(self.redplayer.swords)), True, (64, 64, 64)
        )
        self.redplayer_sword_rect = self.redplayer_sword_surf.get_rect(center=(90, 225))
        self.screen.blit(self.redplayer_sword_surf, self.redplayer_sword_rect)
        # soldiers icon
        self.redplayer_soldier_icon_rect = self.soldier_icon_surf.get_rect(
            center=(25, 225)
        )
        self.screen.blit(self.soldier_icon_surf, self.redplayer_soldier_icon_rect)
        # soldiers number
        self.redplayer_soldier_surf = self.stat_font.render(
            (str(self.redplayer.soldiers)), True, (64, 64, 64)
        )
        self.redplayer_soldier_rect = self.redplayer_soldier_surf.get_rect(
            center=(40, 225)
        )
        self.screen.blit(self.redplayer_soldier_surf, self.redplayer_soldier_rect)

        # CRYSTAL STATS
        # crystals icon
        self.redplayer_crystal_icon_rect = self.crystal_icon_surf.get_rect(
            center=(75, 250)
        )
        self.screen.blit(self.crystal_icon_surf, self.redplayer_crystal_icon_rect)

        # crystals text
        self.redplayer_crystal_surf = self.stat_font.render(
            (str(self.redplayer.crystals)), True, (64, 64, 64)
        )
        self.redplayer_crystal_rect = self.redplayer_crystal_surf.get_rect(
            center=(90, 250)
        )
        self.screen.blit(self.redplayer_crystal_surf, self.redplayer_crystal_rect)

        # wizard icon
        self.redplayer_wizard_icon_rect = self.wizard_icon_surf.get_rect(
            center=(25, 250)
        )
        self.screen.blit(self.wizard_icon_surf, self.redplayer_wizard_icon_rect)

        # wizard text
        self.redplayer_mages_surf = self.stat_font.render(
            (str(self.redplayer.mages)), True, (64, 64, 64)
        )
        self.redplayer_mages_rect = self.redplayer_mages_surf.get_rect(center=(40, 250))
        self.screen.blit(self.redplayer_mages_surf, self.redplayer_mages_rect)

        # BUILDER STATS
        # hammer icon
        self.redplayer_hammer_icon_rect = self.hammer_icon_surf.get_rect(
            center=(75, 275)
        )
        self.screen.blit(self.hammer_icon_surf, self.redplayer_hammer_icon_rect)

        # hammer text
        self.redplayer_brick_surf = self.stat_font.render(
            (str(self.redplayer.bricks)), True, (64, 64, 64)
        )
        self.redplayer_brick_rect = self.redplayer_brick_surf.get_rect(center=(90, 275))
        self.screen.blit(self.redplayer_brick_surf, self.redplayer_brick_rect)

        # builder icon
        self.redplayer_builder_icon_rect = self.builder_icon_surf.get_rect(
            center=(25, 275)
        )
        self.screen.blit(self.builder_icon_surf, self.redplayer_builder_icon_rect)

        # builder text
        self.redplayer_builders_surf = self.stat_font.render(
            (str(self.redplayer.builders)), True, (64, 64, 64)
        )
        self.redplayer_builders_rect = self.redplayer_builders_surf.get_rect(
            center=(40, 275)
        )
        self.screen.blit(self.redplayer_builders_surf, self.redplayer_builders_rect)

        #######################
        # BLUE PLAYER STATS
        #######################

        # Health Stat
        self.blueplayer_health_surf = self.health_font.render(
            (str(self.blueplayer.health)), True, (64, 64, 64)
        )
        self.blueplayer_health_rect = self.blueplayer_health_surf.get_rect(
            center=(685, 285)
        )
        self.screen.blit(self.blueplayer_health_surf, self.blueplayer_health_rect)

        # Sword Icon
        self.blueplayer_sword_icon_rect = self.sword_icon_surf.get_rect(
            center=(860, 225)
        )
        self.screen.blit(self.sword_icon_surf, self.blueplayer_sword_icon_rect)

        # Sword Text
        self.blueplayer_sword_surf = self.stat_font.render(
            (str(self.blueplayer.swords)), True, (64, 64, 64)
        )
        self.blueplayer_sword_rect = self.blueplayer_sword_surf.get_rect(
            center=(875, 225)
        )
        self.screen.blit(self.blueplayer_sword_surf, self.blueplayer_sword_rect)

        # Soldiers Icon
        self.blueplayer_soldier_icon_rect = self.soldier_icon_surf.get_rect(
            center=(810, 225)
        )
        self.screen.blit(self.soldier_icon_surf, self.blueplayer_soldier_icon_rect)

        # Soldiers Text
        self.blueplayer_soldier_surf = self.stat_font.render(
            (str(self.blueplayer.soldiers)), True, (64, 64, 64)
        )
        self.blueplayer_soldier_rect = self.blueplayer_soldier_surf.get_rect(
            center=(825, 225)
        )
        self.screen.blit(self.blueplayer_soldier_surf, self.blueplayer_soldier_rect)

        # Wizard Icon
        self.blueplayer_wizard_icon_rect = self.wizard_icon_surf.get_rect(
            center=(810, 250)
        )
        self.screen.blit(self.wizard_icon_surf, self.blueplayer_wizard_icon_rect)

        # Wizard Text
        self.blueplayer_mages_surf = self.stat_font.render(
            (str(self.blueplayer.mages)), True, (64, 64, 64)
        )
        self.blueplayer_mages_rect = self.blueplayer_mages_surf.get_rect(
            center=(825, 250)
        )
        self.screen.blit(self.blueplayer_mages_surf, self.blueplayer_mages_rect)

        # Crystal Icon
        self.blueplayer_crystal_icon_rect = self.crystal_icon_surf.get_rect(
            center=(860, 250)
        )
        self.screen.blit(self.crystal_icon_surf, self.blueplayer_crystal_icon_rect)

        # Crystal Text
        self.blueplayer_crystal_surf = self.stat_font.render(
            (str(self.blueplayer.crystals)), True, (64, 64, 64)
        )
        self.blueplayer_crystal_rect = self.blueplayer_crystal_surf.get_rect(
            center=(875, 250)
        )
        self.screen.blit(self.blueplayer_crystal_surf, self.blueplayer_crystal_rect)

        # Builder Icon
        self.blueplayer_builder_icon_rect = self.builder_icon_surf.get_rect(
            center=(810, 275)
        )
        self.screen.blit(self.builder_icon_surf, self.blueplayer_builder_icon_rect)

        # Builder Text
        self.blueplayer_builders_surf = self.stat_font.render(
            (str(self.blueplayer.builders)), True, (64, 64, 64)
        )
        self.blueplayer_builders_rect = self.blueplayer_builders_surf.get_rect(
            center=(825, 275)
        )
        self.screen.blit(self.blueplayer_builders_surf, self.blueplayer_builders_rect)

        # Hammer Icon
        self.blueplayer_hammer_icon_rect = self.hammer_icon_surf.get_rect(
            center=(860, 275)
        )
        self.screen.blit(self.hammer_icon_surf, self.blueplayer_hammer_icon_rect)

        # Hammer Text
        self.blueplayer_brick_surf = self.stat_font.render(
            (str(self.blueplayer.bricks)), True, (64, 64, 64)
        )
        self.blueplayer_brick_rect = self.blueplayer_brick_surf.get_rect(
            center=(875, 275)
        )
        self.screen.blit(self.blueplayer_brick_surf, self.blueplayer_brick_rect)

    def build_deck(self):
        self.soldier_cards = (
            [Catapult() for x in range(20)]
            + [King() for x in range(20)]
            + [Warrior() for x in range(20)]
            + [Archer() for x in range(20)]
            + [Fire() for x in range(20)]
        )
        self.mage_cards = (
            [SpellBook() for x in range(20)]
            + [Confusion() for x in range(20)]
            + [Dragon() for x in range(20)]
            + [Wizard() for x in range(20)]
            + [Scroll() for x in range(20)]
        )
        self.builder_cards = (
            [Gate() for x in range(20)]
            + [BlackSmith() for x in range(20)]
            + [Castle() for x in range(20)]
            + [Cart() for x in range(20)]
            + [Kingdom() for x in range(20)]
        )
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
        while len(self.redplayer.hand) < 5:
            self.redplayer.hand.append(self.deck.pop(0))
        while len(self.blueplayer.hand) < 5:
            self.blueplayer.hand.append(self.deck.pop(0))

    def display_time(self):
        self.current_time = int(pygame.time.get_ticks() / 1000)
        self.time_surf = self.paragraph_font.render(
            (str(self.current_time)), True, (64, 64, 64)
        )
        self.time_rect = self.time_surf.get_rect(center=(450, 75))
        g.screen.blit(self.time_surf, self.time_rect)
        return self.current_time

    def event_ticker(self):
        self.event_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.event_timer, 5000)


# initialize game
g = Game()
timer = Timer(1000)
timer2 = Timer(3000)

# main game loop
while g.run:
    g.clock.tick(60)
    # loops through all possible events within pygame
    # now we can check event occurances within that loop.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                g.state = "upkeep"
            if event.key == pygame.K_g:
                g.redplayer.health = 0
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
        if g.start:
            if timer.wait and timer2.wait is False:
                g.active_player.handle_inputs()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    g.start = True
        if event.type == g.event_timer:
            pass

    # displays main game screen and handles the game loop and interactions.
    if g.start is True:
        g.display_game_screen()
        timer.check()
        timer2.check()
        g.display_discard()
        g.display_stats()
        g.blit_things()

        if g.state == "upkeep":
            g.active_player.upkeep()
            g.state = "play"
        if g.state == "play":
            g.state = g.handle_inputs()
        if g.state == "stack":
            g.active_player.play_card()
            g.apply_abilities()
            g.state = "clean"
        if g.state == "clean":
            if timer.wait is False:
                g.active_player.refresh_hand()
                if timer2.wait is False:
                    g.next_player_active()
                    g.state = "upkeep"

        if g.redplayer.health <= 0 or g.blueplayer.health <= 0:
            g.determine_winner()
            g.renderWinner()
            g.state = "gameover"

        if g.redplayer.health >= 100 or g.blueplayer.health >= 100:
            g.determine_winner()
            g.renderWinner()
            g.state = "gameover"

    if g.state == "gameover":
        g.start = False

        if g.displayed_gameover_message is False:
            g.display_end_game_screen()
            g.displayed_gameover_message = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            print("clicked button")
            if g.playAgainRect.collidepoint(mouse_pos) and event.button == 1:
                g.reset()
            if g.quitGameRect.collidepoint(mouse_pos) and event.button == 1:
                pygame.quit()
                exit()

    if g.state == "home":
        g.start = False
        g.display_home_screen()

    pygame.display.update()
    # tells the while run loop to not run faster than 60 times per second
