import curses
import time
from bar import HBar, VBar


def main(stdscr):
    curses.curs_set(0)

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    max_y, max_x = stdscr.getmaxyx()
    # bar_container = stdscr.derwin(20, 4, (max_y//2)-10, (max_x//2)-2)
    bar_container = stdscr.derwin(4, 20, (max_y//2)-2, (max_x//2)-10)

    colors = [
        curses.color_pair(4),
        curses.color_pair(1),
        curses.color_pair(2),
        curses.color_pair(3),
    ]
    a = HBar(
            bar_container,
            total=10,
            value=0,
            text="hi there, friend!",
            text_align="center",
            colors=colors
            )
    a.draw()
# 
    # for i in range(1, 11):
        # a.change_value(i)
        # time.sleep(.1)
# 

    stdscr.getch()


curses.wrapper(main)
