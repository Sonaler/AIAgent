import os

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    
    try:
        path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(path, file_path))
        valid_full_path = os.path.commonpath([path, full_path]) == path

        if not valid_full_path:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(full_path) as f:
            content = f.read(MAX_CHARS)

            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            
        return content


    except Exception as e:
        return f"Error: {e}"