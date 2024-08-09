import os
import time
import subprocess

import list_bag_files

def main():

    # # example data
    # bag_files = ['/home/jiahao/datasets/radcliff/1716181664_2024-05-20-06-07-45_0.bag']

    # real data
    bag_files = list_bag_files.list_bag_files('/home/jiahao/datasets/Oxford-Spires/')

    # log
    print('Total bag files: ' + str(len(bag_files)))

    # loop through all bag files
    for i in range(len(bag_files)):
        bag_file = bag_files[i]
        
        # print
        print('Processing: (' + str(i+1) + '/' + str(len(bag_files)) + ') ' + bag_file)

        # process paths
        result_folder = bag_file.replace('.bag', '') + '_ImMesh/'
        prefix = bag_file.split('/')[-1].split('.')[0]
        result_folder_and_prefix = result_folder + prefix

        # create folder
        if not os.path.exists(result_folder):
            os.makedirs(result_folder)
            
        # START ImMesh
        ImMesh_process = subprocess.Popen('roslaunch ImMesh mapping_spire.launch', shell = True)

        # START rosbag record
        rosbag_record_node_name = 'record_path'
        rosbag_record_file_path = result_folder_and_prefix + "_path.bag"
        rosbag_record_topics = '/path'
        rosbag_record_process = subprocess.Popen('rosbag record -O ' + rosbag_record_file_path + ' ' + rosbag_record_topics + ' __name:=' + rosbag_record_node_name, shell = True)

        # RUN play bag file
        play_bag_option = '-r 2'
        subprocess.run('rosbag play ' + bag_file + ' ' + play_bag_option, shell = True)

        # END record
        rosbag_record_process.terminate()
        subprocess.run('rosnode kill /' + rosbag_record_node_name, shell = True)

        # RUN send save command
        subprocess.run('rostopic pub --once /save_command std_msgs/String "' + result_folder_and_prefix + '"', shell = True) # will default latch for 3 second, enough for ImMesh to save

        # END ImMesh
        ImMesh_process.terminate()
        subprocess.run('rosnode kill /laserMapping', shell = True) # kill node
        subprocess.run('pkill ImMesh_mapping', shell = True) # kill gui


if __name__ == '__main__':
    main()