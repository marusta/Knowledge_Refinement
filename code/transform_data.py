import json

def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        
def transform_data(data):
    actions = []
    
    # Transform right hand actions
    right_hand_actions = [{'action': data['right_hand'][i], 'frame': data['right_hand'][i-1]} for i in range(1, len(data['right_hand']), 2)]
    for i in range(len(right_hand_actions) - 1):
        action = right_hand_actions[i]['action']
        start_frame = right_hand_actions[i]['frame']
        end_frame = right_hand_actions[i + 1]['frame']
        intersecting_pairs = data['intersections'].get(f'frame_{end_frame}', [])
        actions.append({'action': action, 'actor': 'right_hand', 'start_frame': start_frame, 'end_frame': end_frame, 'intersecting_pairs': intersecting_pairs})
    
    # Transform left hand actions
    left_hand_actions = [{'action': data['left_hand'][i], 'frame': data['left_hand'][i-1]} for i in range(1, len(data['left_hand']), 2)]
    for i in range(len(left_hand_actions) - 1):
        action = left_hand_actions[i]['action']
        start_frame = left_hand_actions[i]['frame']
        end_frame = left_hand_actions[i + 1]['frame']
        intersecting_pairs = data['intersections'].get(f'frame_{end_frame}', [])
        actions.append({'action': action, 'actor': 'left_hand', 'start_frame': start_frame, 'end_frame': end_frame, 'intersecting_pairs': intersecting_pairs})
    
    return actions

if __name__ == "__main__":
    # Read the full data with intersections
    process_data = read_json_file('../data/data_full_with_intersections.json')
        
    transformed_data = []
    for entry in processed_data:
        transformed_entry = {
            'subject': entry['subject'],
            'task': entry['task'],
            'take': entry['take'],
        }
        transformed_entry['actions'] =  transform_data(entry)
        transformed_data.append(transformed_entry)

    save_to_json(transformed_data, '../data/transformed_full_data.json')