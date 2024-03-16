import curses
import argparse

parser = argparse.ArgumentParser(
                    prog='Simple File Diff',
                    description='Easily compare between two files')

parser.add_argument('file1', help='The first file to compare')
parser.add_argument('file2', help='The second file to compare')

args = parser.parse_args()

def check_file(file):
    try:
        with open(file, 'r') as f:
            return True
    except FileNotFoundError:
        return False

def read_file(file):
    with open(file, 'r') as f:
        return f.read()

def draw_title(stdscr, file1, file2):
    title = f'Comparing {file1} and {file2}'
    stdscr.addstr(1, 2, " Simple File Diff ", curses.A_STANDOUT | curses.A_BOLD)
    stdscr.addstr(2, 2, title, curses.A_BOLD)

def draw_diff(stdscr, file1, file2):
    draw_title(stdscr, args.file1, args.file2)

    for i, line in enumerate(file1.splitlines()):
        lineNum = i + 1 
        stdscr.addstr(i+4, 2, f'{lineNum:3} \u2502 {line}') 
    for i, line in enumerate(file2.splitlines()):
        width = curses.COLS // 2 + 6
        lineNum = i + 1
        stdscr.addstr(i+4, width, f'{lineNum:3} \u2502 {line}')
    # mid line
    # for i in range(curses.LINES):
    #    stdscr.addstr(i, curses.COLS // 2, '\u2502')

def main(stdscr):
    stdscr.clear()

    if not check_file(args.file1) or not check_file(args.file2):
        exit(1)

    file1_content = read_file(args.file1)
    file2_content = read_file(args.file2)

    draw_diff(stdscr, file1_content, file2_content)

    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)