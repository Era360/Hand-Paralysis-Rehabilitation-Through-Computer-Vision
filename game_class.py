import pygame
from menu_class import *
from game_loop_class import *


class Game():
    def __init__(self):
        pygame.init()

        # Creating Global variables
        self.typed = ''
        self.knowing = ''
        self.stat = []
        self.scores = []
        self.player_score = 0
        self.num = ''
        self.option_state = ''
        self.critical_state = ''

        self.running = True
        self.UP_KEY, self.DOWN_KEY, self.BACK_KEY, self.START_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1280, 708   # 1360, 568

        # Window initiation
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.font = pygame.font.get_default_font()  # getting default font
        self.BLACK, self.WHITE = (25, 25, 25), (255, 255, 255)

        # User Interface options
        ####################################
        self.main_menu = MainMenu(self)
        self.optional_control = OptionControl(self)
        self.credits = Credits(self)

        self.welcome = Welcome(self)

        # for new user
        self.new = New(self)
        self.register = Register(self)
        self.next_one = NextOne(self)
        self.next_two = NextTwo(self)
        self.well = Well(self)
        self.realplayer = RealPatient(self)

        # for existing user
        self.existings = Existing(self)
        self.submit = Submit(self)

        self.fingerss = Fingers(self)

        # Game loop options
        self.seriousgameloop = SeriousGameloops(self)
        self.fungameloop = fungameloop(self)
        self.checkingparalysis = CheckingParalysisGameLoop(self)
        self.tempo = Tempo(self)

        self.critical = Critical(self)

        # the displaying option
        self.curr_menu = self.main_menu
        ####################################

    def check_input(self):
        if self.BACK_KEY:
            self.curr_menu = self.main_menu
            self.run_display = False

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.curr_menu.run_display = False
                self.run_display = False
                # self.draw_text(f'Your score is {player_score}', 40, self.DISPLAY_W/2, self.DISPLAY_H/2)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.curr_menu.run_display = False
                    self.run_display = False
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.BACK_KEY, self.START_KEY = False, False, False, False

    def draw_text(self, text, size, x, y, color=(255, 255, 255)):
        font = pygame.font.Font(self.font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def log_out(self):
        self.typed = ''
        self.knowing = ''
        self.stat = []
        self.scores = []
        self.player_score = 0
