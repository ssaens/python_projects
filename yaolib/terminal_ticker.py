import sys
import time
import os

def tick(ticker_text):
    ind = 0
    while True:
        rows, cols = os.popen('stty size', 'r').read().split()
        cols = int(cols)
        wrap_string = ' ' * cols + ticker_text + ' ' * (cols - 1)
        print(wrap_string[ind:ind + cols], end='')
        ind = (ind + 1) % (cols + len(ticker_text))
        time.sleep(0.12)
        print('\b' * cols, end='')
        sys.stdout.flush()

if __name__ == '__main__':
    ticker_text = input('text_to_tick: ')
    os.system('cls' if os.name == 'nt' else 'clear')
    tick(ticker_text)
