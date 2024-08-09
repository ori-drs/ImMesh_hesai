# given a folder directionary, list all files within this folder, and within folder of this folder recursively, that have .bag extension

import os

# traverse all folders and subfolders to find all bag files
def list_bag_files(folder):
    bag_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            # if end with .bag and not end with _path.bag
            if file.endswith('.bag') and not file.endswith('_path.bag'):
                bag_files.append(os.path.join(root, file))
    return bag_files

if __name__ == '__main__':
    folder = '/home/jiahao/datasets/Oxford-Spires/'
    bag_files = list_bag_files(folder)

    # pretty print
    for bag_file in bag_files:
        print(bag_file)
    print('Total bag files: ' + str(len(bag_files)))