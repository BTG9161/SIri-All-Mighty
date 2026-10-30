# Run this whenever a new tool is created, along with updating execute_tool_call if the function name is changed.

import json 
from tools.memory import memory
from tools.player import Player
from tools.read_file import read_file
from tools.write_file import write_file
from tools.delete_file import delete_file
from mcp.server.fastmcp import FastMCP
from tools.terminal_access import terminal_access


mcp = FastMCP("terminal")

mcp.tool()(delete_file)
mcp.tool()(write_file)
mcp.tool()(terminal_access)
mcp.tool()(memory)
mcp.tool()(read_file)
mcp.tool()(Player.play)

tools = []
tools_string = ""
for tool in mcp._tool_manager.list_tools():
    tools.append({
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.parameters
        }
    })

with open("functions/mcp_server_json_tool.json", 'w') as f:
    json.dump(tools, f, indent=2)

