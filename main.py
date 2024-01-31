import os

def list_files(dir):
    file_list = []
    for root, dirs, files in os.walk(dir):
        if '.git' in dirs:
            dirs.remove('.git')
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

def main():
    dir = os.getcwd()
    files = list_files(dir)
    for file in files:
        print(file)

if __name__ == '__main__':
    main()
    
