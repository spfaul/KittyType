import curses


def main(stdscr):
    while 1:
        stdscr.box()
        key = stdscr.getch()

        if stdscr.getch() == curses.KEY_RESIZE:
            curses.resizeterm(*stdscr.getmaxyx())
            stdscr.clear()
            stdscr.refresh()

        if key == ord('q'):
            break

        stdscr.refresh()

curses.wrapper(main)
