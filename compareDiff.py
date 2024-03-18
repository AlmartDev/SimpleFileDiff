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
    # Hours wasted here: 4
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
        if False: #lines1[i] != lines2[i]:
            # IMPORTANT: we're always checking diffrences from file 1 to file 2, better to think about it as file 1 being the original and file 2 being the modified
            # do a new for loop to compare next lines, if there is any match with any of the next lines means that the lines that didnt mathc were added
            # if there is no match, means that the lines that didnt match were removed, then add a new line to the other side?
            
            found_diff = False

            for j in range(max_lines - i):      ## TODO: not working when new or removed lines have content!
            # CHECKING FOR NEW/REMOVED LINES
                if lines1[i] == lines2[j]:
                    # the line was removed from file 2 to file 1
                    color_start = '\033[41;5;231m' # removed
                    color_end = '\033[0m'
                    lines2.insert(i, '')
                    found_diff = True
                    break
                elif lines2[i] != lines2[i]:    #  added
                    color_start = '\033[1;4;12m'
                    color_end = '\033[0m'
                    break
                elif lines2[i] == lines1[j]:
                    # the line was added from file 2 to file 1
                    color_start = '\033[42;5;231m'  
                    color_end = '\033[0m'
                    lines1.insert(i, '')
                    found_diff = True
                    break
               # else:   # line was added from file 1 to file 2 and has new content
               #     color_start = '\033[1;42;231m'               # So no blinking!
               #     color_end = '\033[0m'
               #     lines1.insert(i, '')
               #     break

            if not found_diff:
                # no line was added or removed, but the content has to be different

                # we are gonna add new characters to the line that has less characters
                if len(lines1[i]) < len(lines2[i]):
                    lines1[i] += ' ' * (len(lines2[i]) - len(lines1[i]))
                elif len(lines1[i]) > len(lines2[i]):
                    lines2[i] += ' ' * (len(lines1[i]) - len(lines2[i]))
                
                length = max(len(lines1[i]), len(lines2[i]))    # same on both because of the previous if

                for char in range(length):
                    if lines2[i][char] != lines1[i][char]:
                        # Add color only for those characters that are different
                        color_start = '\033[1;42;231m'  
                        color_end = '\033[0m'

                        # add the color only to the updated characters (make sure not to remove the color from the previous characters)
                        #lines1[i] = lines1[i][:char] + f"{color_start}{lines1[i][char]}{color_end}" + lines1[i][char+1:]
                        #lines2[i] = lines2[i][:char] + f"{color_start}{lines2[i][char]}{color_end}" + lines2[i][char+1:]
                    else:
                        color_start = ''
                        color_end = ''

            # !!: \u2502 is the unicode character for a vertical line
                
            content_file1 = f"{i+1:<4}\u2502  {lines1[i]}"
            space = (screen_width // 2) - len(content_file1)
            content_file2 = f"{i+1:<4}\u2502  {lines2[i]}"
            content_file2 += ' ' * (screen_width // 2 - len(content_file2))

            content = f"{content_file1}{' '*space}{content_file2}"
            print(f"{color_start}{content}{color_end}")
        else:
            # simply print the line

            # TODO: make all this code a function and call it here, something like print_line() or buffer...
            if len(lines1[i]) > screen_width // 2 - 10:
                # cut the text if it's too long
                lines1[i] = lines1[i][:screen_width // 2 - 10] + '...'
            if len(lines2[i]) > screen_width // 2 - 10:
                # cut the text if it's too long
                lines2[i] = lines2[i][:screen_width // 2 - 10] + '...'

            color = ''
            content_file1 = f"{i+1:<4}\u2502  {lines1[i]}"
            space = (screen_width // 2) - len(content_file1)
            content_file2 = f"{i+1:<4}\u2502  {lines2[i]}"

            content = f"{content_file1}{' '*space}{content_file2}"
            print(f"{color}{content}")

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
