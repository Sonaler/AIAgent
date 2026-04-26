import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments if any are provided",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
                description="Optional arguments that can be provided to run command"
            )
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        output = ""
        path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(path, file_path))
        is_valid_path = os.path.commonpath([path, full_path]) == path

        if not is_valid_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(full_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if full_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'
        

        command = ["python", full_path]
        if args is not None:
            command.extend(args)

        process = subprocess.run(command, text=True, timeout=30, capture_output=True)

        if process.returncode != 0:
            output += f"Process exited with code {process.returncode}"
        
        if len(process.stderr) == 0 and len(process.stdout) == 0:
            output += "No output produced"
            return output
        
        if len(process.stdout) > 0:
            output += "STDOUT:" + process.stdout

        if len(process.stderr) > 0:
            output += "STDERR:" + process.stderr
        
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"