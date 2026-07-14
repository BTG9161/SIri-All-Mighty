import os
import sys
import json
import threading
from dotenv import load_dotenv
from functions.STT import STT_loop
from functions.memory import memory_access
from functions.agent_call import agent_call
from functions.agent_call import final_call
from functions.eleven_call import eleven_call
from functions.execute_tool_call import execute_tool_call
from functions.wake import global_listener, input_queue, type_done


# Load environment variables (API keys, etc.)
load_dotenv()
prompt_list = []
listener = global_listener()
stt = threading.Thread(target=STT_loop, daemon=True) # daemon=True marks a thread as a background/daemon thread — it tells Python's threading system
stt.start()

USER_MEMORY_FILE = "siri_memory.json"
memory = memory_access()

print("Chatting benings...")
# Main loop: runs forever until user exits
while True:
    # Take user input
    type_done.clear()
    type_done.wait()
    prompt = ""

    chunks = []

    while not input_queue.empty():
        chunks.append(input_queue.get()) # .get() fetches the 
    
    prompt = " ".join(chunks)

    if not prompt.strip():
        continue        
    
    # Verbose flag (only works if script called with specific CLI args)
    verbose=False
    if len(sys.argv)==3 and (sys.argv[2]=="-v" or sys.argv[2]=="--verbose"):
        verbose=True

    # Special command to delete memory file
    if prompt.lower() == "delete" and os.path.exists(USER_MEMORY_FILE):
        os.remove(USER_MEMORY_FILE)
        print("Memory file deleted!")
        break

    # Load existing conversation memory if it exists
    if os.path.exists(USER_MEMORY_FILE):
        with open(USER_MEMORY_FILE, "r") as f:
            user_messages = json.load(f)

    else:
        # First run: define system prompts
        with open("system_prompt.txt") as f:
            system_prompt = f.read()
            system_prompt += f"""Long-term:
            {memory}"""

        # Initialize conversation with system prompt
        user_messages = [
        {"role": "system", "content": system_prompt},
        ]
    
    user_messages.append({"role": "user", "content": prompt})
    with open(USER_MEMORY_FILE, "w") as f:
            json.dump(user_messages, f, indent=2)
    
    response = agent_call(user_messages)
    Response = response.choices[0].message.content
    
    # Check for tool calls
    if response.choices[0].message.tool_calls:
        # Execute each tool call (using the helper function from step 2)
        for tool_call in response.choices[0].message.tool_calls:
            function_response = execute_tool_call(tool_call)
            
            # Add tool result to messages
            user_messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": tool_call.function.name,
                "content": str(function_response)
            })
        
        # Send results back and get final response
        final_response = final_call(user_messages)
        final_Response = final_response.choices[0].message.content

        user_messages.append({"role": "assistant", "content": final_Response})

        reply = final_Response
        
        with open(USER_MEMORY_FILE, "w") as f:
            json.dump(user_messages, f, indent=2)
    
    else:
        reply = Response
        # Save model response into memory as assistant message (planning stage)

        user_messages.append({"role": "assistant", "content": Response})
        with open(USER_MEMORY_FILE, "w") as f:
            json.dump(user_messages, f, indent=2)
    
    eleven_call(reply)
    # Exit condition
    if 'bye'.lower() in prompt:
        print("bot> " + reply + "\n")
        os.system("afplay output.mp3")
        break

    # Print reply and play audio
    print("bot> " + reply + "\n")
    os.system("afplay output.mp3")

    # Verbose logging (tokens, etc.)
    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

