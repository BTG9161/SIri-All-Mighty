import os
import sys
import json


def tool(tool):
    params = tool["function"]["parameters"]
    params.pop("title", None)
    params["additionalProperties"] = False

    for prop in params.get("properties", {}).values():
        prop.pop("title", None)
    
    return tool

def _resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_path, relative_path)

with open(_resource_path("functions/mcp_server_json_tool.json")) as f:
    tools = [tool(t) for t in json.load(f)]

