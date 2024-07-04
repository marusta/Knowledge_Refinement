# Knowledge_Refinement

- Link of the original dataset with the documentation: https://bimanual-actions.humanoids.kit.edu/original_dataset#object-relations-label-mapping

### Getting Started
- download datasets from:
  - https://bimanual-actions.humanoids.kit.edu/download/bimacs_rgbd_data_ground_truth.zip
  - https://bimanual-actions.humanoids.kit.edu/download/bimacs_derived_data_3d_objects.zip
  - https://bimanual-actions.humanoids.kit.edu/download/bimacs_derived_data_spatial_relations.zip

### Reading and transforming data
- This is the order of .py files to run:
  1. read_all_data.py
  2. find_intersections.py
  3. transform_data.py

 - As a result of these steps transformed_data.json is created.

### Transforming intermediate .json format to the memnet format:
- code/to_memnet_format.py ----> complete_action_patterns.json is created

