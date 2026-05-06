import os
from config import MAX_CHARS
from google.genai import types
schema_get_file_contents = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads file contents in a specified directory relative to the working directory, up to MAX_CHARS in length",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["file_path"]
    ),
)
def get_file_content(working_directory, file_path):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
        valid_target_file = os.path.commonpath([working_directory_abs, target_file]) == working_directory_abs
        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_file, "r") as f:
            contents = f.read(MAX_CHARS)
            if f.read(1) != "":
                contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return contents

    except Exception as e:
        return f"Error: {e}"
