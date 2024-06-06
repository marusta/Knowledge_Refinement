import os
import json
from config import *

# Change current working directory to the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

def read_data(subject_folder, task_folder, take_folder):
    ground_truth_path = os.path.join(GROUND_TRUTH_PATH, subject_folder, task_folder, take_folder + ".json")
    derived_data_path = os.path.join(DERIVED_DATA_PATH, subject_folder, task_folder, take_folder, "spatial_relations")
    derived_3d_objects_path = os.path.join(DERIVED_3D_OBJECTS, "bimacs_derived_data", subject_folder, task_folder, take_folder, "3d_objects")

    ground_truth_data = read_json_file(ground_truth_path)

    frames_data = {}
    for frame_file in os.listdir(derived_data_path):
        frame_number = os.path.splitext(frame_file)[0]  # Extract frame number from filename
        frame_path = os.path.join(derived_data_path, frame_file)
        frames_data[frame_number] = {'spatial_relations' : read_json_file(frame_path)}

    #frames_3d_data = {}
    if os.path.exists(derived_3d_objects_path):
        for frame_file in os.listdir(derived_3d_objects_path):
            frame_number = os.path.splitext(frame_file)[0]  # Extract frame number from filename
            frame_path = os.path.join(derived_3d_objects_path, frame_file)
            #frames_3d_data[frame_number] = {'3d_objects' : read_json_file(frame_path)}  
            frames_data[frame_number]['3d_objects'] = read_json_file(frame_path)

    return ground_truth_data, frames_data#, frames_3d_data

def main():
      
    all_data = []

    for subject in subjects:
        for task in tasks:
            for take in takes:
                #ground_truth_data, frames_data, frames_3d_data = read_data(subject, task, take)
                ground_truth_data, frames_data = read_data(subject, task, take)

                # Map action ids into actions
                r = ground_truth_data['right_hand']
                l = ground_truth_data['left_hand']
                for i in range (len(r)):
                    if i%2 != 0 and r[i]!=None:
                        r[i] =  actions_mapping[r[i]]
                for i in range (len(l)):
                    if i%2 != 0 and l[i]!=None:
                        l[i] =  actions_mapping[l[i]]

                # Map object ids into objects
                for k, v in frames_data.items():
                    for relation in frames_data[k]['spatial_relations']:
                        relation['object_index'] = objects_mapping[relation['object_index']]
                        relation['subject_index'] = objects_mapping[relation['subject_index']]

                data_entry = {
                    'subject': subject,
                    'task': task,
                    'take': take,
                    'right_hand': r,
                    'left_hand': l,
                    ** frames_data
                }
                # for frame, frame_data in frames_data.items():
                #     if frame in frames_3d_data:
                #         frame_data['3d_objects'] = frames_3d_data[frame]
                #     data_entry[frame] = frame_data
                
                all_data.append(data_entry)

    return all_data

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    data = main()
    save_to_json(data, SAVE_PATH)
