import os
import sys
import subprocess
import json
import base64
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import save
from functions.agent_call import agent_call
from functions.call_function import call_function

# Load environment variables (API keys, etc.)
load_dotenv()

# Initialize ElevenLabs TTS client
eleven_client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)

# Declare memory file globally (even though you redefine it later… interesting choice)
global USER_MEMORY_FILE
global FUNC_MEMORY_FILE
USER_MEMORY_FILE = "siri_user_memory.json"
FUNC_MEMORY_FILE = "siri_func_memory.json"

function_call = bool

# Main loop: runs forever until user exits
while True:
    # Take user input
    prompt = input(">>> ")

    # Verbose flag (only works if script called with specific CLI args)
    verbose=False
    if len(sys.argv)==3 and (sys.argv[2]=="-v" or sys.argv[2]=="--verbose"):
        verbose=True

    # Special command to delete memory file
    if prompt == "Delete" and os.path.exists(USER_MEMORY_FILE) and os.path.exists(FUNC_MEMORY_FILE):
        os.remove(USER_MEMORY_FILE)
        os.remove(FUNC_MEMORY_FILE)
        print("Memory file deleted!")

    # Load existing conversation memory if it exists
    if os.path.exists(USER_MEMORY_FILE) and os.path.exists(FUNC_MEMORY_FILE):
        with open(USER_MEMORY_FILE, "r") as f:
            user_messages = json.load(f)
        
        with open(FUNC_MEMORY_FILE, "r") as f:
            func_messages = json.load(f)

    else:
        # First run: define system prompts
        with open("system_prompt.txt") as f:
            user_system_prompt = f.read()
        
        with open("system_function_prompt.txt") as f:
            func_system_prompt = f.read()

        # Initialize conversation with system prompt
        user_messages = [
        {"role": "system", "content": user_system_prompt},
        ]

        func_messages = [
        {"role": "system", "content": func_system_prompt},
        ]

    # Add user message to conversation
    user_messages.append({"role": "user", "content": prompt})

    # First model call (planning step)
    sys_response = agent_call(user_messages)

    # Raw response from model (stringified dict)
    sys_Response = sys_response.choices[0].message.content
    
    # Save model response into memory as assistant message (planning stage)
    user_messages.append({"role": "assistant", "content": sys_Response})
    
    # Persist updated memory to file
    with open(USER_MEMORY_FILE, "w") as f:
        json.dump(user_messages, f, indent=2)
    
    with open(FUNC_MEMORY_FILE, "w") as f:
        json.dump(func_messages, f, indent=2)
    
    if sys_Response.startswith("{"):
        try:
            # Convert string response into Python JSON
            sys_response_dic = json.loads(sys_Response)

            # Extract user-facing reply (may be ignored later if function used)
            sys_reply = sys_response_dic["response"]

            undecoded_content = sys_response_dic.get("write_content_b64", "")

            decoded_content = base64.b64decode(undecoded_content).decode("utf-8")

        
            # Save updated memory again
            with open(USER_MEMORY_FILE, "w") as f:
                json.dump(user_messages, f, indent=2)


            # If a function was used → second model call (interpret result)
            if sys_response_dic["functions"]:
                response = agent_call(user_messages)
                Response = response.choices[0].message.content
                user_messages.append({"role": "assistant", "content": f"{Response}"})
                
                # Execute function based on model decision
                assistant_query_result = call_function(
                    function=sys_response_dic.get("function", ""),
                    wd=sys_response_dic.get("working_directory", "."),
                    fp=sys_response_dic.get("file_path", ""),
                    terminal=sys_response_dic.get("terminalCommand", ""),
                    content=decoded_content
                )
                
                # Store function result as system message
                user_messages.append({"role": "system", "content": f"Function result: {assistant_query_result}, always respond in JSON"})

                    # Save updated memory again
                with open(USER_MEMORY_FILE, "w") as f:
                    json.dump(user_messages, f, indent=2)
                
                # Extract final reply from second call
                reply = json.loads(Response)["response"]
            
            else:
                # If no function → use first response directly
                reply = sys_reply
        
        except json.JSONDecodeError:
            print("Invalid JSON")
    
    else:
        reply = sys_Response

    # Convert reply to speech
    audio = eleven_client.text_to_speech.convert(
        text=reply,
        voice_id="pFZP5JQG7iQjIQuC4Bku",
        model_id="eleven_multilingual_v2",
    )

    # Save audio file
    save(audio, "output.mp3")
        
    # Exit condition
    if 'bye' in prompt:
        print("bot> " + reply + "\n")
        os.system("afplay output.mp3")
        break

    # Print reply and play audio
    print("bot> " + reply + "\n")
    os.system("afplay output.mp3")

    # Verbose logging (tokens, etc.)
    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {sys_response.usage.prompt_tokens}")
        print(f"Response tokens: {sys_response.usage.completion_tokens}")