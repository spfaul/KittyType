import curses
import time

from components.input_box import InputBox, InputBoxExits
from components.text_display import TextDisplay
from components.end_screen import EndScreen

class MainWindowHandler:

    INPUT_MARGIN_W, INPUT_MARGIN_H = 2, 1
    TEXTS_MARGIN_W, TEXTS_MARGIN_H = 2, 2
    ENDSCR_MARGIN_W, ENDSCR_MARGIN_H = 2, 2
    

    def __init__(self, logs, stdscr):
        """ Handle and display components on main window """
        
        self.stdscr = stdscr
        self.logs = logs
        max_y, max_x = self.stdscr.getmaxyx()

        self.input_container = stdscr.derwin(3, max_x-self.INPUT_MARGIN_W*2, self.INPUT_MARGIN_H, self.INPUT_MARGIN_W)
        self.input_box = InputBox(logs, self.input_container)

        self.text_container = stdscr.derwin(max_y-3-self.TEXTS_MARGIN_H*2, max_x-self.TEXTS_MARGIN_W*2, self.TEXTS_MARGIN_H+3+self.INPUT_MARGIN_H, self.TEXTS_MARGIN_W)
        self.text_display = TextDisplay(logs, self.text_container)

        self.end_screen_container = stdscr.derwin(max_y-self.ENDSCR_MARGIN_H*2, max_x-self.ENDSCR_MARGIN_W*2, self.ENDSCR_MARGIN_H, self.ENDSCR_MARGIN_W)
        self.end_screen = EndScreen(logs, self.end_screen_container)
        
    def run(self):
        self.stdscr.erase()
        _, stats = self.input_box.run(self.on_key_enter)

        curses.curs_set(0)

        self.stdscr.erase()
        self.end_screen.run(stats)
        

    def on_key_enter(self, ch):        
        is_sucess = self.text_display.try_ch(ch)
        
        if ch == curses.ascii.SP and is_sucess: #space
            if self.input_box.dist_to_last_correct == 0:
                self.input_box.wpm['words'] += 1
                self.text_display.move_forward(1)
                self.input_box.win.erase()
                return 0
            else:
                self.input_box.dist_to_last_correct += 1
            
        elif ch == curses.KEY_BACKSPACE:
            if self.input_box.dist_to_last_correct > 0:
                self.input_box.dist_to_last_correct -= 1
                return ch
                
            elif len(self.input_box.tb.gather()) != 0:
                self.text_display.move_backward(1)
            
        elif is_sucess:
            self.input_box.accuracy['total'] += 1

            if self.text_display.is_last_char():
                self.logs.log('\nFinished Typing\n')
                self.text_display.move_forward(1)
                self.input_box.tb._insert_printable_char(ch)
                self.input_box.exit = InputBoxExits.FINISH_TYPING
                return curses.ascii.BEL
                
            elif self.input_box.dist_to_last_correct > 0:
                self.input_box.dist_to_last_correct += 1

            else:
                self.text_display.move_forward(1)
                self.input_box.accuracy['correct'] += 1

            
        elif not is_sucess and curses.ascii.isascii(ch):
            self.input_box.accuracy['total'] += 1
            self.input_box.dist_to_last_correct += 1


        if curses.ascii.isascii(ch) and self.input_box.start_time == None:
            self.input_box.start_time = time.time()        
        
        return ch

