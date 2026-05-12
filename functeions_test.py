from functions.agent_call import agent_call
from functions.delete_file import delete_file
from functions.write_file import write_file
from functions.call_function import call_function
import json

sys_response_dic = json.loads("{\"function\":\"write_file\" \n,\"file_path\": \"test3.py\"\n,\"working_directory\": \".\"\n,\"write_content\": \"def is_even(num): return num % 2 == 0 \\ndef is_odd(num): return not is_even(num)\\ndef main(): print(\\\"Enter a number: \\\") num = int(input()) if is_odd(num): print(f\\\"{num} is odd.\\\") else: print(f\\\"{num} is even.\\\") if __name__ == \\\"__main__\\\": main()\"\n, \"terminalCommand\": \"python test3.py\"\n, \"response\": \"Created file at . test3.py\"}")

# Extract user-facing reply (may be ignored later if function used)
sys_reply = sys_response_dic["response"]

# Execute function based on model decision
assistant_query_result = call_function(
    function=sys_response_dic.get("function", ""),
    wd=sys_response_dic.get("working_directory", "."),
    fp=sys_response_dic.get("file_path", ""),
    terminal=sys_response_dic.get("terminalCommand", ""),
    content=sys_response_dic.get("write_content", "")
)

print(assistant_query_result)
