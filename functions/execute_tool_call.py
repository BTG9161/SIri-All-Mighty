import json
from functions.delete_file import delete_file
from functions.write_file import write_file
from functions.terminal_access import terminal_access


available_functions={"delete_file": delete_file,
                     "write_file": write_file,
                     "terminal_access": terminal_access,
}

def execute_tool_call(tool_call):
    """Parse and execute a single tool call"""
    function_name = tool_call.function.name
    function_to_call = available_functions[function_name]
    function_args = json.loads(tool_call.function.arguments)
    
    # Call the function with unpacked arguments
    return function_to_call(**function_args)

