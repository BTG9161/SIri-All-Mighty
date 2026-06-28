import json

with open("functions/mcp_server_json_tool.json") as f:
    for t in json.load(f):
        print(t)



