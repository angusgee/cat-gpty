import os
import re
import glob
import curses
import pyperclip
from datetime import date

prompts = {
    1: {'title': 'Error checking', 
        'body': 'Act as a senior software engineer performing a code review. Your task is to review the above coding project for potential bugs. The project files are named and delimited by backticks. Ask questions before starting if you need to understand the project. Your output should be a list of suggested improvements, with brief explanations, and the parts of the code you are changing'},
    2: {'title': 'Security vulnerability assessment', 
        'body': 'Act as a senior security engineer performing a code review. Your task is to review the above coding project for security vulnerabilities and suggest ways to make the code more secure. The project files are named and delimited by backticks. Ask questions before starting if you need to understand the project. Your output should be a list of suggested improvements, with brief explanations, and any parts of the code you are changing'},
    3: {'title': 'Improvements to memory and time complexity', 
        'body': 'Act as a senior software engineer performing a code review. Your task is to review the above coding project for ways to make the code more efficient in terms of memory and time complexity. The project files are named and delimited by backticks. Ask  questions before starting if you need to understand the project. Your output should be a list of suggested improvements, with brief explanations, and any parts of the code you are changing'},
    4: {'title': 'Add comments and create documentation', 
        'body': 'Act as a senior software engineer. Your task is to create documentation for the above coding project. The project files are named and delimited by backticks. You shall also review the code for readability and add any comments you think are necessary to make the code easier to understand. Ask questions before starting if you need to understand the project. Your output should be document in the form of a markdown file, plus any additions to the code where you deem it necessary to add comments'},
    5: {'title': 'Provide requirements for refactoring or additions to code', 
        'body': 'Act as a senior software developer and coding mentor. Your task is to refactor the above coding project delimited by triple backticks according to the new requirements in triple quotes. Your output should only be the part of the code you are changing, plus an explanation.\n"""\nPASTE_REQUIREMENTS_HERE\n"""'},
    6: {'title': 'Provide error message for debugging', 
        'body': 'Act as a senior software developer and coding mentor. Your task is to correct the above coding project to fix the errors. The project files are named and delimited by backticks. The error messages are delimited by triple quotes. Your output should only be the part of the code you are changing, plus explanations of your proposed fixes.\n """\nPASTE_ERROR_MESSAGES_HERE\n"""'}
}


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
    excluded_extensions = [
        '.git', '.gitignore', '.env', '.exe', 
        '.jpeg', '.jpg', '.png', '.gif', '.ico', '.svg', '.bmp', '.tiff', '.webp',
        '.mp3', '.wav', '.mp4', '.avi', '.mov', '.flv',
        '.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx',
        '.rar', '.tar', '.gz', '.7z',
        '.o', '.a', '.dll', '.so', '.dylib', '.db', '.sqlite',
        '.log', '.lock', '.bin', '.pyc', '.toc', '.pkg', '.pyz', '.zip', '.spec'
    ]
    return [file for file in files if not any(file.endswith(ext) for ext in excluded_extensions)]

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

# delimit the contents in the format ```\n<filename.ext>:\n ... ````
def process_filename_and_contents(file):
    filename = file.split('/')[-1]
    text_with_delimiters = add_delimiters(remove_blank_rows(read_file(file)))
    file_text = f"\n<{filename}>:\n {text_with_delimiters}"
    return file_text, filename


# lets use the curses lib to handle dynamic file selection
def select_prompt_and_files(stdscr, files):
    # hide the cursor
    curses.curs_set(0)  
    
    # create the colour pair for selected/not selected 
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
   
    # start first screen logic
    # select an optional pre-prompt
    prompt_selected = False
    prompt_index = 0
    exit_without_selection = False
    try:
        while not prompt_selected:
            stdscr.clear()
            stdscr.addstr(0, 0, "Select a prompt, or press any key to continue without one:\n\n")
            for i, prompt in prompts.items():
                title = f"{i}. {prompts[i]['title']}"
                if i == prompt_index + 1:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(title + '\n')
                    stdscr.attroff(curses.color_pair(1))
                else:
                    stdscr.addstr(title + '\n')
            stdscr.refresh()

            key = stdscr.getch()
            if key == curses.KEY_UP and prompt_index > 0:
                prompt_index -= 1
            elif key == curses.KEY_DOWN and prompt_index < len(prompts) - 1:
                prompt_index += 1
            elif key == ord('\n'):
                prompt_selected = True
            else:
                # any other key
                exit_without_selection = True
                break
    
    except curses.error:
        stdscr.clear()
        stdscr.addstr(0, 0, 'Error: Terminal size is too small. Please resize your terminal windowm and try again.')
        stdscr.refresh()
        stdscr.getch()
        return [], '' 
            
    if exit_without_selection:
        user_prompt = ''
    else:
        user_prompt_index = prompt_index + 1
        user_prompt = prompts[user_prompt_index]['body']
   
    # start the second screen logic
    # to start with all of the files selected, create a list of true values
    selected = [True] * len(files)
    
    current_line = 0
    token_counts = [count_tokens(add_delimiters(remove_blank_rows(read_file(file)))) for file in files]
    total_token_count = sum(token_counts) 

    try:
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "===================================================\n")
            stdscr.addstr(1, 0, "Please select/deselect the files you wish to use: \n\n")
            # Display the files and selection state
            for i, file in enumerate(files):
                line_position = i + 3 
                selector = "[X]" if selected[i] else "[ ]"
                if i == current_line:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(line_position, 0, f"{selector} {file} - Tokens: {token_counts[i]}")
                    stdscr.attroff(curses.color_pair(1))
                else:
                    stdscr.addstr(line_position, 0, f"{selector} {file} - Tokens: {token_counts[i]}")

            stdscr.addstr((len(files) + 4), 0, f"Total Token Count: {total_token_count}\nPlease select the files you wish to use: \n\n")
            stdscr.addstr((len(files) + 5), 0, "Press Enter when done\n")
            stdscr.addstr((len(files) + 6), 0, "===================================================\n")
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
    except curses.error:
        stdscr.clear()
        stdscr.addstr(0, 0, 'Error: Terminal size is too small. Please resize your terminal windowm and try again.')
        stdscr.refresh()
        stdscr.getch()
        return [], '' 
   
    selected_files = [file for i, file in enumerate(files) if selected[i]]
    return selected_files, user_prompt

def main():
    
    # get the project files and remove unwanted ones like .git and pycache
    dir = os.getcwd()
    file_list = remove_files(list_files(dir))

    # Start the curses application which calls select_prompt_and_files
    final_list, user_prompt = curses.wrapper(lambda stdscr: select_prompt_and_files(stdscr, file_list))

    prompt_text = '\n```'
    filenames = []
    for file in final_list:
        file_text, filename = process_filename_and_contents(file) 
        prompt_text += file_text
        filenames += filename 
   
    # print the final output and success messages
    final_text = f"{prompt_text}{user_prompt}"
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