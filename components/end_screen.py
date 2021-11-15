import curses
from palettes.colors import Colors
from components.bar import HBar


class EndScreen:

    def __init__(self, logs, win):
        self.win = win

        self.colors = [
            curses.color_pair(Colors.BAR_BORDER),
            curses.color_pair(Colors.BAR_FILLED_COLOR),
            curses.color_pair(Colors.BAR_UNFILLED_COLOR),
            curses.color_pair(Colors.BAR_TEXT)
        ]

        max_y, max_x = win.getmaxyx()
        
        self.acc_bar = HBar(
            win=win.derwin(4, int(max_x/3), 4, 2),
            colors=self.colors,
            text='ACCURACY',
            text_align='center'
        )

        self.wpm_bar = HBar(
            win=win.derwin(4, int(max_x/3), 8, 2),
            colors=self.colors,
            text='WPM',
            text_align='center'
        )

    def run(self, stats):
        self.draw(stats)

    def draw(self, stats):
        self.win.clear()
        
        self.win.box()

        self.acc_bar.total = stats['acc']['total']
        self.acc_bar.value = stats['acc']['correct']
        self.acc_bar.text = f'Accuracy: {int(stats["acc"]["correct"]/stats["acc"]["total"]*100)}%'
        self.acc_bar.draw()

        highest_wpm = 100
        self.wpm_bar.total = highest_wpm
        self.wpm_bar.value = stats['wpm']['val']
        self.wpm_bar.text = f'WPM: {stats["wpm"]["val"]} | Highest WPM: {highest_wpm}'
        self.wpm_bar.draw()

        self.win.refresh() 

        curses.doupdate()
    

