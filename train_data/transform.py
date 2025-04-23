import os
import random
import shutil

# Paths to files and directories
val_folder = 'val'
train_folder = 'train'
val_list_file = 'val_list.txt'
train_list_file = 'train_list.txt'

# Read the validation list
with open(val_list_file, 'r', encoding='utf-8') as f:
    val_lines = f.readlines()

# Select 131 random entries
num_samples = min(131, len(val_lines))
selected_lines = random.sample(val_lines, num_samples)

# Extract the filenames of selected entries
selected_files = []
for line in selected_lines:
    filename = line.split('\t')[0].split('/', 1)[-1]  # Extract filename without 'val/'
    selected_files.append(filename)

# Read existing training list (if it exists)
train_lines = []
if os.path.exists(train_list_file):
    with open(train_list_file, 'r', encoding='utf-8') as f:
        train_lines = f.readlines()

# Move images and update labels
moved_lines = []
remaining_val_lines = []

for line in val_lines:
    parts = line.split('\t', 1)
    if len(parts) < 2:
        continue
        
    val_path = parts[0]
    filename = val_path.split('/', 1)[-1]  # Extract filename without 'val/'
    
    if filename in selected_files:
        # Source and destination paths for the image
        src_img_path = os.path.join(val_folder, filename)
        dst_img_path = os.path.join(train_folder, filename)
        
        # Move the image file if it exists
        if os.path.exists(src_img_path):
            try:
                shutil.move(src_img_path, dst_img_path)
                print(f"Moved {filename} to train folder")
                
                # Add entry to train list (replace 'val/' with 'train/')
                new_line = line.replace(val_path, f"train/{filename}")
                moved_lines.append(new_line)
            except Exception as e:
                print(f"Error moving {filename}: {e}")
        else:
            print(f"Warning: {src_img_path} not found")
    else:
        remaining_val_lines.append(line)

# Update the train_list.txt
with open(train_list_file, 'a', encoding='utf-8') as f:
    f.writelines(moved_lines)

# Update the val_list.txt with remaining entries
with open(val_list_file, 'w', encoding='utf-8') as f:
    f.writelines(remaining_val_lines)

print(f"Transferred {len(moved_lines)} images and labels from validation to training set")
print(f"Remaining validation entries: {len(remaining_val_lines)}")