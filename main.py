import os

# customisable list of file extensions to ignore
extensions = [
    '.git',
    '.gitignore', 
    '.env', 
    '.exe'
]

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

def clean_files(files):
    return [file for file in files if not any(file.endswith(ext) for ext in extensions)]

def count_tokens():
    return 0

def main():
    dir = os.getcwd()
    files = list_files(dir)
    cleaned_files = clean_files(files)
    for file in cleaned_files:
        print(file)

if __name__ == '__main__':
    main()
    
