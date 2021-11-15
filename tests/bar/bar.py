import curses


class Bar:

    def __init__(self, win, **kwargs):
        self.win = win
        self.bar_win = None

        self.total = 100
        self.value = 0
        self.text = None
        self.text_align = 'left'

        # by default, the bar will use first 3 color pairs
        self.border_color = curses.color_pair(1)
        self.complete_color = curses.color_pair(2)
        self.incomplete_color = curses.color_pair(3)
        self.text_color = curses.color_pair(4)
        
        for key, value in kwargs.items():
            setattr(self, key, value)

    def draw(self):
        pass

    def draw_text(self):
        pass

    def change_value(self, new_value):
        self.value = new_value
        self.draw()    


class HBar(Bar):

    def __init__(self, win, **kwargs):
        super().__init__(win, **kwargs)
        
        self.bar_win = win.derwin(1,0) # make relative window to draw bar, in order to free up space for text

    def draw(self):
        self.bar_win.clear()
        self.bar_win.attron(self.border_color)
        self.bar_win.box()
        self.bar_win.attroff(self.border_color)

        self.draw_text()
        self.win.refresh()

        max_y, max_x = self.bar_win.getmaxyx()        
        columns_completed = int((self.value/self.total) * (max_x-2) )

        for y in range(1, max_y-1):
            self.bar_win.addstr(y, 1, ' '*columns_completed, self.complete_color)
            self.bar_win.addstr(y, 1+columns_completed, ' '*(max_x-2-columns_completed), self.incomplete_color)

        self.bar_win.refresh()

        curses.doupdate()


    def draw_text(self):
        max_y, max_x = self.win.getmaxyx()

        if type(self.text) != str:
            raise TypeError('Type of text must be str')

        if len(self.text) > max_x:
            raise ValueError('Text too long to fit on bar.')
                
        if self.text_align == 'left':
            self.win.addstr(0, 0, self.text, self.text_color)
            
        elif self.text_align == 'right':
            self.win.addstr(0, max_x-len(self.text), self.text, self.text_color)
            
        elif self.text_align == 'center':
            self.win.addstr(0, (max_x-len(self.text))//2, self.text, self.text_color)


class VBar(Bar):

    def __init__(self, win, **kwargs):
        super().__init__(win, **kwargs)
        
        self.bar_win = win # no text implementation for Vertical bar, so no need to free up space
    
    def draw(self):
        self.bar_win.clear()

        self.bar_win.attron(self.border_color)
        self.bar_win.box()
        self.bar_win.attroff(self.border_color)

        self.draw_text()

        max_y, max_x = self.bar_win.getmaxyx()
        rows_completed = (self.value/self.total) * max_y-1

        for y in range(1, max_y-1):
            if max_y-y-2 < rows_completed:
                self.bar_win.addstr(y, 1, ' '*(max_x-2), self.complete_color)
            else:
                self.bar_win.addstr(y, 1, ' '*(max_x-2), self.incomplete_color )
# 
# 
        # for y in range(1, max_y-1):
            # for x in range(1, max_x-1):
                # if max_y-y-2 < rows_completed:
                    # self.bar_win.addch(y, x, ' ', self.complete_color)
                # else:
                    # self.bar_win.addch(y, x, ' ', self.incomplete_color)

        self.bar_win.refresh()
        curses.doupdate()



