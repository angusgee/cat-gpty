import os
import re

# list all filepaths in the current dir and subdirs
# exclude pycache and .git folders
def list_files(dir):
    file_paths= []
    for root, dirs, files in os.walk(dir):
        if '.git' in dirs:
            dirs.remove('.git')
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')
        for file in files:
            file_paths.append(os.path.join(root, file))
    # print(f"list of files: {file_paths}")
    # print(len(file_paths))
    return file_paths

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
    
    Choose a proompt:
    
    1. Error checking
    2. Security vulnerability assessment
    3. Improvements to memory and time complexity
    4. Add comments and create documentation
    5. No prompt baby I'm raw dogging it
    
    =========================

"""))

prompts = [
    'Act as a senior software engineer performing a code review. Your task is to review the coding project delimited by backticks for potential bugs. Ask as many questions as you need to understand the project before starting.',
    'Act as a senior security engineer performing a code review. Your task is to review the coding project delimited by backticks for security vulnerabilities and suggest ways to make the code more secure. Ask as many questions as you need to understand the project before starting.', 
    'Act as a senior software engineer performing a code review. Your task is to review the coding project delimited by backticks for ways to make the code more effecitent in terms of memory and time complexity. Ask as many questions as you need to understand the project before starting.', 
    'Act as a senior software engineer. Your task is to create documentation for the project delimited by backticks. You shall also review the code for readability and add any comments you think are necessary to make the code easier to understand. Ask as many questions as you need to understand the project before starting.' 
]

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
    prompt_text = '\n```'
    total_token_count = 0
    for file in file_list:
        filename = file.split('/')[-1]
        text_with_delimiters = add_delimiters(remove_blank_rows(read_file(file)))
        token_count =  count_tokens(text_with_delimiters)
        total_token_count += token_count
        print(f"count of tokens for {filename}: {token_count}")
        file_text = f"\n<{filename}>:\n {text_with_delimiters}"
        prompt_text += file_text
    
    while True:
        try:
            shall_proceed = input(f'total token count: {total_token_count}\n do you wish to proceed? Y/N')
            if shall_proceed.upper() == 'Y':
                break
            else:
                print('please select or deselect files')
        except ValueError: 
            print('please choose a valid character')

    print(f"{prompts[user_prompt - 1]},{prompt_text}")
    # print(f"total tokens: {total_token_count}")
    
    try:    
        with open('prompt.txt', 'w', encoding='utf8') as f:
            f.write(f'{prompts[user_prompt - 1]}\n{prompt_text}')
    except OSError as e:
        print(f'error saving to file: {e}')
        
    
    # output to file
    # copy to clipboard
                
if __name__ == '__main__':
    main()
    
