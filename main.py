import os
import re
import glob
import curses
import platform
import pyperclip
from datetime import date

prompts = [
    'Act as a senior software engineer performing a code review. Your task is to review the following coding project for potential bugs. The project files are named and delimited by backticks. Ask as many questions as you need to understand the project before starting.',
    'Act as a senior security engineer performing a code review. Your task is to review the following coding project for security vulnerabilities and suggest ways to make the code more secure. The project files are named and delimited by backticks. Ask as many questions as you need to understand the project before starting.', 
    'Act as a senior software engineer performing a code review. Your task is to review the following coding project for ways to make the code more effecitent in terms of memory and time complexity. The project files are named and delimited by backticks. Ask as many questions as you need to understand the project before starting.', 
    'Act as a senior software engineer. Your task is to create documentation for the following project. The project files are named and delimited by backticks. You shall also review the code for readability and add any comments you think are necessary to make the code easier to understand. Ask as many questions as you need to understand the project before starting.', 
    'Act as a senior software developer and coding mentor. Your task is to refactor the code delimited by triple backticks according to the new requirements in triple quotes. Your output should only be the part of the code you are changing, plus an explanation.\n """PASTE_REQUIREMENTS_HERE"""',
    'Act as a senior software developer and coding mentor. Your task is to correct the code delimited by backticks. The error messages are delimited by triple quotes. Your output should only be the part of the code you are changing, plus an explanation.\n """PASTE_ERROR_MESSAGES_HERE"""' 
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
5. Provide requirements for refactoring or additions to code
6. Provide error message for debugging

=========================

Choose a prompt 1-6, or press any other key to continue without one: """))

# delimit the contents in the format ```\n<filename.ext>:\n ... ````
def process_filename_and_contents(file):
    filename = file.split('/')[-1]
    text_with_delimiters = add_delimiters(remove_blank_rows(read_file(file)))
    file_text = f"\n<{filename}>:\n {text_with_delimiters}"
    return file_text, filename


# lets use the curses lib to handle dynamic file selection
def select_files(stdscr, files):
    # hide the cursor
    curses.curs_set(0)  
    
    # create the colour pair for selected/not selected 
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
   
    # start first screen logic
    # select an optional pre-prompt
    prompt_selected = False
    prompt_index = 0
    while not prompt_selected:
        stdscr.clear()
        stdscr.addstr(0, 0, "Select a prompt:\n\n")
        for i, prompt in enumerate(prompts):
            if i == prompt_index:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(f"{i+1}. {prompt}\n")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(f"{i+1}. {prompt}\n")
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and prompt_index > 0:
            prompt_index -= 1
        elif key == curses.KEY_DOWN and prompt_index < len(prompts) - 1:
            prompt_index += 1
        elif key == ord('\n'):
            prompt_selected = True

    user_prompt = prompt_index  
   
    # start the second screen logic
    # to start with all of the files selected, create a list of true values
    selected = [True] * len(files)
    
    total_token_count = 0
    current_line = 0
    token_counts = [count_tokens(add_delimiters(remove_blank_rows(read_file(file)))) for file in files]
    print(f'token count: token_counts')
    print(type(token_counts))

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "===================================================\n")
        stdscr.addstr(1, 0, f"Total Token Count: {total_token_count}\nPlease select the files you wish to use: \n\n")
        # Display the files and selection state
        for i, file in enumerate(files):
            line_position = i + 4
            selector = "[X]" if selected[i] else "[ ]"
            if i == current_line:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(line_position, 0, f"{selector} {file} - Tokens: {token_counts[i]}")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(line_position, 0, f"{selector} {file} - Tokens: {token_counts[i]}")

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
            if selected[current_line]:
                total_token_count += token_counts[current_line]
            else: 
                total_token_count -= token_counts[current_line]
        # exit on enter key
        elif key == ord('\n'):
            break
        
    selected_files = [file for i, file in enumerate(files) if selected[i]]
    return selected_files, user_prompt

def main():
    # while True:
    #     try:
    #         user_prompt = get_user_input()
    #         if user_prompt in [1, 2, 3, 4, 5, 6]:
    #             break
    #         elif user_prompt == None:
    #             print('continuing without prompt')
    #             break
    #     except ValueError:
    #         print('please enter a number')
    
    # get the project files and remove unwanted ones like .git and pycache
    dir = os.getcwd()
    file_list = remove_files(list_files(dir))

    # Start the curses application which calls select_files
    final_list, user_prompt = curses.wrapper(lambda stdscr: select_files(stdscr, file_list))

    prompt_text = '\n```'
    filenames = []
    for file in final_list:
        file_text, filename = process_filename_and_contents(file) 
        prompt_text += file_text
        filenames += filename 
   
    # clear the terminal and print the final output and success messages
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    final_text = f"{user_prompt} {prompt_text}"
    final_token_count = count_tokens(final_text) 
    print(f'\nFinal token count including pre-prompt: {final_token_count}')

    # copy to clipboard
    try:
        pyperclip.copy(final_text)
        print('Prompt successfully copied to clipboard')
    except OSError as e:
        print(f'error writing to clipboard: {e}\n')   
       
    # write to file
    try:   
        today = date.today()
        output_filename = f'prompt_{today}.txt'
        with open(output_filename, 'w', encoding='utf8') as f:
            f.write(final_text)
            print('Prompt successfully written to file\n')
    except OSError as e:
        print(f'error saving to file: {e}\n')   
 
 
if __name__ == '__main__':
    main()