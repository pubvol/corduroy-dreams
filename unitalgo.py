# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 11:30:42 2020

@author: LocalAdmin
"""
import numpy as np
import tkinter as Tk
from PIL import Image, ImageTk, ImageDraw
import random
import matplotlib.pyplot as plt

#colorcodes

empty_rgb = [255,255,255]
warrior_rgb = [38, 117, 35] #grün
bowman_rgb = [26, 156, 128] #blau
knight_rgb = [145, 156, 26] #gelb
ai_warrior_rgb = [163, 35, 21] #rot
ai_bowman_rgb = [94, 11, 120] #lila
ai_knight_rgb = [219, 37, 150] #pink
colorcodes = [(255,255,255),(38, 117, 35),(26, 156, 128),(145, 156, 26),(163, 35, 21),(94, 11, 120),(219, 37, 150)]
coloradress = [empty_rgb, warrior_rgb, ai_warrior_rgb, (0,0,0), (0,0,0), bowman_rgb, ai_bowman_rgb, (0,0,0), (0,0,0), knight_rgb, ai_knight_rgb, (0,0,0), (0,0,0)]
coloradress_with_sleepy = [empty_rgb, warrior_rgb, ai_warrior_rgb, warrior_rgb, ai_warrior_rgb, bowman_rgb, ai_bowman_rgb, bowman_rgb, ai_bowman_rgb, knight_rgb, ai_knight_rgb, knight_rgb, ai_knight_rgb]

npcoloradress = np.array(coloradress)

#sleepy einheiten fixen


#player units are odd numbers, ai are even

warrior = 1
sleepy_warrior = 3
bowman = 5
sleepy_bowman = 7
knight = 9
sleepy_knight = 11



ai_warrior = 2
sleepy_ai_warrior = 4
ai_bowman = 6
sleepy_ai_bowman = 8
ai_knight = 10
sleepy_ai_knight = 12



empty = 0


unit_array = np.array([[knight,empty,empty,ai_bowman],[bowman,warrior,empty,ai_warrior],[empty,warrior,empty,empty]]).tolist()


#CONVERT RGB TO INT AND BACK

def convert_rgb(unit_array):
    for x in range(len(unit_array)):
        for y in range(len(unit_array[x])):
                unit_array[x][y] = coloradress.index(unit_array[x][y])
    unit_array = np.array(unit_array)
    return unit_array

# def convert_int(unit_array):
#     unit_array = np.array(unit_array,dtype='int') 
#     npcoloradress = np.array(coloradress)
#     unit_array = npcoloradress[unit_array]
#     return unit_array        
def convert_int(unit_array):
    for x in range(len(unit_array)):
        for y in range(len(unit_array[x])):  
            unit_array[x][y] = coloradress_with_sleepy[unit_array[x][y]]
    return unit_array

#MAKE MOVE FUNCTIONS

def make_move(unit_array):
    for x in range(len(unit_array)):
        for y in range(len(unit_array[x])):
            if np.all(unit_array[x][y] == warrior):
                melee(x,y,unit_array)
            elif np.all(unit_array[x][y] == sleepy_warrior):
                unit_array[x][y] = warrior
            elif np.all(unit_array[x][y] == bowman):
                ranged(x,y,unit_array)
            elif np.all(unit_array[x][y] == sleepy_bowman):
                unit_array[x][y] = bowman
            elif np.all(unit_array[x][y] == knight):
                cavalry(x,y,unit_array)
            elif np.all(unit_array[x][y] == sleepy_knight):
                unit_array[x][y] = knight
    print("turn finished")
    return unit_array
           
def ai_make_move(unit_array):
    for x in range(len(unit_array)):
        for y in range(len(unit_array[x])):
            if np.all(unit_array[x][y] == ai_warrior):
                ai_melee(x,y,unit_array)
            elif np.all(unit_array[x][y] == sleepy_ai_warrior):
                unit_array[x][y] = ai_warrior
            elif np.all(unit_array[x][y] == ai_bowman):
                ai_ranged(x,y,unit_array)
            elif np.all(unit_array[x][y] == sleepy_ai_bowman):
                unit_array[x][y] = ai_bowman
            elif np.all(unit_array[x][y] == ai_knight):
                ai_cavalry(x,y,unit_array)
            elif np.all(unit_array[x][y] == sleepy_ai_knight):
                unit_array[x][y] = ai_knight
    print("turn finished ai")
    return unit_array
    
#PLAYER MOVE FUNCTIONS  

def melee(x,y,unit_array):
    if y+1 >= len(unit_array[x]):   #am ende angekommen
        return unit_array
    else:
        c = np.zeros(len(unit_array),dtype=int)
        for dx in [-1,0,1]: 
            if y+1 >= len(unit_array[x]) or x+dx >= len(unit_array) or x+dx < 0:
                continue  
            elif unit_array[x+dx][y+1] % 2 == 0 and unit_array[x+dx][y+1] != 0:
                c[x+dx] = 1
        if sum(c) == 0:     #wenn keiner vor ihm steht -> ein feld weiter gehen
            if np.equal(unit_array[x][y+1], empty):
                unit_array[x][y] = empty
                unit_array[x][y+1] = sleepy_warrior
        else:               #ansonsten einen random gegner vor ihm angreifen
            print("yeet")
            attack_choice = np.where(c==1)[0]
            unit_array[random.choice(attack_choice)][y+1] = empty
            
    return unit_array


def ranged(x,y,unit_array):
    if y+1 >= len(unit_array[x]):   #am ende angekommen
        return unit_array
    else:
        c = np.zeros(len(unit_array),dtype=int)
        for dx in [-1,0,1]:
            if y+2 >= len(unit_array[x]) or x+dx >= len(unit_array) or x+dx < 0:
                continue
            elif unit_array[x+dx][y+2] % 2 == 0 and unit_array[x+dx][y+2] != 0:
                c[x+dx] = 1
        if sum(c) == 0:     #wenn keiner vor ihm steht -> ein feld weiter gehen
            if np.equal(unit_array[x][y+1], empty):
                unit_array[x][y] = empty
                unit_array[x][y+1] = sleepy_bowman
        else:               #ansonsten einen random gegner vor ihm angreifen
            print("yeet pfeil")
            attack_choice = np.where(c==1)[0]
            unit_array[random.choice(attack_choice)][y+2] = empty
            
    return unit_array

def cavalry(x,y,unit_array):
    if y+1 >= len(unit_array[x]):   #am ende angekommen
        return unit_array
    else:
        c = np.zeros(len(unit_array),dtype=int)
        for dx in [-1,0,1]:
            if y+1 >= len(unit_array[x]) or x+dx >= len(unit_array) or x+dx < 0:
                continue
            elif unit_array[x+dx][y+1] % 2 == 0 and unit_array[x+dx][y+1] != 0:
                c[x+dx] = 1
        if sum(c) == 0:     #wenn keiner vor ihm steht -> ein feld weiter gehen
            if y+2 < len(unit_array[x]) and np.equal(unit_array[x][y+2], empty):
                unit_array[x][y] = empty
                unit_array[x][y+2] = sleepy_knight
        else:               #ansonsten einen random gegner vor ihm angreifen
            print("yeet ferd")
            attack_choice = np.where(c==1)[0]
            unit_array[random.choice(attack_choice)][y+1] = empty
            
    return unit_array

#AI MOVE FUNCTIONS

def ai_melee(x,y,unit_array):
    if y-1 <= 0:   #am ende angekommen
        return unit_array
    else:
        c = np.zeros(len(unit_array),dtype=int)
        for dx in [-1,0,1]: 
            if y-1 < 0 or x+dx >= len(unit_array) or x+dx < 0:
                continue
            elif unit_array[x+dx][y-1] % 2 != 0:
                c[x+dx] = 1
        if sum(c) == 0:     #wenn keiner vor ihm steht -> ein feld weiter gehen
            if np.equal(unit_array[x][y-1], empty):
                unit_array[x][y] = empty
                unit_array[x][y-1] = sleepy_ai_warrior
        else:               #ansonsten einen random gegner vor ihm angreifen
            print("yeet ai")
            attack_choice = np.where(c==1)[0]
            unit_array[random.choice(attack_choice)][y-1] = empty
            
    return unit_array


def ai_ranged(x,y,unit_array):
    if y-1 <= 0:   #am ende angekommen
        return unit_array
    else:
        c = np.zeros(len(unit_array),dtype=int)
        for dx in [-1,0,1]:          
            if y-2 < 0 or x+dx >= len(unit_array) or x+dx < 0:
                continue
            elif unit_array[x+dx][y-2] % 2 != 0:
                c[x+dx] = 1
        if sum(c) == 0:     #wenn keiner vor ihm steht -> ein feld weiter gehen
            if np.equal(unit_array[x][y-1], empty):
                unit_array[x][y] = empty
                unit_array[x][y-1] = sleepy_ai_bowman
        else:               #ansonsten einen random gegner vor ihm angreifen
            print("yeet pfeil ai")
            attack_choice = np.where(c==1)[0]
            unit_array[random.choice(attack_choice)][y-2] = empty
            
    return unit_array

def ai_cavalry(x,y,unit_array):
    if y-1 <= 0:   #am ende angekommen
        return unit_array
    else:
        c = np.zeros(len(unit_array),dtype=int)
        for dx in [-1,0,1]: 
            if y-1 < 0 or x+dx >= len(unit_array) or x+dx < 0:
                continue
            elif unit_array[x+dx][y-1] % 2 != 0:
                c[x+dx] = 1
        if sum(c) == 0:     #wenn keiner vor ihm steht -> ein feld weiter gehen
            if y-2 < len(unit_array[x]) and np.equal(unit_array[x][y-2], empty):
                unit_array[x][y] = empty
                unit_array[x][y-2] = sleepy_ai_knight
        else:               #ansonsten einen random gegner vor ihm angreifen
            print("yeet ferd ai")
            attack_choice = np.where(c==1)[0]
            unit_array[random.choice(attack_choice)][y-1] = empty
            
    return unit_array

#AI 
    
def find_counter(unit_array):
    unit_value = np.array([0,1,1,1,1,2,2,2,2,3,3,3,3])
    army_value = unit_value[unit_array]
    army_value = sum(sum(army_value))
    units = np.array([0,2,6,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    value = 0
    episodes = 1
    print(army_value)
    for x in range(episodes): 
        print(f"episode {x}")
        while value <= army_value:
            for y in range(50,100):
                for x in range(len(unit_array)):
                    unit_array[x][y] = random.choice(units)
                    value = value + unit_value[unit_array[x][y]]
                    print(value)
                    print(value<=army_value)
                    if value > army_value:
                        break
                if value > army_value:
                    break
    return unit_array
        
                    





#find_counter(test_array)


test = [[(255,255,255),(38, 117, 35),(26, 156, 128)],[(145, 156, 26),(163, 35, 21),(94, 11, 120)],[(219, 37, 150),(219, 37, 150),(219, 37, 150)]]
# make_move(unit_array)
# ai_make_move(unit_array)
# make_move(unit_array)
# ai_make_move(unit_array)
#ai_make_move(unit_array)
# convert_rgb(test)
# print(test)
# convert_int(test)
# print(test)
