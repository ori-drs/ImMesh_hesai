import os
import time
import subprocess

from list_bag_files import list_bag_files
from list_bag_files import convert_string_to_list

def main():

    # # example data
    # bag_files = ['/home/jiahao/datasets/radcliff/1716181664_2024-05-20-06-07-45_0.bag']

    # real data
    mission_list = convert_string_to_list('''/home/jiahao/datasets/Oxford-Spires/Christ-Church/rosbag/1710927712
                                          /home/jiahao/datasets/Oxford-Spires/Blenheim/rosbag/1710410169-ethan-walk-for-lintong
                                          /home/jiahao/datasets/Oxford-Spires/Keble/rosbag/1710252275''')

    # log
    print('Total missions: ' + str(len(mission_list)))

    # loop through all bag files
    for i in range(len(mission_list)):
        mission_folder = mission_list[i]
        
        # print
        print('Processing: (' + str(i+1) + '/' + str(len(mission_list)) + ') ' + mission_folder)

        # process paths
        mission_location = mission_folder.split('/')[-3]
        mission_timestamp = mission_folder.split('/')[-1]
        result_folder = '/home/jiahao/datasets/Oxford-Spires_ImMesh2/' + mission_location + '_' + mission_timestamp + '/'
        prefix = mission_location + '_' + mission_timestamp
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
        play_bag_option = '-r 1'
        subprocess.run('rosbag play ' + mission_folder + '/17*.bag ' + play_bag_option, shell = True)

        # END record
        rosbag_record_process.terminate()
        subprocess.run('rosnode kill /' + rosbag_record_node_name, shell = True)

        # RUN send save command
        subprocess.run('rostopic pub --once /save_command std_msgs/String "' + result_folder_and_prefix + '"', shell = True) # will default latch for 3 second, enough for ImMesh to save
        time.sleep(60) # wait for ImMesh to save


        # END ImMesh
        ImMesh_process.terminate()
        subprocess.run('rosnode kill /laserMapping', shell = True) # kill node
        subprocess.run('pkill ImMesh_mapping', shell = True) # kill gui


if __name__ == '__main__':
    main()