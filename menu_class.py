import pygame
import pygame_textinput12
import json  # for storing the progress in database on json format
import time
import matplotlib.pyplot as plt


class Menu():
    def __init__(self, game_class):
        self.game = game_class
        self.mid_w, self.mid_h = self.game.DISPLAY_W/2, self.game.DISPLAY_H/2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.little_offset = -50
        self.offset = -100
        self.big_offset = -150
        self.user_icon_off = pygame.transform.scale(pygame.image.load('user_icon_off.jpg'),
                                                    (75, 50))
        self.user_icon_on = pygame.transform.scale(pygame.image.load('user_icon_on.jpg'),
                                                   (75, 50))

    def draw_cursor(self):
        self.game.draw_text('>', 15, self.cursor_rect.x, self.cursor_rect.y)

    def read_db(self):
        try:
            udb = open('udb.db', "r")
        except:
            # print('Failed to open database database')
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        try:
            dicT = json.load(udb)
            udb.close()
            return dicT
        except:
            return {}

    def clear_patient(self, patient):
        whole = self.read_db()
        whole.pop(patient)
        udb = open('udb.db', 'w')
        json.dump(whole, udb)
        udb.close()

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        if self.game.typed in self.read_db():
            self.game.window.blit(
                self.user_icon_on, (self.game.DISPLAY_W - 100, 15))
        else:
            self.game.window.blit(self.user_icon_off,
                                  (self.game.DISPLAY_W - 100, 15))

        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game_class):
        Menu.__init__(self, game_class)
        self.state = 'Start'
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.funx, self.funy = self.mid_w, self.mid_h + 50
        self.creditx, self.credity = self.mid_w, self.mid_h + 70
        self.quitx, self.quity = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            if self.game.typed in self.read_db():
                self.game.draw_text(
                    'Logged on', 15, self.game.DISPLAY_W - 50, 75)
            else:
                self.game.draw_text(
                    'Logged off', 15, self.game.DISPLAY_W - 50, 75)
            self.game.draw_text(
                'Main Menu', 30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 20)
            self.game.draw_text('Start Training', 25, self.startx, self.starty)
            self.game.draw_text('Play for fun', 25, self.funx, self.funy)
            self.game.draw_text('Credits', 25, self.creditx, self.credity)
            self.game.draw_text('Quit', 25, self.quitx, self.quity)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.funx + self.offset, self.funy)
                self.state = 'fun'
            elif self.state == "fun":
                self.cursor_rect.midtop = (
                    self.creditx + self.offset, self.credity)
                self.state = 'Credits'
            elif self.state == "Credits":
                self.cursor_rect.midtop = (
                    self.quitx + self.offset, self.quity)
                self.state = 'quit'
            elif self.state == "quit":
                self.cursor_rect.midtop = (
                    self.startx + self.offset, self.starty)
                self.state = 'Start'

        elif self.game.UP_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (
                    self.quitx + self.offset, self.quity)
                self.state = 'quit'
            elif self.state == "fun":
                self.cursor_rect.midtop = (
                    self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == "quit":
                self.cursor_rect.midtop = (
                    self.creditx + self.offset, self.credity)
                self.state = 'Credits'
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.funx + self.offset, self.funy)
                self.state = 'fun'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.run_display = False
                self.game.curr_menu = self.game.welcome
                self.game.option_state = 'serious'
            elif self.state == 'fun':
                self.game.curr_menu = self.game.optional_control
                self.run_display = False
                self.game.option_state = 'have_fun'
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
                self.run_display = False
            elif self.state == 'quit':
                self.run_display = False
                self.game.running = False


