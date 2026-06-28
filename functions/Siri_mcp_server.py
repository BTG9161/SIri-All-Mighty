#import json 
from functions.delete_file import delete_file
from functions.write_file import write_file
from functions.terminal_access import terminal_access
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("terminal")

mcp.tool()(delete_file)
mcp.tool()(write_file)
mcp.tool()(terminal_access)

#tools = []
#tools_string = ""
#for tool in mcp._tool_manager.list_tools():
#    tools.append({
#        "type": "function",
#        "function": {
#            "name": tool.name,
#            "description": tool.description,
#            "parameters": tool.parameters
#        }
#    })

#with open("mcp_server_json_tool.json", 'w') as f:
#    json.dump(tools, f, indent=2)


mcp.run(transport="stdio")

