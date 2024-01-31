import os
import settings 

def list_files(dir):
    return [os.path.join(root, file) for root, dirs, files in os.walk(dir) if '.git' in dirs for file in files]

def main():
    dir = os.getcwd()
    files = list_files(dir)
    for file in files:
        print(file)

if __name__ == '__main__':
    main()
    
