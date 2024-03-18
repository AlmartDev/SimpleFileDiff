import os
import difflib
import argparse

screen_width = os.get_terminal_size().columns

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_file(file_path):
    return os.path.isfile(file_path)

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def draw_title(file1, file2):
    title = "\033[1;7m Simple File Diff \033[0m"
    print(title.center(os.get_terminal_size().columns))

    title = f'\033[1mComparing {file1} and {file2}\033[0m\n'
    print(title.center(os.get_terminal_size().columns))

    title = f"{file1:^{screen_width//2}}{file2:^{screen_width//2}}"
    color_start = '\033[1;4;12m'
    color_end = '\033[0m'
    print(f"{color_start}{title}{color_end}")

def print_line(index=0, line1='', line2='', color_start='', color_end=''):
    if len(line1) > screen_width // 2 - 10:
        # cut the text if it's too long
        line1 = line1[:screen_width // 2 - 10] + '...'
    if len(line2) > screen_width // 2 - 10:
        # cut the text if it's too long
        line2 = line2[:screen_width // 2 - 10] + '...'

    if index != 0:
        content_file1 = f"{index+1:<4}\u2502  {line1}"
        space = (screen_width // 2) - len(content_file1)
        content_file2 = f"{index+1:<4}\u2502  {line2}"
    else:
        content_file1 = f"{'##':<4}\u2502  {line1}"
        space = (screen_width // 2) - len(content_file1)
        content_file2 = f"{'##':<4}\u2502  {line2}"

    content = f"{content_file1}{' '*space}{content_file2}"
    print(f"{color_start}{content}{color_end}")

def draw_diff(content1, content2):
    lines1 = content1.splitlines()
    lines2 = content2.splitlines()

    # make both files the same length
    if len(lines1) > len(lines2):
        lines2 += [''] * (len(lines1) - len(lines2))
    elif len(lines2) > len(lines1):
        lines1 += [''] * (len(lines2) - len(lines1))

    diff = difflib.ndiff(lines1, lines2)

    # draw side by side diff
    for index, line in enumerate(diff):
        if line.startswith('-'):
            print_line(index, line[2:], '', '\033[31m', '\033[0m')
        elif line.startswith('+'):
            print_line(index, '', line[2:], '\033[32m', '\033[0m')
        elif line.startswith('?'):
            line = line.rstrip()
            print_line(0, line[2:], line[2:], '\033[1;34m', '\033[0m')
        else:
            print_line(index, line, line)
        

def main():
    parser = argparse.ArgumentParser(
        prog='Simple File Diff',
    )

    parser.add_argument('file1', help='The first file to compare')
    parser.add_argument('file2', help='The second file to compare')

    parser.add_argument('--version', '-v', action='version', version='%(prog)s (sfd) 1.0')
    parser.add_argument('--clear', '-c', action='store_true', help='Clear the screen before showing the diff')

    args = parser.parse_args()

    if args.clear:
        clear_screen()

    if not (check_file(args.file1) and check_file(args.file2)):
        print("Error: One or more files do not exist.")
        exit(1)

    file1_name = os.path.basename(args.file1)
    file2_name = os.path.basename(args.file2)

    file1_content = read_file(args.file1)
    file2_content = read_file(args.file2)

    draw_title(file1_name, file2_name)
    draw_diff(file1_content, file2_content)

if __name__ == '__main__':
    main()
