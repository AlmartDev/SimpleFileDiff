import os
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

def draw_diff(content1, content2):
    #
    # How this diff comparison works:
    # Hours wasted here: 2
    #
    # This function should: show both files side by side with its line number
    # highlight when new lines are added or removed, in a different color if added or removed
    # highlight when lines are different, in a different color if added or removed
    #
    # All of it without using any external library or tool, just print statements
    #    

    lines1 = content1.split('\n')
    lines2 = content2.split('\n')

    max_lines = max(len(lines1), len(lines2))

    # first im gonna add all the missing lines to the shorter file
    if len(lines1) < len(lines2):
        for i in range(len(lines2) - len(lines1)):
            lines1.append('')
    elif len(lines1) > len(lines2):
        for i in range(len(lines1) - len(lines2)):
            lines2.append('')

    for i in range(max_lines):
        if lines1[i] != lines2[i]:
            pass
        else:
            # simply print the line
            color = ''
            content_file1 = f"{i+1:<4}|  {lines1[i]}"
            space = (screen_width // 2) - len(content_file1)
            content_file2 = f"{i+1:<4}|  {lines2[i]}"

            content = f"{content_file1}{' '*space}{content_file2}"
            print(f"{color}{content}")

def main():
    parser = argparse.ArgumentParser(
        prog='Simple File Diff',
    )

    parser.add_argument('file1', help='The first file to compare')
    parser.add_argument('file2', help='The second file to compare')
    args = parser.parse_args()

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
