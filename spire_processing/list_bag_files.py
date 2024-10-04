# given a folder directionary, list all files within this folder, and within folder of this folder recursively, that have .bag extension

import os

# traverse all folders and subfolders to find all bag files
# skip if under trajectory folder
def list_bag_files(folder):
    bag_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            # if end with .bag and not end with _path.bag and does not start with Fast-LIO
            if file.endswith('.bag') and not file.endswith('_path.bag') and 'trajectories' not in root and not file.startswith('Fast-LIO'):
                bag_files.append(os.path.join(root, file))
    return bag_files

def list_mission_folder(folder):
    bag_files = list_bag_files(folder)
    mission_folders = []
    for bag_file in bag_files:
        # folder path using os.path.dirname
        mission_folders.append(os.path.dirname(bag_file))
    
    # unique
    mission_folders = list(set(mission_folders))
    return mission_folders

def convert_string_to_list(input_string):
    list = input_string.split('\n')
    return list

# if __name__ == '__main__':
#     folder = '/home/jiahao/datasets/Oxford-Spires/'
#     bag_files = list_bag_files(folder)

#     # pretty print
#     for bag_file in bag_files:
#         print(bag_file)
#     print('Total bag files: ' + str(len(bag_files)))

if __name__ == '__main__':
    folder = '/home/jiahao/datasets/Oxford-Spires/'
    mission_folder = list_mission_folder(folder)
    
    # pretty print
    for folder in mission_folder:
        print(folder)
    print('Total mission folders: ' + str(len(mission_folder)))