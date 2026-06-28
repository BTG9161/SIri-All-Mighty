import json


def tool(tool):
    params = tool["function"]["parameters"]
    params.pop("title", None)
    params["additionalProperties"] = False

    for prop in params.get("properties", {}).values():
        prop.pop("title", None)
    
    return tool

with open("functions/mcp_server_json_tool.json") as f:
    tools = [tool(t) for t in json.load(f)]

