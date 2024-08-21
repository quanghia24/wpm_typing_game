import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to speed typing!")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm = 0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")  # line 1 at index 0
    for i, char in enumerate(target):
        if(i < len(current)):
            if (char == current[i]):
                stdscr.addstr(0, i, char, curses.color_pair(2))  # line 0 at index i
            else:
                stdscr.addstr(0, i, current[i], curses.color_pair(3))

    stdscr.refresh()
          
def load_text():
    with open('text.txt', 'r') as file:
        lines = file.readlines() # return list of lines
        return random.choice(lines).strip() # strip to remove last character

def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while (True):
        time_elapesed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapesed/60)) / 5) 
        stdscr.clear()

        if (len(current_text) >= len(target_text)): break
        display_text(stdscr, target_text, current_text, wpm)

        try:
            key = stdscr.getkey()
        except:
            continue
    
        if key in ("KEY_BACKSPACE", '\b', '\x7f'):
            if (len(current_text) > 0):
              current_text.pop()
        else:
            current_text.append(key)

    stdscr.nodelay(False)
    if (target_text == "".join(current_text)): 
        stdscr.addstr(2, 0, "You have finish the test!") 
        stdscr.addstr(3, 0, f"Your score is:{wpm}")
        

def main(stdscr):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    while (True):
        start_screen(stdscr)
        wpm_test(stdscr)

        stdscr.addstr("\nPress any key to continue!")
        stdscr.getkey() 
    
wrapper(main)


