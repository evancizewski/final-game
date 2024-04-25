#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 09:12:07 2024

@author: evancizewski
"""

import pygame
import random
import simpleGE


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0)
FROG_COLOR = (0, 255, 0)
CAR_COLOR = (255, 0, 0)
CAR_WIDTH = 50
CAR_HEIGHT = 30
CAR_SPEED = 7
CAR_GAP = 200


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Frogger")

clock = pygame.time.Clock()

class Frog:
    def __init__(self):
        self.width = 30
        self.height = 30
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height
        self.color = FROG_COLOR

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

        
        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
        if self.y < 0:
            self.y = 0
        elif self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height

class Car:
    def __init__(self, x, y):
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.x = x
        self.y = y
        self.color = CAR_COLOR
        self.speed = CAR_SPEED

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        self.x += self.speed
        if self.x > SCREEN_WIDTH:
            self.x = -self.width


frog = Frog()


cars = []
for i in range(3):
    car = Car(random.randint(0, SCREEN_WIDTH - CAR_WIDTH), 50 + i * CAR_GAP)
    cars.append(car)

running = True
while running:
    screen.fill(BACKGROUND_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        frog.move(-5, 0)
    if keys[pygame.K_RIGHT]:
        frog.move(5, 0)
    if keys[pygame.K_UP]:
        frog.move(0, -5)
    if keys[pygame.K_DOWN]:
        frog.move(0, 5)

   
    for car in cars:
        car.move()
        car.draw()

  
    frog.draw()

   
    for car in cars:
        if (frog.x < car.x + car.width and
            frog.x + frog.width > car.x and
            frog.y < car.y + car.height and
            frog.y + frog.height > car.y):
            frog.x = SCREEN_WIDTH // 2 - frog.width // 2
            frog.y = SCREEN_HEIGHT - frog.height

    pygame.display.flip()
    clock.tick(60)
    

    
class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time Left: 10"
        self.center = (500, 30)
        self.lblTime = LblTime()
        
        self.sprites = [self.frog,
                        self.lblScore, 
                        self.lblTime]
        
    def process(self):
        for coin in self.coins:
            if self.charlie.collidesWith(coin):
                self.sndCoin.play()
                coin.reset()
                self.score += 1
                self.lblScore.text = f"Score: {self.score}"
                
        self.lblTime.text = f"Time Left: {self.timer.getTimeLeft():.2f}"
        if self.timer.getTimeLeft() < 0:
            print(f"Final Score: {self.score}")
            self.stop()

class Instructions(simpleGE.Scene):
    def __init__(self, score):
        super().__init__()
        self.setImage("background.png")
        
        self.response = "Play"
        
        self.instructions = simpleGE.MultiLabel()
        self.instructions.textLines = [
        "CTy to cross without getting hit by the red blocks",
        "",
        "Good Luck!"]
        
        self.instructions.center = (320, 240)
        self.instructions.size = (500, 250)
        
        self.prevScore = score
        self.lblScore = simpleGE.Label()
        self.lblScore.text = f"Last score: {self.prevScore}"
        self.lblScore.center = (320, 400)
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play (up)"
        self.btnPlay.center = (100, 400)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit (down)"
        self.btnQuit.center = (550, 400)
        
        self.sprites = [self.instructions,
                        self.lblScore,
                        self.btnQuit,
                        self.btnPlay]
        
    def process(self):
        #buttons
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()
        if self.btnPlay.clicked:
            self.response = "Play"
            self.stop()

        #arrow keys
        if self.isKeyPressed(pygame.K_UP):
            self.response = "Play"
            self.stop()
        if self.isKeyPressed(pygame.K_DOWN):
            self.response = "Quit"
            self.stop()

def main():
    
    keepGoing = True
    score = 0
    while keepGoing:
        
        instructions = Instructions(score)
        instructions.start()
                
        if instructions.response == "Play":    
            game.start()
            score = game.score
        else:
            keepGoing = False

pygame.quit()