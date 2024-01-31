import os

# list all files in the current dir and subdirs
# exclude pycache and .git folders
def list_files(dir):
    file_list = []
    for root, dirs, files in os.walk(dir):
        if '.git' in dirs:
            dirs.remove('.git')
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

# exclude any files if their extension is in extensions list
def clean_files(files):
    extensions = ['.git', '.gitignore', '.env', '.exe','.jpeg', '.jpg', '.png']
    return [file for file in files if not any(file.endswith(ext) for ext in extensions)]

# read files 
def read_files(file_path):
    try:
        with open(file_path, 'r') as r:
            return r.read()
    except Exception as e:
        print(f'Error reading {file_path}: {e}')
        return ''
        
# roughly count the tokens
# to-do: split longer words into tokens based on five letters per token
# to-do: also split based on '(' and ')' 
def count_tokens(file):
    return len(file.split())

def main():
    dir = os.getcwd()
    cleaned_file_paths = clean_files(list_files(dir))
    for file in cleaned_file_paths:
        print(read_files(file))

if __name__ == '__main__':
    main()
    
