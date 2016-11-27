import curses
import random
import time
import os
from sort import insertionsorter, selectionsorter, mergesorter

VERSION, BUILD, PATCH = 0, 0, 1
DISPLAYS = [insertionsorter, selectionsorter, mergesorter]

def main(stdscr):
    curses.curs_set(False)
    stdscr.clear()

    stdscr.addstr(0, 0, "viSort Test Build {}.{}.{}".format(VERSION, BUILD, PATCH))
    stdscr.refresh()

    ROWS, COLUMNS = curses.LINES, curses.COLS
    infoport = curses.newwin(1, COLUMNS, 1, 0)
    viewport = curses.newwin(ROWS - 2, COLUMNS, 2, 0)

    while 1:
        render_header(infoport, 'Data')

        lst = [random.randint(0, ROWS - 3) for _ in range(COLUMNS)]
        render_sort(viewport, lst)
        k = stdscr.getkey()

        render_header(infoport, 'Selection Sort')
        visualize_sort(viewport, selectionsorter, lst, 0.05)

        k = stdscr.getkey()

        render_header(infoport, 'Insertion Sort')
        visualize_sort(viewport, insertionsorter, lst, 0.001)

        k = stdscr.getkey()

        render_header(infoport, 'Merge Sort (Bottom Up)')
        visualize_sort(viewport, mergesorter, lst, 0.1)

        k = stdscr.getkey()

    k = stdscr.getkey()

def render_header(view, msg):
    view.clear()
    view.addstr(0, 0, msg)
    view.refresh()

def visualize_sort(view, sort, lst, delay=0.05):
    to_sort = lst[:]
    for l in sort(to_sort):
        render_sort(view, l)
        time.sleep(delay)

def render_sort(view, lst):
    view.clear()
    vh, vw = view.getmaxyx()
    try:
        for i, x in enumerate(lst):
            row = vh - 1 - x
            view.addstr(row, i, '.')
            for j in range(row + 1, vh):
                view.addstr(j, i, ' ')
    except:
        pass
    view.refresh()

def views():
    index = 0
    yield DISPLAYS[index]
    index += 1
    if index >= len(DISPLAYS):
        index = 0

if __name__ == '__main__':
    curses.wrapper(main)
