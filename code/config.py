GROUND_TRUTH_PATH = "bimacs_rgbd_data_ground_truth"
DERIVED_DATA_PATH = "bimacs_derived_data"
DERIVED_3D_OBJECTS = "bimacs_derived_data_3d_objects"
SAVE_PATH = "data_full.json"

actions_mapping = {0:   'idle', 
                   1:	'approach',
                   2:	'retreat',
                   3:	'lift',
                   4:	'place',
                   5:	'hold',
                   6:	'pour',
                   7:	'cut',
                   8:	'hammer',
                   9:	'saw',
                   10:	'stir',
                   11:	'screw',
                   12:	'drink',
                   13:	'wipe'
                   }
 
objects_mapping =  {0:	'bowl',
                    1:	'knife',
                    2:	'screwdriver',
                    3:	'cutting board',
                    4:	'whisk',
                    5:	'hammer',
                    6:	'bottle',
                    7:	'cup',
                    8:	'banana',
                    9:	'cereals',
                    10:	'sponge',
                    11:	'wood',
                    12:	'saw',
                    13:	'hard drive',
                    14:	'left hand',
                    15:	'right hand'
}

subjects = ['subject_' + str(i) for i in range(1, 7)]
tasks = ['task_1_k_cooking', 'task_2_k_cooking_with_bowls', 'task_3_k_pouring', 'task_4_k_wiping', 
            'task_5_k_cereals', 'task_6_w_hard_drive', 'task_7_w_free_hard_drive', 'task_8_w_hammering', 'task_9_w_sawing']
takes = [f"take_{i}" for i in range(10)]