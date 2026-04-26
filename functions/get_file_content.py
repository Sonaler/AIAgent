import os

from google.genai import types

MAX_CHARS = 10000

schema_get_file_content = types.FunctionDeclaration(
    name = "get_file_content",
    description= "Returns the first 10000 characters of the provided file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description = "Path to the file, relative to the working directory"
            ),
        },
    ),
)

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
        