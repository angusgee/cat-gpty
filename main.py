import os
import re
import glob
import curses
import pyperclip

prompts = [
    'Act as a senior software engineer performing a code review. Your task is to review the following coding project for potential bugs. The project files are named and delimited by backticks. Ask as many questions as you need to understand the project before starting.',
    'Act as a senior security engineer performing a code review. Your task is to review the following coding project for security vulnerabilities and suggest ways to make the code more secure. The project files are named and delimited by backticks. Ask as many questions as you need to understand the project before starting.', 
    'Act as a senior software engineer performing a code review. Your task is to review the following coding project for ways to make the code more effecitent in terms of memory and time complexity. The project files are named and delimited by backticks. Ask as many questions as you need to understand the project before starting.', 
    'Act as a senior software engineer. Your task is to create documentation for the following project. The project files are named and delimited by backticks. You shall also review the code for readability and add any comments you think are necessary to make the code easier to understand. Ask as many questions as you need to understand the project before starting.' 
]

# list all filepaths in the current dir and subdirs
# exclude pycache, node_modules, and .git folders
def list_files(dir):
    pattern = os.path.join(dir, '**', '*')
    all_paths = glob.glob(pattern, recursive=True)
    files = [path for path in all_paths if os.path.isfile(path)]
    cleaned_files = [f for f in files if "pycache" not in f and '.git' not in f and 'node_modules' not in f]
    # print(cleaned_files)
    return cleaned_files
 
# exclude file if extension is in list
def remove_files(files):
    extensions = ['.git', '.gitignore', '.env', '.exe','.jpeg', '.jpg', '.png']
    return [file for file in files if not any(file.endswith(ext) for ext in extensions)]

def read_file(file_path):
    try:
        with open(file_path, 'r') as r:
            return r.read()
    except Exception as e:
        print(f'Error reading {file_path}: {e}')
        return ''

def remove_blank_rows(text):
    return '\n'.join([line for line in text.splitlines() if line.strip() != ''])

def add_delimiters(text):
    return f"{text}\n```"
        
def count_tokens(text):
    tokens = re.findall(r'\b\w+\b|\S', text)
    return len(tokens)

def get_user_input():
    return int(input("""
=========================

1. Error checking
2. Security vulnerability assessment
3. Improvements to memory and time complexity
4. Add comments and create documentation
5. No prompt I'm raw dogging it

=========================

Choose a prompt: """))

def process_filename_and_contents(file):
    filename = file.split('/')[-1]
    text_with_delimiters = add_delimiters(remove_blank_rows(read_file(file)))
    token_count = count_tokens(text_with_delimiters)
    print(f"count of tokens for {filename}: {token_count}")
    file_text = f"\n<{filename}>:\n {text_with_delimiters}"
    return file_text, filename, token_count

def select_files(stdscr, files):
    # hide the cursor
    curses.curs_set(0)  
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    # create a list of false values the same length as the file list
    selected = [False] * len(files)
    current_line = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "===================================================\n")
        stdscr.addstr(1, 0, "Please select the files you wish to use: \n\n")
        # Display the files and selection state
        for i, file in enumerate(files):
            line_position = i + 3
            selector = "[X]" if selected[i] else "[ ]"
            if i == current_line:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(line_position, 0, f"{selector} {file}")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(line_position, 0, f"{selector} {file}")

        stdscr.addstr((len(files) + 4), 0, "Press Enter when done\n")
        stdscr.addstr((len(files) + 5), 0, "===================================================\n")
        stdscr.refresh()

        # Keyboard handling
        key = stdscr.getch()
        # move up
        if key == curses.KEY_UP:
            current_line = max(0, current_line - 1)
        # move down
        elif key == curses.KEY_DOWN:
            current_line = min(len(files) - 1, current_line + 1)
        # select or deselect file using spacebar
        elif key == ord(' '):
            selected[current_line] = not selected[current_line]
        # exit on enter key
        elif key == ord('\n'):
            break
        
    return [file for i, file in enumerate(files) if selected[i]]

def main():
    while True:
        try:
            user_prompt = get_user_input()
            if user_prompt in [1, 2, 3, 4, 5]:
                break
            else:
                print('please choose a valid option 1-5')
        except ValueError:
            print('please enter a number')
    dir = os.getcwd()
    file_list = remove_files(list_files(dir))

    # Start the curses application
    final_list = curses.wrapper(lambda stdscr: select_files(stdscr, file_list))

    prompt_text = '\n```'
    total_token_count = 0
    filenames = []
    for file in final_list:
        file_text, filename, token_count = process_filename_and_contents(file) 
        total_token_count += token_count
        prompt_text += file_text
        filenames += filename 
   
    # print(final_list)

    while True:
        try:
            shall_proceed = input(f'total token count: {total_token_count}\n do you wish to proceed? Y/N: ')
            if shall_proceed.upper() == 'Y':
                break
            else:
                break
        except ValueError: 
            print('please choose a valid character')

    # copy to clipboard
    try:
        pyperclip.copy(f"{prompts[user_prompt - 1]} {prompt_text}")
        print('Prompt successfully copied to clipboard')
    except OSError as e:
        print(f'error writing to clipboard: {e}')   
       
    # write to file
    try:    
        with open('prompt.txt', 'w', encoding='utf8') as f:
            f.write(f'{prompts[user_prompt - 1]}\n{prompt_text}')
            print('Prompt successfully written to file')
            
    except OSError as e:
        print(f'error saving to file: {e}')   
 
 
if __name__ == '__main__':
    main()