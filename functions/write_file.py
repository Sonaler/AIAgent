import os

def write_file(working_directory, file_path, content):

    try:
        path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(path, file_path))
        is_valid_path = os.path.commonpath([full_path, path]) == path

        if not is_valid_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(full_path):
            f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(path, exist_ok=True)

        with open(full_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"