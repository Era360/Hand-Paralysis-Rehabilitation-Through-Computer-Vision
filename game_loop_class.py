import pygame
import cv2
import numpy as np
import trackerModule as tr # Module for tracking and returning hand's position on the screen
# import color_tracking as ct
from random import choice  # for randomizing the position of the falling obstacle
import time   # for counting time before the training starts
from menu_class import Register   # for saving the progress to the database in json format
import matplotlib.pyplot as plt  # plotting results' graphs

class SeriousGameloops():
    def __init__(self, game_class):
        self.game = game_class
        pygame.mixer.init()
        pygame.font.init()
        pygame.display.set_caption('Hand paralysis rehab')

        self.cap = cv2.VideoCapture(0)
        
        # tracking intializng
        self.detector = tr.HandDetector()
        # self.detect = ct.Color_Track()
        self.read_database = Register(game_class)

        # configuring game objects
        self.spaceship_width, self.spaceship_height = 45, 30
        self.obstacle_width, self.obstacle_height = 40, 34
        self.quarter_width = int(self.game.DISPLAY_W//4)
        self.right_quarter = int((self.game.DISPLAY_W//2)+ self.quarter_width)

        # Importing required files
        self.HIT_SOUND = pygame.mixer.Sound('grenade.mp3')
        self.HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
        self.WINNER_FONT = pygame.font.SysFont('comicsans', 100)
        
        # self.space = pygame.transform.scale(pygame.image.load('space.jpg'),
        #                                      (self.game.DISPLAY_W, self.game.DISPLAY_H))
        self.spaceship = pygame.transform.rotate(
                                        pygame.transform.scale(
                                                            pygame.image.load('spaceship.png'),
                                                                 (self.spaceship_width, self.spaceship_height)), 180)
        self.obstacle = pygame.transform.scale(pygame.image.load('stone.png'),
                                                 (self.obstacle_width, self.obstacle_height))

        self.fps = 60   
        self.x_positions = []
        for a in range(self.quarter_width, self.right_quarter):
            self.x_positions.append(a)
        self.fingers = {
                        'hand': 0, 
                        'thumb': 4,
                        'index': 8,
                        'middle': 12,
                        'ring': 16,
                        'little': 20
                        }

        self.player = pygame.Rect(100, 500, self.spaceship_width, self.spaceship_height)
        self.clock = pygame.time.Clock()
        self.fail_health = 0
        self.played = 0  # For increasing speed
        
        self.obstacle_vel = 10
        self.stonez = pygame.Rect( 100, 50, self.obstacle_width, self.obstacle_height)
        
    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

    def display_menu(self):
        self.run_display = True
        while self.run_display: 
            success, img = self.cap.read()
            img = cv2.resize(img, (self.game.DISPLAY_W, self.game.DISPLAY_H))

            img = self.detector.find_hands(img, False)
            lm_list = self.detector.find_position(img, draw=True,
                                                     index = self.fingers.get(self.game.knowing))
            inversed_pos = np.interp(lm_list, (0, self.game.DISPLAY_W), (self.game.DISPLAY_W, 0))
            least_pos = np.interp(inversed_pos, (self.quarter_width, self.right_quarter),
                                     (0, self.game.DISPLAY_W))
            
            self.clock.tick(self.fps)       
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.game.stat.append(self.game.player_score)
                    try:
                        # Updating the existing database
                        scores = self.read_database.read_db()[self.game.typed].get('score')[:]
                        scores.append(sum(self.game.stat)//len(self.game.stat)+1)
                        self.read_database.update_db({self.game.typed:{'score':scores, 'age':self.read_database.read_db()[self.game.typed].get('age')}})
                    except:
                        pass
                    self.run_display = False
                    self.game.running = False
            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run_display = False
                        self.fail_health = 0
                        die_text = ""
                        self.game.stat.append(self.game.player_score)
                        try:
                            # Updating the existing database
                            scores = self.read_database.read_db()[self.game.typed].get('score')[:]
                            scores.append(sum(self.game.stat)//len(self.game.stat)+1)
                            self.read_database.update_db({self.game.typed:{'score':scores, 'age':self.read_database.read_db()[self.game.typed].get('age')}})
                        except:
                            pass
                        self.game.log_out()
                        self.game.curr_menu = self.game.main_menu
                        self.blit_screen()
            
            if self.stonez.y < self.player.y - 30:
                # if self.played >= 10 and self.played <= 20:
                #     self.obstacle_vel = 13
                # elif self.played >= 21 and self.played <=30:
                #     self.obstacle_vel = 14
                # elif self.played > 30:
                #     self.obstacle_vel = 18
                self.stonez.y += self.obstacle_vel
                if self.player.colliderect(self.stonez):
                    self.game.player_score += 2
                    self.HIT_SOUND.play()
                    self.played += 1

                elif self.stonez.y == self.player.y -30 and not self.player.colliderect(self.stonez): 
                    self.game.player_score -= 1
                    self.fail_health += 1
                
            else:
                self.stonez.y = 50
                self.stonez.x = self.positioning()    
            
            die_text = ""
            if self.fail_health == 3:
                die_text = "You Lost!"

            if die_text != "":
                self.fail_health = 0
                die_text = ""
                self.game.stat.append(self.game.player_score) 
                self.run_display = False
                self.game.curr_menu = self.game.tempo
                self.blit_screen()
                # print(self.game.stat)
            
            # cv2.imshow('OUTPUT', img)
            # cv2.waitKey(1)

            self.player_movement(self.player, least_pos)
            self.draw_window(self.player, self.stonez, self.game.player_score, self.fail_health)
    
    def draw_window(self, player, stonez, player_score, fail_health):
            self.game.window.fill((100, 100, 100))
            player_health_text = self.HEALTH_FONT.render("Score: " + str(player_score), 1,
                                                         (255, 255, 255))
            self.game.window.blit(player_health_text, (10, 10))
            fail_health_text = self.HEALTH_FONT.render("Fails: " + str(fail_health), 1,
                                                         (255, 255, 255))
            self.game.window.blit(fail_health_text, (10, 50))
            self.game.window.blit((self.spaceship), (player.x, player.y))
            self.game.window.blit((self.obstacle), (stonez.x, stonez.y))
            pygame.display.update()

    def player_movement(self, player, least_pos):
        player.x = least_pos

    def positioning(self):
        X = choice(self.x_positions)
        return X

class fungameloop(SeriousGameloops):
    def __init__(self, game_class):
        self.game = game_class
        SeriousGameloops.__init__(self, game_class)
        
    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

    def display_menu(self):
        self.run_display = True
        while self.run_display: 
            success, img = self.cap.read()
            img = cv2.resize(img, (self.game.DISPLAY_W, self.game.DISPLAY_H),
                                     interpolation = cv2.INTER_AREA)

            img = self.detector.find_hands(img, False)
            lm_list = self.detector.find_position(img, draw=True,
                                                     index = self.fingers.get(self.game.knowing))
            # lm_list = self.detect.find_position(img)
            inversed_pos = np.interp(lm_list, (0, self.game.DISPLAY_W), (self.game.DISPLAY_W, 0))
            # least_pos = np.interp(inversed_pos, (self.quarter_width, self.right_quarter),
            #                          (0, self.game.DISPLAY_W))
            
            self.clock.tick(self.fps)       
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.run_display = False
                    self.game.running = False
            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run_display = False
                        self.fail_health = 0
                        die_text = ""
                        self.game.curr_menu = self.game.main_menu
                        self.game.log_out()
                        self.blit_screen()
            
            if self.stonez.y < self.player.y - 30:
                if self.played >= 10 and self.played <= 20:
                    self.obstacle_vel = 13
                elif self.played >= 21 and self.played <=30:
                    self.obstacle_vel = 14
                elif self.played > 30:
                    self.obstacle_vel = 18

                self.stonez.y += self.obstacle_vel
                if self.player.colliderect(self.stonez):
                    self.game.player_score += 2
                    self.HIT_SOUND.play()
                    self.played += 1

                elif self.stonez.y == self.player.y -30 and not self.player.colliderect(self.stonez): 
                    self.game.player_score -= 1
                    self.fail_health += 1
                
            else:
                self.stonez.y = 50
                self.stonez.x = self.positioning()    
            
            die_text = ""
            if self.fail_health == 3:
                die_text = "You Lost!"

            # if die_text != "":
            #     self.fail_health = 0
            #     die_text = ""
            #     self.game.stat.append(self.game.player_score) 
            #     self.run_display = False
            #     # self.game.curr_menu = self.game.tempo
            #     self.blit_screen()
            
            # cv2.imshow('OUTPUT', img)
            # cv2.waitKey(1)

            self.player_movement(self.player, inversed_pos)
            self.draw_window(self.player, self.stonez, self.game.player_score, self.fail_health)
    
    def draw_window(self, player, stonez, player_score, fail_health):
            self.game.window.fill((100, 100, 100))
            player_health_text = self.HEALTH_FONT.render("Score: " + str(player_score), 1,
                                                         (255, 255, 255))
            self.game.window.blit(player_health_text, (10, 10))
            fail_health_text = self.HEALTH_FONT.render("Fails: " + str(fail_health), 1,
                                                         (255, 255, 255))
            self.game.window.blit(fail_health_text, (10, 50))
            self.game.window.blit((self.spaceship), (player.x, player.y))
            self.game.window.blit((self.obstacle), (stonez.x, stonez.y))
            pygame.display.update()

    def player_movement(self, player, least_pos):
        player.x = least_pos

    def positioning(self):
        X = choice(self.x_positions)
        return X

class CheckingParalysisGameLoop(SeriousGameloops):
    def __init__(self, game_class):
        self.game = game_class
        SeriousGameloops.__init__(self, game_class)
        self.critical_point = 0
        self.fails = 0
        self.plays =0

    def display_menu(self):
        self.run_display = True
        while self.run_display: 
            success, img = self.cap.read()
            img = cv2.resize(img, (self.game.DISPLAY_W, self.game.DISPLAY_H),
                                     interpolation=cv2.INTER_AREA)

            img = self.detector.find_hands(img, False)
            lm_list = self.detector.find_position(img, draw=False,
                                                     index = self.fingers.get(self.game.knowing))
            inversed_pos = np.interp(lm_list, (0, self.game.DISPLAY_W), (self.game.DISPLAY_W, 0))
            # least_pos = np.interp(inversed_pos, (self.quarter_width, self.right_quarter),
                                    #  (0, self.game.DISPLAY_W))
            
            self.clock.tick(self.fps)       
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.game.stat.append(self.game.player_score)
                    self.run_display = False
            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run_display = False
                        self.fail_health = 0
                        die_text = ""
                        self.game.log_out()
                        self.game.curr_menu = self.game.main_menu
                        self.blit_screen()
            
            if self.stonez.y < self.player.y - 30:
                self.stonez.y += self.obstacle_vel
                if self.player.colliderect(self.stonez):
                    self.game.player_score += 2
                    self.critical_point += 1
                    self.plays += 1
                    self.HIT_SOUND.play()

                elif self.stonez.y == self.player.y -30 and not self.player.colliderect(self.stonez): 
                    self.game.player_score -= 1
                    self.plays += 1
                    self.fails += 1
                
            else:
                self.stonez.y = 50
                self.stonez.x = self.positioning()    
            
            die_text = ""
            if self.plays == 10:
                die_text = "You Lost!"

            if die_text != "":
                self.fail_health = 0
                die_text = ""
                self.run_display = False
                if self.critical_point <= 3:
                    self.game.curr_menu = self.game.critical
                    self.game.stat.append(self.game.player_score)
                    self.game.player_score = 0
                    try:
                        # Updating the existing database
                        scores = self.read_database.read_db()[self.game.typed].get('score')[:]
                        scores.append(sum(self.game.stat)//len(self.game.stat)+1)
                        self.read_database.update_db({self.game.typed:{'score':scores, 'age':self.read_database.read_db()[self.game.typed].get('age')}})
                        self.game.stat.clear()
                    except:
                        pass
                    self.game.stat.clear()
                    self.game.player_score = 0
                    # self.game.log_out()
                else:
                    self.game.curr_menu = self.game.well
                    self.game.stat.clear()
                    self.game.player_score = 0
                    # self.game.log_out()
                
            
            # cv2.imshow('OUTPUT', img)
            # cv2.waitKey(1)

            self.player_movement(self.player, inversed_pos)
            self.draw_window_critical(self.player, self.stonez, self.critical_point, self.fails)

    def draw_window_critical(self, player, stonez, critical_point, fails):
            self.game.window.fill((0, 100, 100))
            critical_health_text = self.HEALTH_FONT.render("Critical points: " + str(critical_point), 1,
                                                         (255, 255, 255))
            self.game.window.blit(critical_health_text, (10, 10))
            fail_text = self.HEALTH_FONT.render("Fails: " + str(fails), 1,
                                                         (255, 255, 255))
            self.game.window.blit(fail_text, (10, 50))
            self.game.window.blit((self.spaceship), (player.x, player.y))
            self.game.window.blit((self.obstacle), (stonez.x, stonez.y))
            pygame.display.update()

class Tempo(SeriousGameloops):
    def display_menu(self):
        self.run_display = True 
        while self.run_display:
            self.game.display.fill(self.game.BLACK) 
            if len(self.game.stat) == 1:
                self.game.scores.append(self.game.player_score)
                self.game.draw_text(f'Your score is {self.game.scores[0]}', 20,
                                    self.game.DISPLAY_W/2, self.game.DISPLAY_H/2)
                self.game.draw_text("You got few data for us to plot the graph play again", 15,
                                    self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 + 30)
                self.blit_screen()
                self.run_display = False
                time.sleep(2)
                counting = 0
                while counting < 1:
                    for a in [5, 4, 3, 2, 1]:
                        self.game.display.fill(self.game.BLACK)
                        self.game.draw_text('Proceed in, '+ str(a), 30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
                        self.game.draw_text('(You can press "ESC" to quit training)', 10, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2)
                        self.blit_screen()
                        time.sleep(1)
                    counting += 1

                self.game.player_score = 0
                if self.game.knowing in self.fingers:
                    self.game.curr_menu = self.game.seriousgameloop
                else:
                    self.game.curr_menu = self.game.main_menu
                    self.game.log_out()

            else:
                self.game.scores[0] = self.game.player_score
                # self.game.draw_text(f'Your score is {self.game.scores[0]}', 20,
                                    # self.game.DISPLAY_W/2, self.game.DISPLAY_H/2)
                plt.plot(self.game.stat)
                plt.xlim(0, len(self.game.stat))  # len(self.read_database.read_db()[self.game.typed].get('score')))
                plt.ylabel("Your scores.")
                plt.xlabel("Number of plays")
                plt.show()
                self.blit_screen()
                counting = 0
                saying = 'no'
                while counting < 1:
                    for a in [5, 4, 3, 2, 1]:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    saying = 'yes'
                        if saying == 'yes':
                            break
                        else:
                            self.game.display.fill(self.game.BLACK)
                            self.game.draw_text('Proceed in, '+ str(a), 30, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
                            self.game.draw_text('(You can press "ESC" to quit training)', 10, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2)
                            self.blit_screen()
                            time.sleep(1)
                    
                    if saying == 'yes':
                        self.run_display = False
                        self.fail_health = 0
                        counting += 1
                        self.game.stat.append(self.game.player_score)
                        try:
                            # Updating the existing database
                            scores = self.read_database.read_db()[self.game.typed].get('score')[:]
                            scores.append(sum(self.game.stat)//len(self.game.stat)+1)
                            self.read_database.update_db({self.game.typed:{'score':scores, 'age':self.read_database.read_db()[self.game.typed].get('age')}})
                        except:
                            pass
                        self.game.curr_menu = self.game.main_menu
                        self.game.log_out()
                        self.blit_screen()
                    
                    else:
                        counting += 1
                        self.run_display = False
                        self.game.curr_menu = self.game.seriousgameloop
                        self.game.player_score = 0
