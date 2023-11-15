import os
import shutil
import glob

DESKTOP_PATH = "C:\\Users\\deand\\Desktop"
DOWNLOADS_PATH = "C:\\Users\\deand\\Downloads"

def get_files_by_type(directory, file_type):
    pattern = os.path.join(directory, f"*.{file_type}")
    files = glob.glob(pattern)
    return files

def list_files(files):
    print("List of files in the directory:")
    for idx, file_name in enumerate(files, start=1):
        print(f"{idx}. {file_name}")

def open_folder(folder_path):
    if os.path.exists(folder_path):
        os.startfile(folder_path)
    else:
        print("Folder does not exist.")

def main():
    
    print("Select the source directory:")
    print("1. Downloads")
    print("2. Desktop")
    source_choice = input("Enter the number corresponding to the source directory: ").lower()

    if source_choice == '1':
        source_path = DOWNLOADS_PATH
    elif source_choice == '2':
        source_path = DESKTOP_PATH
    else:
        print("Invalid choice. Exiting.")
        return

    file_type_choice = input("Enter 'all' for all files or enter any key to pick a specific file by type: ").lower()

    if file_type_choice == 'all':
        files = glob.glob(os.path.join(source_path, "*"))
    else:
        file_type = input("Enter the file type (e.g., txt, pdf): ").lower()
        files = get_files_by_type(source_path, file_type)

    while not files:
        print("No files found in the specified directory.")
        retry_choice = input("Do you want to re-enter the file type? (yes/no): ").lower()
        if retry_choice == 'yes':
            file_type = input("Enter the file type (e.g., txt, pdf): ").lower()
            files = get_files_by_type(source_path, file_type)
        else:
            break

    if not files:
        print("Exiting.")
        return

    list_files(files)

    all_files_choice = input("Do you want to perform the operation on all files? (yes/no): ").lower()

    target_folder = ""  # Initialize target_folder here

    if all_files_choice == 'yes':
        perform_all_files_operation(files, source_path, all_files_choice, target_folder, DESKTOP_PATH)
    # Inside the else block where a specific file is processed
    else:
        file_choice = int(input("Enter the number corresponding to the file you want to process: "))
        selected_file = files[file_choice - 1]
        operation = input("Choose operation (move/copy/rename/delete): ").lower()

        # Updated line to handle target_folder
        target_folder_input = input(f"Enter the target folder path (press Enter for 'Desktop'): ")

        if target_folder_input:
            target_folder = os.path.abspath(target_folder_input)
        else:
            target_folder = os.path.join(os.path.expanduser('~'), 'Desktop')

        perform_file_operation(os.path.join(source_path, selected_file), operation, target_folder)

# Modify the function definition to accept DESKTOP_PATH as a parameter
def perform_all_files_operation(files, source_path, all_files_choice, target_folder, DESKTOP_PATH):
    operation = input("Choose operation (move/copy/rename/delete) for all files: ").lower()

    if operation not in ['move', 'copy', 'rename', 'delete']:
        print("Invalid operation. Please choose move, copy, rename, or delete.")
        return  # Exit the function if the operation is invalid

    if all_files_choice == 'yes':
        if not target_folder:
            target_folder_input = input("Enter the target folder path (press Enter for Desktop): ")
            target_folder = target_folder_input if target_folder_input else DESKTOP_PATH

        if os.path.exists(target_folder) and os.path.isdir(target_folder):
            for file_path in files:
                perform_file_operation(file_path, operation, target_folder)
            open_folder(target_folder)
        else:
            print("Invalid folder path. Operation aborted.")
    else:
        for file_path in files:
            target_folder_input = input(f"Enter the target folder path for {file_path} (press Enter for Desktop): ")
            current_target_folder = target_folder_input if target_folder_input else DESKTOP_PATH

            # Updated the default target_folder value here
            target_folder = os.path.abspath(current_target_folder)

            if os.path.exists(target_folder) and os.path.isdir(target_folder):
                perform_file_operation(file_path, operation, target_folder)
            else:
                print(f"Invalid folder path. Operation aborted for {file_path}.")

def perform_file_operation(file_path, operation, target_folder):
    if operation == 'delete':
        confirm_delete = input(f"Are you sure you want to delete {file_path}? (yes/no): ").lower()
        if confirm_delete == 'yes':
            os.remove(file_path)
            print(f"{file_path} deleted successfully.")
        else:
            print(f"{file_path} was not deleted.")
    elif operation == 'rename':
        new_name = input("Enter the new name for the file: ")
        new_path = os.path.join(os.path.dirname(file_path), new_name)
        os.rename(file_path, new_path)
        print(f"{file_path} renamed to {new_path} successfully.")
    elif operation in ['copy', 'move']:
        if not target_folder:
            print("Target folder path not provided. Operation aborted.")
            return

        if os.path.exists(target_folder) and os.path.isdir(target_folder):
            if operation == 'copy':
                shutil.copy(file_path, os.path.join(target_folder, os.path.basename(file_path)))
                print(f"{file_path} copied successfully.")
            elif operation == 'move':
                shutil.move(file_path, os.path.join(target_folder, os.path.basename(file_path)))
                print(f"{file_path} moved successfully.")
            open_folder(target_folder)
        else:
            print(f"Invalid folder path: {target_folder}. Operation aborted.")
    else:
        print("Invalid operation. Please choose move, copy, rename, or delete.")


if __name__ == "__main__":
    while True:
        main()
        continue_choice = input("Do you want to perform another operation? (yes/no): ").lower()
        if continue_choice != 'yes':
            break
