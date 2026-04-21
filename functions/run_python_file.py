import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a reglar file'
        
        if not target_file[-3:] == ".py":
            return f'Error: "{file_path}" is not a Python file'

        valid_target_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        command = ["python", target_file]
        if args:
            command.extend(args)
        
        process = subprocess.run(command, capture_output=True, timeout=30, text=True)

        result = ""
        if process.returncode != 0:
            result += f"Process exited with code {process.returncode}\n"

        if process.stdout != "":
            result += f"STDOUT: {process.stdout}\n"

        if process.stderr != "":
            result += f"STDERR: {process.stderr}"

        return result
        
    except Exception as e:
        return f"Error: executing Python file {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes/runs a Python file. Use this when the user asks to run, execute, or launch a Python script.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to the Python file to run, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Array of String arguments for the Python function (default is None)",
                items=types.Schema(
                    type=types.Type.STRING,
                ),
            ),
        },
    ),
)