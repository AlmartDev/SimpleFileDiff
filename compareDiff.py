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

    file1_lines = file1.splitlines()
    file2_lines = file2.splitlines()

    # first we draw both files side by side
    for i, (line1, line2) in enumerate(zip(file1_lines, file2_lines)):
        lineNum = i + 1

        width = curses.COLS // 2 + 6

        stdscr.addstr(i+4, 2, f'{lineNum:3} \u2502 {line1}') 
        stdscr.addstr(i+4, width, f'{lineNum:3} \u2502 {line2}')
        
    # Updated line: RGB(255, 255, 204) or #FFFFCC
    # Added line: RGB(214, 255, 214) or #D6FFD6
    # Deleted line: RGB(255, 229, 229) or #FFE5E5

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # then we draw the differences
    for i, (line1, line2) in enumerate(zip(file1_lines, file2_lines)):
        if line1 != line2:
            
            stdscr.addstr(i+4, 0, ' ' * curses.COLS, curses.A_REVERSE | curses.color_pair(1) | curses.A_BOLD) 
            stdscr.addstr(i+4, 0, f'{i+1:3} \u2502 {line1}', curses.A_REVERSE | curses.color_pair(1) | curses.A_BOLD)
            stdscr.addstr(i+4, width, f'{i+1:3} \u2502 {line2}', curses.A_REVERSE | curses.color_pair(1) | curses.A_BOLD)

def main(stdscr):
    stdscr.clear()

    curses.curs_set(0)

    if not check_file(args.file1) or not check_file(args.file2):
        exit(1)

    file1_content = read_file(args.file1)
    file2_content = read_file(args.file2)

    draw_diff(stdscr, file1_content, file2_content)

    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)