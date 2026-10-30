import json
from tools.player import Player
from tools.memory import memory
from tools.read_file import read_file
from tools.write_file import write_file
from tools.delete_file import delete_file
from tools.terminal_access import terminal_access

player = Player()

available_functions={"delete_file": delete_file,
                     "write_file": write_file,
                     "terminal_access": terminal_access,
                     "memory": memory,
                     "read_file": read_file,
                     "play": player.play,
}

def execute_tool_call(tool_call):
    """Parse and execute a single tool call"""
    function_name = tool_call.function.name
    function_to_call = available_functions[function_name]
    function_args = json.loads(tool_call.function.arguments)
    
    # Call the function with unpacked arguments
    return function_to_call(**function_args)

