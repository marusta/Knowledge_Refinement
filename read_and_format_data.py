import json
import zipfile
import os
print(os.getcwd())
from config import *

def jsons_from_zip(zip_filename):
    with zipfile.ZipFile(zip_filename, mode="r") as archive:
        files = archive.namelist()

    jsons = []
    for f in files:
        with zipfile.ZipFile(zip_filename, mode="r") as archive:
            with archive.open(f) as myfile:
                jsons.append({f : json.loads(myfile.read())})
        
    return jsons

def map_actions(jsons_ground_truth):
    for j_file in jsons_ground_truth:
        r = list(j_file.values())[0]['right_hand']
        l = list(j_file.values())[0]['left_hand']

        for i in range (len(r)):
            if i%2 != 0 and r[i]!=None:
                r[i] =  actions_mapping[r[i]]
        
        for i in range (len(l)):
            if i%2 != 0 and l[i]!=None:
                l[i] =  actions_mapping[l[i]]


def get_frames(ground_truth_json):
    for k, v in ground_truth_json.items():
        frames = [i for i in v['right_hand'] if type(i)==int]
        actions = [i for i in v['right_hand'] if type(i)!=int]
        # frames.extend([i for i in v['left_hand'] if type(i)==int])
        frame_files = [k.replace('bimacs_rgbd_data_ground_truth', 'bimacs_derived_data').replace('.json', '/spatial_relations/') + 'frame_' + str(i) + '.json' for i in frames]
    return frame_files, actions

def read_spacial_relations(jsons_ground_truth):
    all_sequences = []
    for json_1 in jsons_ground_truth:
        frame_files, actions = get_frames(json_1)

        seq_1 = {}
        for path in frame_files:
            components = path.split('/')
            seq_1['task'] = components[2]
            seq_1['subject'] = components[1]
            seq_1['take'] = components[3]
            with open(path) as f:
                d = json.load(f)
                seq_1[components[-1].replace('.json', '')] = {}
                if frame_files.index(path) < len(actions):
                    seq_1[components[-1].replace('.json', '')]['action'] = actions[frame_files.index(path)]
                for i, js in enumerate(d):
                    if js['relation_name'] in ('moving together', 'halting together', 'fixed moving together', 
                        'getting close', 'moving apart', 'stable', 'temporal') and js['object_index'] < js['subject_index']:
        
                        seq_1[components[-1].replace('.json', '')]['relation_name'] = js['relation_name'] 
                        seq_1[components[-1].replace('.json', '')]['objects'] = [objects_mapping[js['object_index']], objects_mapping[js['subject_index']]]
        all_sequences.append(seq_1)
    return all_sequences

def save_jsons_data(all_sequences, filename):
    save_file = open(filename, "w")  
    json.dump(all_sequences, save_file, indent = 6)  
    save_file.close()  

def main():
    jsons_ground_truth = jsons_from_zip(GROUND_TRUTH_PATH)
    map_actions(jsons_ground_truth) # action ids are translated into actions
    all_sequences = read_spacial_relations(jsons_ground_truth)
    save_jsons_data(all_sequences, SAVE_PATH)

if __name__ == "__main__":
    main()