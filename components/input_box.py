import curses
import curses.textpad
import curses.ascii

from enum import Enum, auto
import time
import math
from palettes.colors import Colors


class InputBoxExits(Enum):
    DEFAULT = auto()
    KB_INTERRUPT = auto()
    FINISH_TYPING = auto()


class InputBox:
    def __init__(self, logs, win: "window"):
        self.container = win
        self.draw_box(self.container)
        self.container.refresh()
        my, mx = win.getmaxyx()

        self.logs = logs
        self.win = self.container.derwin(my-2,mx-2,1,1)

        self.exit_code = InputBoxExits.DEFAULT
        self.tb = curses.textpad.Textbox(self.win, True)
        self.dist_to_last_correct = 0
        self.start_time = None

        # stats
        self.accuracy = {'total': 0,'correct': 0}
        self.wpm = {'val': 0, 'words': 0}
        

    def run(self, validate):
        self.exit_code = InputBoxExits.DEFAULT

        self.edit(self.tb, validate=validate)
        
        time_taken = time.time()-self.start_time
        self.wpm['val'] = int(self.wpm['words'] * math.ceil(60 / time_taken))
        
        stats = {
            'acc': self.accuracy,
            'wpm': self.wpm
        }

        return self.exit_code, stats

    def draw_box(self, win):
        win.attron(curses.color_pair(Colors.INPUT_BORDER))
        win.box()
        win.attroff(curses.color_pair(Colors.INPUT_BORDER))

    def edit(self, tb, validate):
        while 1:
            try:
                ch = tb.win.getch()
            except KeyboardInterrupt:
                tb.win.getch() # clears -1 from getch queue
                self.exit = InputBoxExits.KB_INTERRUPT
                break
            
            if validate:
                ch = validate(ch)
            if not ch:
                continue
            if not self.do_command(tb, ch):
                break

            tb.win.refresh()

        return tb.gather()


    def do_command(self, tb, ch):
        "Process a single editing command."
        tb._update_max_yx()
        (y, x) = tb.win.getyx()
        tb.lastcmd = ch
        if curses.ascii.isprint(ch):
            if y < tb.maxy or x < tb.maxx:
                tb._insert_printable_char(ch)
        elif ch == curses.ascii.SOH:                           # ^a
            tb.win.move(y, 0)
        elif ch in (curses.ascii.STX, curses.ascii.BS,curses.KEY_BACKSPACE):
            if x > 0:
                tb.win.move(y, x-1)
            elif y == 0:
                pass
            elif tb.stripspaces:
                tb.win.move(y-1, tb._end_of_line(y-1))
            else:
                tb.win.move(y-1, tb.maxx)
            if ch in (curses.ascii.BS, curses.KEY_BACKSPACE):
                tb.win.delch()
        elif ch == curses.ascii.EOT:                           # ^d
            tb.win.delch()
        elif ch == curses.ascii.ENQ:                           # ^e
            if tb.stripspaces:
                tb.win.move(y, tb._end_of_line(y))
            else:
                tb.win.move(y, tb.maxx)
        # elif ch in (curses.ascii.ACK, curses.KEY_RIGHT):       # ^f
            # if x < tb.maxx:
                # tb.win.move(y, x+1)
            # elif y == tb.maxy:
                # pass
            # else:
                # tb.win.move(y+1, 0)
        elif ch == curses.ascii.BEL:                           # ^g
            return 0
        elif ch == curses.ascii.NL:                            # ^j
            if tb.maxy != 0 and 0 < tb.maxy:
                tb.win.move(y+1, 0)
        elif ch == curses.ascii.VT:                            # ^k
            if x == 0 and tb._end_of_line(y) == 0:
                tb.win.deleteln()
            else:
                # first undo the effect of tb._end_of_line
                tb.win.move(y, x)
                tb.win.clrtoeol()
        elif ch == curses.ascii.FF:                            # ^l
            tb.win.refresh()
        elif ch in (curses.ascii.SO, curses.KEY_DOWN):         # ^n
            if y < tb.maxy:
                tb.win.move(y+1, x)
                if x > tb._end_of_line(y+1):
                    tb.win.move(y+1, tb._end_of_line(y+1))
        elif ch == curses.ascii.SI:                            # ^o
            tb.win.insertln()
        elif ch in (curses.ascii.DLE, curses.KEY_UP):          # ^p
            if y > 0:
                tb.win.move(y-1, x)
                if x > tb._end_of_line(y-1):
                    tb.win.move(y-1, tb._end_of_line(y-1))
        return 1


