import os

def rename_files():
    current_directory = os.path.dirname(__file__)
    working_directory = os.path.join(current_directory, "prank")
    
    files = os.listdir(working_directory)

    os.chdir(working_directory)

    for file_name in files:
        os.rename(file_name, file_name.translate(None, "0123456789"))    

    os.chdir(current_directory)

rename_files()