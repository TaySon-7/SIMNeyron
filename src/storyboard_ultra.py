import os

folder_path = "dataset2/Videos"
for file_name in os.listdir(folder_path):
    if os.path.isfile(os.path.join(folder_path, file_name)):
        print(file_name)
