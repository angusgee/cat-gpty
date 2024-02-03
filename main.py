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
    print(f"list of files: {file_paths}")
    print(len(file_paths))
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
    return f"{text}```"
        
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
    prompt_text = ''
    total_token_count = 0
    for file in file_list:
        filename = file.split('/')[-1]
        blank_rows_removed = remove_blank_rows(read_file(file))
        text_with_delimiters = add_delimiters(blank_rows_removed)
        token_count =  count_tokens(text_with_delimiters)
        total_token_count += token_count
        print(f"count of tokens for {filename}: {token_count}")
        file_text = f"\n{filename}:\n {text_with_delimiters}"
        prompt_text += file_text
    print(prompt_text)
    print(f"total tokens: {total_token_count}")
        
        

    # concatenate the delimited strings, filepaths, and text together
    # add the prompt based on user selection
    # output to file
    # copy to clipboard
                
if __name__ == '__main__':
    main()
    
