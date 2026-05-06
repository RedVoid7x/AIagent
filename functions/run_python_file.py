import os
import subprocess
from google.genai import types
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to list files from, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Arguments available to input",
                items=types.Schema(
                    type=types.Type.STRING,
                )
            )
        },
            ),
)
def run_python_file(working_directory, file_path, args=None):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
        valid_target_file = os.path.commonpath([working_directory_abs, target_file]) == working_directory_abs
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_file]
        if args != None:
            command.extend(args)
        run_command = subprocess.run(command, capture_output=True, text=True, cwd=working_directory, timeout=30)
        output = ""
        if run_command.stderr == "" and run_command.stdout == "":
            output = "No output produced"
        else:
            output = f"STDOUT:{run_command.stdout}\nSTDERR:{run_command.stderr}"
        if run_command.returncode != 0:
            output += f"Process exited with code {run_command.returncode}"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"