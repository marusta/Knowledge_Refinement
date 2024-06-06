import json

def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def propagate_tools(actions):
    # Forward pass: Propagate tools from subsequent actions
    for i in range(len(actions) - 1):
        if 'tool' not in actions[i]:
            if actions[i]['action'] != 'retreat' and  actions[i]['action'] != 'idle':
                for j in range(i + 1, len(actions)):
                    if 'tool' in actions[j]:
                        actions[i]['tool'] = actions[j]['tool']
                        break

    # Backward pass: Handle 'retreat' actions
    for i in range(len(actions) - 1, 0, -1):
        if actions[i]['action'] == 'retreat' and 'tool' not in actions[i]:
            for j in range(i - 1, -1, -1):
                if 'tool' in actions[j]:
                    actions[i]['tool'] = actions[j]['tool']
                    break

    return actions

if __name__ == "__main__":
    # Read the full transformed data
    transformed_data = read_json_file('../data/transformed_full_data.json')
 
    for i in range (len(transformed_data)):
        acts = propagate_tools(transformed_data[i]['actions'])
        transformed_data[i]['actions'] = acts

    # Save the processed data
    save_to_json(transformed_data, '../data/transformed_data.json')

