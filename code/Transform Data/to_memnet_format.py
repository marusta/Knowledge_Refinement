import time
from bson import ObjectId
import json
import os
import sys

start_time = time.time()

def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def generate_uuid():
    return str(ObjectId())

def frame_to_time(start, frame):
    frame_secs = frame/30
    return start + frame_secs

def action_to_node(action, subject):
    return {
        "link": "spec_to",
        "parent_attributes": {"accessid": [f"{action['action']}.v.01"]},
        'node_attributes': {
                            "type": "action",
                            "utterances": [action['action']],
                            "timestamp": frame_to_time(start_time, action['start_frame']),
                            "duration" : frame_to_time(0, action['end_frame'] - action['start_frame']),
                            "memory": "stm",
                            "uuid": generate_uuid(),
                            "actor": action['actor'],
                            "start_frame": action['start_frame'],
                            "end_frame": action['end_frame'],
                            }
    }

def object_to_node(object):
    return { 
        "link": "spec_to",
        "parent_attributes": {"accessid": ["object.n.01"]},
        'node_attributes': {
                            "type": "object",
                            "utterances": [object],
                            "memory": "stm",
                            "uuid": generate_uuid()
                            }
    }

def create_link(link_type, parent_uuid, child_uuid):
    return {
        "link": link_type,
        "parent_attributes": {"uuid": parent_uuid},
        "node_attributes": {
            "uuid": child_uuid
        }
    }

def transform_data(data):
    nodes = []
    links = []

    for entry in data:
        subject = entry['subject']
        task = entry['task']
        take = entry['take']
        actions = entry['actions']

        # Create and add abstract action a.k.a parent action node
        parent_node = {
            "link": "spec_to",
            "parent_attributes": {"accessid": [f"{task}.v.01"]},
            'node_attributes': {
                                "type": "action",
                                "utterances": [task],
                                "timestamp": start_time,
                                "memory": "stm",
                                "uuid": generate_uuid(),
                                "subject": subject
                                }
        }

        # Create and add subject node
        subject_node = {
            "link": "spec_to",
            "parent_attributes": {"accessid": ["person.n.01"]},
            'node_attributes': {
                                "type": "agent",
                                "utterances": [subject],
                                "memory": "stm",
                                "uuid": generate_uuid()
                            }
        }

        nodes.append(parent_node)
        nodes.append(subject_node)
        nodes.append(create_link("has_actor", parent_node['node_attributes']['uuid'], subject_node['node_attributes']['uuid']))

        preceding_action = None

        objects = {}

        # Process actions and create corresponding nodes and links
        for action in actions:
            action_node = action_to_node(action, subject)
            nodes.append(action_node)

            if 'tool' in action:
                if action['tool'][0] not in objects.keys():
                    object_node = object_to_node(action['tool'])
                    nodes.append(object_node)
                    objects[action['tool'][0]] = object_node
                else:
                    object_node = objects[action['tool'][0]]
                
                # Create a link between action and object
                links.append(create_link("has_object", action_node['node_attributes']['uuid'], object_node['node_attributes']['uuid']))

            # Create a link between abstract action and action
            links.append(create_link("has_element", parent_node['node_attributes']['uuid'], action_node['node_attributes']['uuid']))

            if preceding_action:
                if preceding_action['node_attributes']['end_frame'] == action_node['node_attributes']['start_frame'] and preceding_action['node_attributes']['actor'] == action_node['node_attributes']['actor']:
                    links.append(create_link("has_next", preceding_action['node_attributes']['uuid'], action_node['node_attributes']['uuid']))

            preceding_action = action_node

    return nodes, links


if __name__ == "__main__":

    data = read_json_file(os.path.join(sys.path[0],"..", "data",'transformed_full_data_fixed.json'))
    nodes, links = transform_data(data)

    save_to_json(nodes + links, os.path.join(sys.path[0],"..", "data", 'complete_action_patterns.json'))