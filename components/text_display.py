import curses
import textwrap
import json
import random
import os
from palettes.colors import Colors

class TextDisplay:
    def __init__(self, logs, win: "win"):
        """Initalize a text display"""
        self.logs = logs
        self.win = win
        self.win.box()

        self.text = self.fetch_texts()
        self.curr_pos = -1
        self.draw()

    def draw(self):
        max_y, max_x = self.win.getmaxyx()
        self.win.box()

        texts = textwrap.wrap(self.text, width=max_x-2, drop_whitespace=False)
        
        if self.curr_pos < 0:
            for height, t in enumerate(texts):
                self.win.addstr(1+height, 1, t,  curses.color_pair(2))
        else:
            ptr = 0
            color = 3 # everything is typed until curr_pos
            for height, t in enumerate(texts):                            
                if ptr+len(t) > self.curr_pos and color == 3: # this is the line with curr_pos
                    color = 2 # probably should change to some sort of enum palette system, but that's for another day
                    last_typed_char = self.curr_pos-ptr + 1
                    typed_seg, untyped_seg = t[:last_typed_char], t[last_typed_char:]
                    self.win.addstr(1+height, 1, typed_seg, curses.color_pair(Colors.TYPED))
                    self.win.addstr(1+height, 1+last_typed_char, untyped_seg, curses.color_pair(Colors.UNTYPED))
                else:
                    self.win.addstr(1+height, 1, t, curses.color_pair(color))
                    
                ptr += len(t)
            
        self.win.refresh()
    
    def try_ch(self, ch):
        self.logs.log(f'trying char { (ch, chr(ch)) }\n')
        if self.curr_pos+1 == len(self.text):
            return False
        
        if ch == ord(self.text[self.curr_pos+1]):
            return True
        else:
            return False

    def is_last_char(self):
        if self.curr_pos+2 == len(self.text):
            return True
        return False

    def move_forward(self, amnt):
        self.curr_pos += amnt
        self.draw()

    def move_backward(self, amnt):
        self.curr_pos -= amnt        
        self.draw()

    def fetch_texts(self):
        with open(os.path.join(os.path.dirname(__file__), '../samples/quotes.json'), 'r') as file:
            data = json.load(file)

        return random.choice(data)['content']
        