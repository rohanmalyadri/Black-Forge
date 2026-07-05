import os
from black_forge.tools.registry import global_tool_registry, ToolSchema

def read_file(filepath: str) -> str:
    """Read the contents of a file."""
    if not os.path.exists(filepath):
        return f"Error: File {filepath} not found."
    with open(filepath, 'r') as f:
        return f.read()

def write_file(filepath: str, content: str) -> str:
    """Write string content to a file."""
    try:
        with open(filepath, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing to file: {str(e)}"

# Register Built-ins
global_tool_registry.register_tool(
    ToolSchema(name="read_file", description="Reads the contents of a local file by providing its filepath."),
    read_file
)

global_tool_registry.register_tool(
    ToolSchema(name="write_file", description="Writes string content to a local file. Replaces the file if it exists."),
    write_file
)
