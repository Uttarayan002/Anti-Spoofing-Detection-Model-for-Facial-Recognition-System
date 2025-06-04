import os
import random
import shutil
from itertools import islice

################################################################################
output_folder_path = "/home/rik/Documents/face_spoof_detection/dataset/splitdata"  # Output directory for split data
input_folder_path = "/home/rik/Documents/face_spoof_detection/dataset/all"  # Input directory containing all data
split_ratio = {"train": 0.8, "val": 0.1, "test": 0.1}  # Split ratios
classes = ["fake", "real"]  # Class names
################################################################################

try:
    # Remove existing output directory if it exists
    shutil.rmtree(output_folder_path)
except OSError as e:
    pass

# Create directories for train, val, and test data
os.makedirs(f"{output_folder_path}/train/images", exist_ok=True)
os.makedirs(f"{output_folder_path}/train/labels", exist_ok=True)
os.makedirs(f"{output_folder_path}/val/images", exist_ok=True)
os.makedirs(f"{output_folder_path}/val/labels", exist_ok=True)
os.makedirs(f"{output_folder_path}/test/images", exist_ok=True)
os.makedirs(f"{output_folder_path}/test/labels", exist_ok=True)

# Get the names of all files in the input folder
list_name = os.listdir(input_folder_path)
unique_name = [name.split('.')[0] for name in list_name]
unique_name = list(set(unique_name))  # Remove duplicates

# Shuffle the list of unique names
random.shuffle(unique_name)

# Calculate the number of images for each split
len_data = len(unique_name)
print(f'Total Images: {len_data}')
len_train = int(len_data * split_ratio["train"])
len_val = int(len_data * split_ratio["val"])
len_test = int(len_data * split_ratio["test"])

# Adjust training data length if there's a remainder
if len_data != len_train + len_val + len_test:
    remaining = len_data - (len_train + len_val + len_test)
    len_train += remaining

print(f'Total Images: {len_data} \nSplit: {len_train} {len_val} {len_test}')

# Split the list of unique names
length_to_split = [len_train, len_val, len_test]
input_iter = iter(unique_name)
output = [list(islice(input_iter, elem)) for elem in length_to_split]
print(f'Total Images: {len_data} \nSplit: {len(output[0])} {len(output[1])} {len(output[2])}')

# Copy files to respective directories based on split
sequence = ['train', 'val', 'test']
for i, out in enumerate(output):
    for file_name in out:
        shutil.copy(f'{input_folder_path}/{file_name}.jpg', f'{output_folder_path}/{sequence[i]}/images/{file_name}.jpg')
        shutil.copy(f'{input_folder_path}/{file_name}.txt', f'{output_folder_path}/{sequence[i]}/labels/{file_name}.txt')

print("Split process complete")

# Create data.yaml file for training configuration
data_yaml = f'''train: {output_folder_path}/train/images
val: {output_folder_path}/val/images
test: {output_folder_path}/test/images

nc: {len(classes)}
names: {classes}


'''

# Write data.yaml file
with open(f"{output_folder_path}/data.yaml", 'w') as f:
    f.write(data_yaml)

print("data.yaml file created")
