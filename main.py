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
def clean_files(files):
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
    dir = os.getcwd()
    cleaned_files_list = clean_files(list_files(dir))
    for file in cleaned_files_list:
        filename = file.split('/')[-1]
        print(f"count of tokens for {filename}: {count_tokens(remove_blank_rows(read_file(file)))}")
    while True:
        try:
            user_prompt = get_user_input()
            if user_prompt in [1, 2, 3, 4, 5]:
                break
            else:
                print('please choose a valid option 1-5')
        except ValueError:
            print('please enter a number')
            
if __name__ == '__main__':
    main()
    
