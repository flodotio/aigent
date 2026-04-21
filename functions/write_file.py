import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.isdir(target_file):
            return f"Error: Cannot write to '{file_path}' as it is a directory"

        valid_target_dir= os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_dir:
            return f"Error: Cannot read {file_path} as it is outside the permitted working directory"
        
        try:
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
        except:
            return f"Error: create directories"

        with open(target_file, "w") as f:
            f.write(content)

        return f"Successfully wrote to '{file_path}' ({len(content)} characters written)"
        
    except:
        return f"Error: exception in write_file()"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the content to a file in a specified path relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to store the file to, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content that is written to the file",
            ),
        },
    ),
)