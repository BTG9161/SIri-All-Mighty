#import json 
from delete_file import delete_file
from write_file import write_file
from terminal_access import terminal_access
from memory import memory
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("terminal")

mcp.tool()(delete_file)
mcp.tool()(write_file)
mcp.tool()(terminal_access)
mcp.tool()(memory)

mcp.run(transport="stdio")

