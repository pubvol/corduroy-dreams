#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as Tk
from PIL import Image, ImageTk, ImageDraw
import numpy as np
import unitalgo

#color codes:
empty = (255,255,255)
warrior = (38, 117, 35) #grün
bowman = (26, 156, 128) #blau
knight = (145, 156, 26) #gelb
ai_warrior = (163, 35, 21) #rot
ai_bowman = (94, 11, 120) #lila
ai_knight = (219, 37, 150) #pink
colorcodes = [(255,255,255),(38, 117, 35),(26, 156, 128),(145, 156, 26),(163, 35, 21),(94, 11, 120),(219, 37, 150)]


class NimGui(object):
    def __init__(self, root):
        self.root = root
        self.root.title("War Simulator (Jetzt mit mittelmäßiger KI!)")
        self.image_size = 100, 50
        self.root.minsize(width=500, height=300)
        self.animation_started = False
        self.animation_speed = 100
        self.rules = Tk.IntVar()
        self.rules.set(0)
        self.unit_color = Tk.IntVar()
        self.unit_color.set(0)
        self.menubar()
        self.life_image = Image.new("RGB", (self.image_size[0], self.image_size[1]), "white")
        self.resized_image = None
        self.draw = ImageDraw.Draw(self.life_image)
        self.life_photoimage = ImageTk.PhotoImage(self.life_image)
        self.life_image_label = Tk.Label(root, image=self.life_photoimage, borderwidth=0, cursor="cross")
        self.life_image_label.bind("<B1-Motion>", self.mouse_move)
        self.life_image_label.bind("<ButtonPress-1>", self.mouse_down)
        self.life_image_label.bind("<ButtonRelease-1>", self.mouse_up)          #add restliche buttons (mit zugeh. fkts)
        self.life_image_label.bind("<Configure>", lambda e: self.show_image())
        self.life_image_label.pack(side="top", fill="both", expand=True)
        self.mouse_x, self.mouse_y = 0, 0
        self.pen_color = empty
        self.player_turn = 1

    @property
    def screen_size(self):
        return self.life_image_label.winfo_width(), self.life_image_label.winfo_height()

    def mouse_position(self, event):
        current_screen_size = self.screen_size
        return (event.x * self.image_size[0] / current_screen_size[0],
                event.y * self.image_size[1] / current_screen_size[1])

    def mouse_down(self, event):
        self.mouse_x, self.mouse_y = self.mouse_position(event)
        if self.life_image.getpixel((self.mouse_x, self.mouse_y)) == empty:
            self.pen_color = colorcodes[self.unit_color.get()]
        else:
            self.pen_color = empty
        self.draw.line((self.mouse_x, self.mouse_y, self.mouse_x, self.mouse_y), fill=self.pen_color)
        self.show_image()

    def mouse_up(self, event):
        self.mouse_x, self.mouse_y = -1, -1

    def mouse_move(self, event):
        current_mouse_position = self.mouse_position(event)
        if current_mouse_position != (self.mouse_x, self.mouse_y):
            self.draw.line((self.mouse_x, self.mouse_y, current_mouse_position[0], current_mouse_position[1]),
                           fill=self.pen_color)
            self.mouse_x, self.mouse_y = current_mouse_position
            self.show_image()

    def show_image(self):
        self.resized_image = self.life_image.resize(self.screen_size, Image.NEAREST)
        self.life_photoimage = ImageTk.PhotoImage(self.resized_image)
        self.life_image_label.config(image=self.life_photoimage)

    def start(self):
        if not self.animation_started:
            self.root.after(self.animation_speed, self.animate)
        self.animation_started = True

    def stop(self):
        self.animation_started = False

    def step(self):
        self.animation_started = False
        self.update_image()

    def update_image(self):     
        units_as_list = np.array(self.life_image).tolist()
        unitalgo.convert_rgb(units_as_list)
        if self.rules.get() == 1:           #rules brauchts eig nicht
            if self.player_turn == 1:
                updated_units = unitalgo.make_move(units_as_list)
                self.player_turn = 0
            else:
                updated_units = unitalgo.ai_make_move(units_as_list)
                self.player_turn = 1
        else:
            if self.player_turn == 1:
                updated_units = unitalgo.make_move(units_as_list)
                self.player_turn = 0
            else:
                updated_units = unitalgo.ai_make_move(units_as_list)
                self.player_turn = 1
        unitalgo.convert_int(updated_units)
        numpy_image = np.array(updated_units).astype('uint8')
        self.life_image = Image.fromarray(numpy_image)
        self.draw = ImageDraw.Draw(self.life_image)
        self.show_image()

    def animate(self):
        if self.animation_started:
            self.update_image()
            self.root.after(self.animation_speed, self.animate)
            
    def calculate_ai(self):
        units_as_list = np.array(self.life_image).tolist()
        unitalgo.convert_rgb(units_as_list)
        updated_units = unitalgo.find_counter(units_as_list)
        unitalgo.convert_int(updated_units)
        numpy_image = np.array(updated_units).astype('uint8')
        self.life_image = Image.fromarray(numpy_image)
        self.draw = ImageDraw.Draw(self.life_image)
        self.show_image()

    def set_image_size(self, size):
        self.image_size = size
        self.life_image = Image.new("RGB", (self.image_size[0], self.image_size[1]), "white")
        self.draw = ImageDraw.Draw(self.life_image)
        self.show_image()

    def menubar(self):
        menu_main = Tk.Menu(self.root)
        menu_neu = Tk.Menu(menu_main, tearoff=0)
        menu_start = Tk.Menu(menu_main, tearoff=0)
        menu_options = Tk.Menu(menu_main, tearoff=0)
        menu_unit = Tk.Menu(menu_main, tearoff=0)
        menu_options.add_radiobutton(label="Nur auf linke Hälfte, KI simulieren lassen", value=0, variable=self.rules)
        menu_options.add_radiobutton(label="Selbst alle Einheiten setzen", value=1, variable=self.rules)
        menu_unit.add_radiobutton(label="Warrior", value=1, variable=self.unit_color)
        menu_unit.add_radiobutton(label="Bowman", value=2, variable=self.unit_color)
        menu_unit.add_radiobutton(label="Knight", value=3, variable=self.unit_color)
        menu_unit.add_radiobutton(label="AI_Warrior", value=4, variable=self.unit_color)
        menu_unit.add_radiobutton(label="AI_Bowman", value=5, variable=self.unit_color)
        menu_unit.add_radiobutton(label="AI_Knight", value=6, variable=self.unit_color)
        menu_neu.add_command(label="100x50", underline=0, command=lambda: self.set_image_size((100, 50)))
        menu_neu.add_command(label="150x100", underline=1, command=lambda: self.set_image_size((150, 100)))
        menu_neu.add_command(label="200x150", underline=1, command=lambda: self.set_image_size((200, 150)))
        menu_help = Tk.Menu(menu_main, tearoff=0)
        help_text = ("War Simulator - klick dich einfach durch oben")
        menu_help.add_command(label="Über", underline=0, command=lambda: Tk.messagebox.showinfo("Von Tim Felgenhauer für Python SoSe 2020", help_text))
        menu_main.add_cascade(label="Neu", underline=0, menu=menu_neu)
        menu_main.add_cascade(label="Start", underline=0, menu=menu_start)
        menu_start.add_command(label="Start", underline=0, command=self.start)
        menu_start.add_command(label="Stop", underline=1, command=self.stop)
        menu_start.add_command(label="1 Schritt", underline=1, command=self.step)
        menu_start.add_command(label="KI Aufstellung berechnen", underline=1, command=self.calculate_ai)
        menu_main.add_cascade(label="Optionen", underline=0, menu=menu_options)
        menu_main.add_cascade(label="Einheit", underline=0, menu=menu_unit)
        menu_main.add_cascade(label="Hilfe", underline=0, menu=menu_help)
        self.root.config(menu=menu_main)


r = Tk.Toplevel()
mainWindow = NimGui(r)
r.mainloop()
