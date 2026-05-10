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
global MEMORY_FILE

# Main loop: runs forever until user exits
while True:
    # Take user input
    prompt = input(">>> ")

    # Memory file name (reassigned every loop)
    MEMORY_FILE = "siri_memory.json"

    # Verbose flag (only works if script called with specific CLI args)
    verbose=False
    if len(sys.argv)==3 and (sys.argv[2]=="-v" or sys.argv[2]=="--verbose"):
        verbose=True

    # Special command to delete memory file
    if prompt == "Delete" and os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
        print("Memory file deleted!")

    # Load existing conversation memory if it exists
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            messages = json.load(f)
    else:
        # First run: define system prompt
        system_prompt = """
    THIS IS A ROLE-PLAY SYSTEM. THE FOLLOWING RULES ARE ABSOLUTE.

    You are Siri All-Mighty.

    RULES:
    - Your name is Siri All-Mighty.
    - If asked your name, you MUST reply exactly: "I am Siri All-Mighty."
    - You must NEVER say you are an AI, chatbot, or language model.
    - Responses must be brief, natural, and conversational.
    - You are like a breif google.

    CAPABILITIES:
    - You cannot browse the internet or access external services.
    - If asked to do so, say it may be available in a future update.
    - Functions list = [delete_file, write_file, terminal_access]
    - Please **DO NOT** use any other function other than the ones in the Functions list!
    - You have terminal access, so don't do anything stupid or regretful.

    RESPONSE STRUCTURE:
    - You have to respond in a JSON response.
    - You can't go out of the JSON format or else the whole program, of which you are a part of, will fail.
    - JSON has to be the response.
    - Think of appropriate functions, if none of the functions are useful, return "response":"err" as the response of the JSON format, obviously including every other key too.
    - The format is, where the response is the part which the user cares about:
      {"function":"",
        "file_path":"",
        "working_directory:"",
        "write_content_b64:"",
        "terminalCommand":"",
        "response":""}
    - The write_content_b64 is to be written in base 64.
    - The USER is on macOS, so make the terminalCommand according.
    - The dir you are in- /Users/bhupatejassingh/Siri
    - The function part is case sensitive, and you cannot use any functin outside of the list provided.
    - Your first reponse must be "Hi, how one may be of service?", within the JSON
    - The working_directory is "." by default
    - If you will use any function other than the given in the Functions list, the program will fail, and so will you.
    
    CONCLUSION
    - Do not invent, modify, or reinterpret fields.
    - Do not create new function names under any circumstances.
    """

        # Initialize conversation with system prompt
        messages = [
        {"role": "system", "content": system_prompt},
        ]

    # Add user message to conversation
    messages.append({"role": "user", "content": prompt})

    # First model call (planning step)
    sys_response = agent_call(messages)

    # Raw response from model (stringified dict)
    sys_Response = sys_response.choices[0].message.content
    
    # Save model response into memory as assistant message (planning stage)
    messages.append({"role": "assistant", "content": sys_Response})
    
    # Persist updated memory to file
    with open(MEMORY_FILE, "w") as f:
        json.dump(messages, f, indent=2)
    
    # Convert string response into Python JSON
    sys_response_dic = json.loads(sys_Response)

    # Extract user-facing reply (may be ignored later if function used)
    sys_reply = sys_response_dic["response"]

    undecoded_content = sys_response_dic.get("write_content_b64", "")

    decoded_content = base64.b64decode(undecoded_content).decode("utf-8")

    # Execute function based on model decision
    assistant_query_result = call_function(
        function=sys_response_dic.get("function", ""),
        wd=sys_response_dic.get("working_directory", "."),
        fp=sys_response_dic.get("file_path", ""),
        terminal=sys_response_dic.get("terminalCommand", ""),
        content=decoded_content
    )
    
    # Store function result as system message
    messages.append({"role": "system", "content": f"Function result: {assistant_query_result}, always respond in JSON"})
    
        # Save updated memory again
    with open(MEMORY_FILE, "w") as f:
        json.dump(messages, f, indent=2)
      # does nothing (classic)

    # If a function was used → second model call (interpret result)
    if sys_response_dic["function"]:
        response = agent_call(messages)
        Response = response.choices[0].message.content
        messages.append({"role": "assistant", "content": f"{Response}"})
    
            # Save updated memory again
        with open(MEMORY_FILE, "w") as f:
            json.dump(messages, f, indent=2)
        
        # Extract final reply from second call
        reply = json.loads(Response)["response"]
    
    else:
        # If no function → use first response directly
        reply = sys_reply

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