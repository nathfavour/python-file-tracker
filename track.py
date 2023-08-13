import os
import json

def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size

def track_directory(directory_path):
    tracking_data = {}

    for dirpath, dirnames, filenames in os.walk(directory_path):
        folder_info = {
            "folder_name": os.path.basename(dirpath),
            "size": get_folder_size(dirpath),
            "file_information": []
        }
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, "r") as file:
                    lines = sum(1 for _ in file)
            except (IOError, UnicodeDecodeError):
                lines = 0
            file_info = {
                "name": filename,
                "size": os.path.getsize(filepath),
                "lines": lines,
            }
            folder_info["file_information"].append(file_info)
        tracking_data[os.path.basename(dirpath)] = folder_info

    return tracking_data

def write_tracking_to_file(tracking_data, filename):
    with open(filename, "w") as file:
        json.dump(tracking_data, file, indent=4)

def compare_tracking_data(original_data, new_data):
    differences = []
    for folder_name, new_folder_info in new_data.items():
        if folder_name in original_data:
            original_folder_info = original_data[folder_name]
            if original_folder_info != new_folder_info:
                differences.append(f"Folder '{folder_name}' has changed.")
        else:
            differences.append(f"Folder '{folder_name}' is new.")
    
    for folder_name, original_folder_info in original_data.items():
        if folder_name not in new_data:
            differences.append(f"Folder '{folder_name}' has been deleted.")

    return differences

def print_differences(differences):
    if differences:
        print("Differences in file and folder information:")
        for diff in differences:
            print("-", diff)
    else:
        print("No differences found.")

def main():
    tracking_filename = "tracks.txt"
    new_tracking_data = track_directory(".")
    
    if os.path.exists(tracking_filename):
        with open(tracking_filename, "r") as file:
            original_tracking_data = json.load(file)
        
        differences = compare_tracking_data(original_tracking_data, new_tracking_data)
        print_differences(differences)

    write_tracking_to_file(new_tracking_data, tracking_filename)
    print("Tracking information saved in", tracking_filename)

if __name__ == "__main__":
    main()
