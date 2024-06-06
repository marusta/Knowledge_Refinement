# Knowledge_Refinement

- Link of the original dataset with the documentation: https://bimanual-actions.humanoids.kit.edu/original_dataset#object-relations-label-mapping

### Getting Started
- download datasets from:
  - https://bimanual-actions.humanoids.kit.edu/download/bimacs_rgbd_data_ground_truth.zip
  - https://bimanual-actions.humanoids.kit.edu/download/bimacs_derived_data_3d_objects.zip
  - https://bimanual-actions.humanoids.kit.edu/download/bimacs_derived_data_spatial_relations.zip

### Reading and transforming data
- This is the order of python files to run:
  1. read_all_data.py
  2. find_intersections.py
  3. transform_data.py
  4. propagate_tools.py

 - As a result of this steps transformed_data.json is created.
