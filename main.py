import curses
import os

from palettes.palette import Palette
from components.main_window import MainWindowHandler

from helpers.logger import Logger

def main(stdscr):
    # disable cursor blinking
    curses.curs_set(1)
    # Apply colors from palette
    Palette()

    #initalize logger
    logs = Logger(os.path.join(os.path.dirname(__file__), 'run_log.txt'))
    logs.log("Init ran fine\n")

    # initialize main window
    main_win = MainWindowHandler(logs, stdscr)
    main_win.run()

    key = stdscr.getch()




if __name__ == '__main__':
    curses.wrapper(main)