class Welcome(Menu):
    def __init__(self, game_class):
        Menu.__init__(self, game_class)
        self.state = 'new'
        self.newx, self.newy = self.mid_w, self.mid_h + 20
        self.existx, self.existy = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.newx + self.big_offset, self.newy)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            if self.game.typed in self.read_db():
                self.game.draw_text(
                    'Logged on', 15, self.game.DISPLAY_W - 50, 75)
            else:
                self.game.draw_text(
                    'Logged off', 15, self.game.DISPLAY_W - 50, 75)
            self.game.draw_text('Hello, I\'m HPRS!', 30,
                                self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
            self.game.draw_text('Are you a new user?',
                                25, self.newx, self.newy)
            self.game.draw_text('OR', 20, self.mid_w, self.mid_h + 40)
            self.game.draw_text('Existing user', 25, self.existx, self.existy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.log_out()
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'new':
                self.state = 'exist'
                self.cursor_rect.midtop = (
                    self.existx + self.offset, self.existy)
            elif self.state == 'exist':
                self.state = 'new'
                self.cursor_rect.midtop = (
                    self.newx + self.big_offset, self.newy)
        elif self.game.START_KEY:
            if self.state == "new":
                self.game.curr_menu = self.game.new
                self.run_display = False
            elif self.state == "exist":
                self.game.curr_menu = self.game.existings
                self.run_display = False


class Credits(Menu):
    def __init__(self, game_class):
        Menu.__init__(self, game_class)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            if self.game.typed in self.read_db():
                self.game.draw_text(
                    'Logged on', 15, self.game.DISPLAY_W - 50, 75)
            else:
                self.game.draw_text(
                    'Logged off', 15, self.game.DISPLAY_W - 50, 75)
            self.game.draw_text(
                'Credits', 30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 20)
            self.game.draw_text(
                'Made by Elia', 25, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 10)
            self.blit_screen()


class OptionControl(Menu):
    def __init__(self, game_class):
        Menu.__init__(self, game_class)
        self.state = 'fingers'
        self.fingersx, self.fingersy = self.mid_w, self.mid_h + 20
        self.handx, self.handy = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.fingersx + self.offset, self.fingersy)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            if self.game.typed in self.read_db():
                self.game.draw_text(
                    'Logged on', 15, self.game.DISPLAY_W - 50, 75)
            else:
                self.game.draw_text(
                    'Logged off', 15, self.game.DISPLAY_W - 50, 75)
            self.game.draw_text('What do you want to control with.', 30, self.game.DISPLAY_W/2,
                                self.game.DISPLAY_H/2 - 30)
            self.game.draw_text('Fingers', 25, self.fingersx, self.fingersy)
            self.game.draw_text('OR', 10, self.mid_w, self.mid_h + 40)
            self.game.draw_text('Hand', 25, self.handx, self.handy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            if self.game.critical_state == 'registered':
                counting = 0
                while counting < 1:
                    self.game.display.fill(self.game.BLACK)
                    self.game.draw_text("Please let\'s first check how the paralysis is",
                                        30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2)
                    self.blit_screen()
                    time.sleep(4)
                    counting += 1
            else:
                self.game.log_out()
                self.game.curr_menu = self.game.main_menu
                self.run_display = False

        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'fingers':
                self.state = 'hand'
                self.cursor_rect.midtop = (
                    self.handx + self.offset, self.handy)
            elif self.state == 'hand':
                self.state = 'fingers'
                self.cursor_rect.midtop = (
                    self.fingersx + self.offset, self.fingersy)

        elif self.game.START_KEY:
            if self.state == 'fingers':
                self.game.curr_menu = self.game.fingerss
                self.run_display = False

            elif self.state == 'hand':
                self.run_display = False
                self.game.knowing = 'hand'
                if self.game.option_state == 'serious':
                    if self.game.critical_state == 'registered':
                        counting = 0
                        while counting < 1:
                            for a in [5, 4, 3, 2, 1]:
                                self.game.display.fill(self.game.BLACK)
                                self.game.draw_text(
                                    'Lets start analysis in, ' + str(a), 30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
                                self.blit_screen()
                                time.sleep(1)
                            counting += 1
                        self.game.curr_menu = self.game.checkingparalysis
                        self.game.option_state = ''
                        self.game.critical_state = ''

                    else:
                        counting = 0
                        while counting < 1:
                            for a in [5, 4, 3, 2, 1]:
                                self.game.display.fill(self.game.BLACK)
                                self.game.draw_text(
                                    'Lets start training in, ' + str(a), 30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
                                self.game.window.blit(
                                    self.game.display, (0, 0))
                                pygame.display.update()
                                self.game.reset_keys()
                                time.sleep(1)
                            counting += 1
                        self.game.curr_menu = self.game.seriousgameloop
                        self.game.option_state = ''

                elif self.game.option_state == 'have_fun':
                    counting = 0
                    while counting < 1:
                        for a in [5, 4, 3, 2, 1]:
                            self.game.display.fill(self.game.BLACK)
                            self.game.draw_text(
                                'Lets start playing in, ' + str(a), 30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
                            self.blit_screen()
                            time.sleep(1)
                        counting += 1
                    self.game.curr_menu = self.game.fungameloop
                    self.game.option_state = ''

# Choosing finger to control with


class Fingers(Menu):
    def __init__(self, game_class):
        Menu.__init__(self, game_class)
        self.state = 'thumb'
        self.thumbx, self.thumby = self.mid_w, self.mid_h + 10
        self.indexx, self.indexy = self.mid_w, self.mid_h + 30
        self.middlex, self.middley = self.mid_w, self.mid_h + 50
        self.ringx, self.ringy = self.mid_w, self.mid_h + 70
        self.littlex, self.littley = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (
            self.thumbx + self.little_offset, self.thumby)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            if self.game.typed in self.read_db():
                self.game.draw_text(
                    'Logged on', 15, self.game.DISPLAY_W - 50, 75)
            else:
                self.game.draw_text(
                    'Logged off', 15, self.game.DISPLAY_W - 50, 75)
            self.game.draw_text(
                'Choose finger:', 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
            self.game.draw_text('Thumb', 15, self.thumbx, self.thumby)
            self.game.draw_text('Index', 15, self.indexx, self.indexy)
            self.game.draw_text('Middle', 15, self.middlex, self.middley)
            self.game.draw_text('Ring', 15, self.ringx, self.ringy)
            self.game.draw_text('Little', 15, self.littlex, self.littley)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.log_out()
            self.game.curr_menu = self.game.optional_control
            self.run_display = False

        elif self.game.DOWN_KEY:
            if self.state == 'thumb':
                self.state = 'index'
                self.cursor_rect.midtop = (
                    self.indexx + self.little_offset, self.indexy)
            elif self.state == 'index':
                self.state = 'middle'
                self.cursor_rect.midtop = (
                    self.middlex + self.little_offset, self.middley)
            elif self.state == 'middle':
                self.state = 'ring'
                self.cursor_rect.midtop = (
                    self.ringx + self.little_offset, self.ringy)
            elif self.state == 'ring':
                self.state = 'little'
                self.cursor_rect.midtop = (
                    self.littlex + self.little_offset, self.littley)
            elif self.state == 'little':
                self.state = 'thumb'
                self.cursor_rect.midtop = (
                    self.thumbx + self.little_offset, self.thumby)

        elif self.game.UP_KEY:
            if self.state == 'thumb':
                self.state = 'little'
                self.cursor_rect.midtop = (
                    self.littlex + self.little_offset, self.littley)
            elif self.state == 'little':
                self.state = 'ring'
                self.cursor_rect.midtop = (
                    self.ringx + self.little_offset, self.ringy)
            elif self.state == 'ring':
                self.state = 'middle'
                self.cursor_rect.midtop = (
                    self.middlex + self.little_offset, self.middley)
            elif self.state == 'middle':
                self.state = 'index'
                self.cursor_rect.midtop = (
                    self.indexx + self.little_offset, self.indexy)
            elif self.state == 'index':
                self.state = 'thumb'
                self.cursor_rect.midtop = (
                    self.thumbx + self.little_offset, self.thumby)

        elif self.game.START_KEY:
            if self.game.option_state == 'serious':
                if self.game.critical_state == 'registered':
                    if self.state == 'thumb':
                        self.game.knowing = 'thumb'
                        self.run_display = False
                    elif self.state == 'index':
                        self.game.knowing = 'index'
                        self.run_display = False
                    elif self.state == 'middle':
                        self.game.knowing = 'middle'
                        self.run_display = False
                    elif self.state == 'ring':
                        self.game.knowing = 'ring'
                        self.run_display = False
                    elif self.state == 'little':
                        self.game.knowing = 'little'
                        self.run_display = False
                    counting = 0
                    while counting < 1:
                        for a in [5, 4, 3, 2, 1]:
                            self.game.display.fill(self.game.BLACK)
                            self.game.draw_text(
                                'Lets start analysis in, ' + str(a), 30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
                            self.blit_screen()
                            time.sleep(1)
                        counting += 1
                    self.game.curr_menu = self.game.checkingparalysis
                    self.game.option_state = ''
                    self.game.critical_state = ''

                else:
                    if self.state == 'thumb':
                        self.game.knowing = 'thumb'
                        self.run_display = False
                    elif self.state == 'index':
                        self.game.knowing = 'index'
                        self.run_display = False
                    elif self.state == 'middle':
                        self.game.knowing = 'middle'
                        self.run_display = False
                    elif self.state == 'ring':
                        self.game.knowing = 'ring'
                        self.run_display = False
                    elif self.state == 'little':
                        self.game.knowing = 'little'
                        self.run_display = False
                    counting = 0
                    while counting < 1:
                        for a in [5, 4, 3, 2, 1]:
                            self.game.display.fill(self.game.BLACK)
                            self.game.draw_text(
                                'Lets start training in, ' + str(a), 30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
                            self.blit_screen()
                            time.sleep(1)
                        counting += 1
                    self.game.curr_menu = self.game.seriousgameloop
                    self.game.option_state = ''

            elif self.game.option_state == 'have_fun':
                if self.state == 'thumb':
                    self.game.knowing = 'thumb'
                    self.run_display = False
                elif self.state == 'index':
                    self.game.knowing = 'index'
                    self.run_display = False
                elif self.state == 'middle':
                    self.game.knowing = 'middle'
                    self.run_display = False
                elif self.state == 'ring':
                    self.game.knowing = 'ring'
                    self.run_display = False
                elif self.state == 'little':
                    self.game.knowing = 'little'
                    self.run_display = False
                counting = 0
                while counting < 1:
                    for a in [5, 4, 3, 2, 1]:
                        self.game.display.fill(self.game.BLACK)
                        self.game.draw_text(
                            'Lets start playing in, ' + str(a), 30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
                        self.blit_screen()
                        time.sleep(1)
                    counting += 1
                self.game.curr_menu = self.game.fungameloop
                self.game.option_state = ''

# Existing user's menu


class Existing(Menu):
    def __init__(self, game_class):
        Menu.__init__(self, game_class)

        self.typedx, self.typedy = self.mid_w, self.mid_h + 20
        self.submitx, self.submity = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (
            self.submitx + self.little_offset, self.submity)
        self.textinput = pygame_textinput12.TextInput()

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            if self.game.typed in self.read_db():
                self.game.draw_text(
                    'Logged on', 15, self.game.DISPLAY_W - 50, 75)
            else:
                self.game.draw_text(
                    'Logged off', 15, self.game.DISPLAY_W - 50, 75)
            self.game.draw_text('What\'s your name? (Start typing)',
                                30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
            self.game.draw_text('Submit', 25, self.submitx, self.submity)
            self.textinput.update(pygame.event.get())
            self.game.draw_text(self.textinput.get_text(),
                                25, self.typedx, self.typedy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.START_KEY:
            self.game.typed = self.textinput.get_text().lower()
            self.database()

    def read_db(self):
        try:
            udb = open('udb.db', "r")
        except:
            # print('Failed to open database database')
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        try:
            dicT = json.load(udb)
            udb.close()
            return dicT
        except:
            return {}

    def database(self):
        if self.game.typed in self.read_db():
            self.game.num = self.read_db()[self.game.typed].get('score')[-1]
            # print(self.game.num)
            self.game.curr_menu = self.game.submit
            self.run_display = False
        else:
            counting = 0
            while counting < 1:
                self.game.display.fill(self.game.BLACK)
                self.game.draw_text(
                    f"Sorry, I dont know {self.game.typed}", 30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
                self.game.draw_text(
                    "Can you please register", 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2)
                self.blit_screen()
                time.sleep(5)
                counting += 1
            self.game.option_state = 'serious'
            self.game.log_out()
            self.game.curr_menu = self.game.welcome
            self.run_display = False


class Submit(Existing):
    def __init__(self, game_class):
        # Menu.__init__(self, game_class)
        Existing.__init__(self, game_class)
        self.state = 'progress'
        self.progressx, self.progressy = self.mid_w, self.mid_h + 20
        self.proceedx, self.proceedy = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (
            self.progressx + (self.big_offset - 60), self.progressy)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            if self.game.typed in self.read_db():
                self.game.draw_text(
                    'Logged on', 15, self.game.DISPLAY_W - 50, 75)
            else:
                self.game.draw_text(
                    'Logged off', 15, self.game.DISPLAY_W - 50, 75)
            self.game.draw_text('Welcome Back, ' + self.game.typed,
                                30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
            self.game.draw_text('Youre past score was: ' +
                                str(self.game.num), 15, self.mid_w, self.mid_h)
            self.game.draw_text(
                'Do you want to see your progress?', 25, self.progressx, self.progressy)
            self.game.draw_text('OR', 15, self.mid_w, self.mid_h + 40)
            self.game.draw_text('Proceed with training', 25,
                                self.proceedx, self.proceedy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.log_out()
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'progress':
                self.state = 'proceed'
                self.cursor_rect.midtop = (
                    self.proceedx + self.big_offset, self.proceedy)
            elif self.state == 'proceed':
                self.state = 'progress'
                self.cursor_rect.midtop = (
                    self.progressx + (self.big_offset - 60), self.progressy)

        elif self.game.START_KEY:
            if self.state == "progress":
                plt.plot(self.read_db()[self.game.typed].get('score'))
                plt.xlim(0, len(self.read_db()[self.game.typed].get('score')))
                plt.ylabel("Your scores.")
                plt.xlabel("Number of plays")
                plt.show()
                self.game.curr_menu = self.game.submit
                self.run_display = False
            elif self.state == "proceed":
                # self.game.typed = ''
                self.game.curr_menu = self.game.optional_control
                self.run_display = False

# New users' menu


class New(Menu):
    def __init__(self, game_class):
        Menu.__init__(self, game_class)
        self.nextx, self.nexty = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.nextx + self.offset, self.nexty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            if self.game.typed in self.read_db():
                self.game.draw_text(
                    'Logged on', 15, self.game.DISPLAY_W - 50, 75)
            else:
                self.game.draw_text(
                    'Logged off', 15, self.game.DISPLAY_W - 50, 75)
            self.game.draw_text(
                'Your Welcome', 30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
            self.game.draw_text(
                'As i introduced myself, I\'m HPRS', 20, self.mid_w, self.mid_h + 20)
            self.game.draw_text(
                'i am going to help you throughout your rehabilitation process.', 20, self.mid_w, self.mid_h + 40)
            self.game.draw_text('Register', 15, self.nextx, self.nexty)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.log_out()
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

        elif self.game.START_KEY:
            self.game.curr_menu = self.game.register
            self.run_display = False


class Register(Existing):
    def __init__(self, game_class):
        # Menu.__init__(self, game_class)
        Existing.__init__(self, game_class)

        self.typedx, self.typedy = self.mid_w, self.mid_h + 20
        self.submitx, self.submity = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (
            self.submitx + self.little_offset, self.submity)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.display.fill(self.game.BLACK)
            self.game.check_events()
            self.check_input()
            if self.game.typed in self.read_db():
                self.game.draw_text(
                    'Logged on', 15, self.game.DISPLAY_W - 50, 75)
            else:
                self.game.draw_text(
                    'Logged off', 15, self.game.DISPLAY_W - 50, 75)
            self.game.draw_text('Can you give me your name and age separated by comma',
                                30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
            self.game.draw_text('Submit', 25, self.submitx, self.submity)
            # Feed it with events every frame
            self.textinput.update(pygame.event.get())
            self.game.draw_text(self.textinput.get_text(),
                                25, self.typedx, self.typedy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.START_KEY:
            self.game.typed = self.textinput.get_text().lower()
            self.database()

    def update_db(self, newdata, clear=False):
        data = self.read_db()
        data.update(newdata)
        # wdb = dict(data.items() + newdata.items())
        udb = open('udb.db', 'w')
        json.dump(data, udb)
        udb.close()

    def adduser(self, name, age):
        self.update_db({name: {'score': [0], 'age': age}})

    def database(self):
        name_age = self.game.typed.split(', ')
        try:
            if name_age[0] in self.read_db():
                counting = 0
                while counting < 1:
                    self.game.display.fill(self.game.BLACK)
                    self.game.draw_text(
                        'Name exists', 30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
                    self.blit_screen()
                    time.sleep(2)
                    counting += 1
                self.game.curr_menu = self.game.register
                self.run_display = False
                self.game.typed = ''

            else:
                self.adduser(name_age[0], name_age[1])
                # print(self.game.typed)
                self.game.curr_menu = self.game.next_one
                self.run_display = False
                self.game.typed = name_age[0]
        except:
            counting = 0
            while counting < 1:
                self.game.display.fill(self.game.BLACK)
                self.game.draw_text("Invalid Format ", 30, self.game.DISPLAY_W/2,
                                    self.game.DISPLAY_H/2 - 20, color=(255, 0, 0))
                self.game.draw_text(
                    "Register as instructed", 25, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2)
                self.blit_screen()
                time.sleep(5)
                counting += 1


class NextOne(Menu):
    def __init__(self, game_class):
        Menu.__init__(self, game_class)
        self.nextx, self.nexty = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.nextx + self.little_offset, self.nexty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            if self.game.typed in self.read_db():
                self.game.draw_text(
                    'Logged on', 15, self.game.DISPLAY_W - 50, 75)
            else:
                self.game.draw_text(
                    'Logged off', 15, self.game.DISPLAY_W - 50, 75)
            self.game.draw_text(
                'Just make sure to attend as instructed by your doctor.', 20, self.mid_w, self.mid_h + 20)
            self.game.draw_text('Next', 15, self.nextx, self.nexty)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            counting = 0
            while counting < 1:
                self.game.display.fill(self.game.BLACK)
                self.game.draw_text("Your registered account is DELETED ",
                                    30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2)
                self.blit_screen()
                time.sleep(3)
                counting += 1
            self.clear_patient(self.game.typed)
            self.game.log_out()
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

        elif self.game.START_KEY:
            self.game.curr_menu = self.game.next_two
            self.run_display = False


class NextTwo(Menu):
    def __init__(self, game_class):
        Menu.__init__(self, game_class)
        self.nextx, self.nexty = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.nextx + self.little_offset, self.nexty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            if self.game.typed in self.read_db():
                self.game.draw_text(
                    'Logged on', 15, self.game.DISPLAY_W - 50, 75)
            else:
                self.game.draw_text(
                    'Logged off', 15, self.game.DISPLAY_W - 50, 75)
            self.game.draw_text(
                'Let\'s first see how critical the paralysis is.', 20, self.mid_w, self.mid_h + 20)
            self.game.draw_text('Start', 15, self.nextx, self.nexty)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            counting = 0
            while counting < 1:
                self.game.display.fill(self.game.BLACK)
                self.game.draw_text("Your registered account is DELETED ",
                                    30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2)
                self.blit_screen()
                time.sleep(3)
                counting += 1
            self.clear_patient(self.game.typed)
            self.game.log_out()
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

        elif self.game.START_KEY:
            self.game.critical_state = 'registered'
            self.game.curr_menu = self.game.optional_control
            self.run_display = False


class Well(Menu):
    def __init__(self, game_class):
        Menu.__init__(self, game_class)
        self.state = 'playing'
        self.playingx, self.playingy = self.mid_w, self.mid_h + 20
        self.realpx, self.realpy = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (
            self.playingx + self.big_offset, self.playingy)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            if self.game.typed in self.read_db():
                self.game.draw_text(
                    'Logged on', 15, self.game.DISPLAY_W - 50, 75)
            else:
                self.game.draw_text(
                    'Logged off', 15, self.game.DISPLAY_W - 50, 75)
            self.game.draw_text('You are very good, this makes me wonder.', 30, self.game.DISPLAY_W/2,
                                self.game.DISPLAY_H/2 - 30)
            self.game.draw_text('Are you just playing', 25,
                                self.playingx, self.playingy)
            self.game.draw_text('OR', 10, self.mid_w, self.mid_h + 40)
            self.game.draw_text('Real patient', 25, self.realpx, self.realpy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            counting = 0
            while counting < 1:
                self.game.display.fill((0, 0, 0))
                self.game.draw_text("Sorry, can i know if you are a real patient or just playing",
                                    30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2)
                self.blit_screen()
                time.sleep(4)
                counting += 1
            # self.game.curr_menu = self.game.main_menu
            # self.run_display = False

        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'playing':
                self.state = 'realp'
                self.cursor_rect.midtop = (
                    self.realpx + self.offset, self.realpy)
            elif self.state == 'realp':
                self.state = 'playing'
                self.cursor_rect.midtop = (
                    self.playingx + self.big_offset,  self.playingy)

        elif self.game.START_KEY:
            if self.state == 'playing':
                counting = 0
                while counting < 1:
                    self.game.display.fill(self.game.BLACK)
                    self.game.draw_text(
                        "Go for 'Play for fun' ", 30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
                    self.game.draw_text("Your registered account is DELETED ",
                                        30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2)
                    self.blit_screen()
                    time.sleep(3)
                    counting += 1
                self.clear_patient(self.game.typed)
                self.game.log_out()
                self.game.curr_menu = self.game.main_menu
                self.run_display = False

            elif self.state == 'realp':
                self.game.curr_menu = self.game.realplayer
                self.run_display = False


class RealPatient(Menu):
    def __init__(self, game_class):
        Menu.__init__(self, game_class)
        self.procedx, self.procedy = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (
            self.procedx + self.big_offset, self.procedy)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            if self.game.typed in self.read_db():
                self.game.draw_text(
                    'Logged on', 15, self.game.DISPLAY_W - 50, 75)
            else:
                self.game.draw_text(
                    'Logged off', 15, self.game.DISPLAY_W - 50, 75)
            self.game.draw_text(
                f'Well, you are doing very good {self.game.typed}, this will be easy you are almost cured', 20, self.mid_w, self.mid_h + 20)
            self.game.draw_text('Proceed with training', 15,
                                self.procedx, self.procedy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            counting = 0
            while counting < 1:
                self.game.display.fill(self.game.BLACK)
                self.game.draw_text("Thanks for allowing us to analyse the paralysis",
                                    30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
                self.game.draw_text(
                    "see you soon", 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2)
                self.blit_screen()
                time.sleep(4)
                counting += 1
            self.game.curr_menu = self.game.main_menu
            self.game.log_out()
            self.run_display = False

        elif self.game.START_KEY:
            self.game.curr_menu = self.game.optional_control
            self.game.option_state = 'serious'
            self.run_display = False


class Critical(Menu):
    def __init__(self, game_class):
        Menu.__init__(self, game_class)
        self.state = 'proceedd'
        self.proceedx, self.proceedy = self.mid_w, self.mid_h + 10
        self.quittx, self.quitty = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (
            self.proceedx + self.little_offset, self.proceedy)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            if self.game.typed in self.read_db():
                self.game.draw_text(
                    'Logged on', 15, self.game.DISPLAY_W - 50, 75)
            else:
                self.game.draw_text(
                    'Logged off', 15, self.game.DISPLAY_W - 50, 75)
            self.game.draw_text('Not very bad, don\'t worry we will be together to the end',
                                30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
            self.game.draw_text('Proceed with training', 25,
                                self.proceedx, self.proceedy)
            self.game.draw_text('Quit', 25, self.quittx, self.quitty)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.game.log_out()
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'proceedd':
                self.state = 'quitt'
                self.cursor_rect.midtop = (
                    self.quittx + self.little_offset, self.quitty)
            elif self.state == 'quitt':
                self.state = 'proceedd'
                self.cursor_rect.midtop = (
                    self.proceedx + self.little_offset, self.proceedy)
        elif self.game.START_KEY:
            if self.state == "quitt":
                self.run_display = False
                self.game.curr_menu = self.game.main_menu
                self.game.log_out()
            elif self.state == "proceedd":
                self.game.curr_menu = self.game.optional_control
                self.game.option_state = 'serious'
                self.run_display = False

# class Proceed(Menu):
