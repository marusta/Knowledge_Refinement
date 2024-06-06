import json
import trimesh

def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def create_aabb(bounding_box):
    # Create a 3D axis-aligned bounding box (AABB) using trimesh
    min_corner = [bounding_box['x0'], bounding_box['y0'], bounding_box['z0']]
    max_corner = [bounding_box['x1'], bounding_box['y1'], bounding_box['z1']]
    if any(min_c >= max_c for min_c, max_c in zip(min_corner, max_corner)):
        raise ValueError("Invalid bounding box: min corner is not less than max corner")
    aabb = trimesh.primitives.Box(bounds=[min_corner, max_corner])
    return aabb

def calculate_volume(bounding_box):
    length = abs(bounding_box['x1'] - bounding_box['x0'])
    width = abs(bounding_box['y1'] - bounding_box['y0'])
    height = abs(bounding_box['z1'] - bounding_box['z0'])
    return length * width * height

def is_significant_intersection(bb1, bb2, percentage_threshold=20.0):
    try:
        aabb1 = create_aabb(bb1)
        aabb2 = create_aabb(bb2)

        intersection = aabb1.intersection(aabb2)
        if intersection.is_empty or not intersection.is_volume:
            return False
        
        intersection_volume = intersection.volume
        smaller_volume = min(calculate_volume(bb1), calculate_volume(bb2))
        return intersection_volume > (percentage_threshold / 100.0) * smaller_volume
    except ValueError as e:
        print(f"Error creating AABB or calculating intersection: {e}")
        return False
    
def find_significant_intersections(objects, percentage_threshold=20.0):
    intersections = []
    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            bb1 = objects[i]['bounding_box']
            bb2 = objects[j]['bounding_box']
            if is_significant_intersection(bb1, bb2, percentage_threshold):
                intersections.append([objects[i]['class_name'], objects[j]['class_name']])
    return intersections

def find_intersections_in_frames(frame_data, percentage_threshold=20.0):
    if '3d_objects' in frame_data:
        return find_significant_intersections(frame_data['3d_objects'], percentage_threshold)
    return []

def process_data(data, percentage_threshold=20.0):
    processed_data = []
    for entry in data:
        processed_entry = {
            'subject': entry['subject'],
            'task': entry['task'],
            'take': entry['take'],
            'right_hand': entry.get('right_hand', {}),
            'left_hand': entry.get('left_hand', {}),
        }

        processed_entry['intersections'] = {}
        for frame_key in entry:
            if frame_key.startswith('frame_'):
                frame_intersections = find_intersections_in_frames(entry[frame_key], percentage_threshold)
                
                processed_entry['intersections'][frame_key] = frame_intersections
                
        processed_data.append(processed_entry)
    return processed_data

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
    # Read the full data
    data = read_json_file('../data/data_full.json')
    
    # Process the data to find intersections
    processed_data = process_data(data, percentage_threshold=20.0)
    
    # Save the processed data
    save_to_json(processed_data, '../data/data_full_with_intersections.json')