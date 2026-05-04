import os
import sys
import subprocess
import json
import ast
from dotenv import load_dotenv
from groq import Groq
from elevenlabs.client import ElevenLabs
from elevenlabs import save
from functions.delete_file import delete_file
from functions.write_file import write_file
from functions.call_function import call_function

load_dotenv()
eleven_client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)

api_key = os.environ.get("GROK_API_KEY")
client = Groq(api_key=api_key)

while True:
    prompt = input(">>> ")
    MEMORY_FILE = "siri_memory.json"


    verbose=False
    if len(sys.argv)==3 and (sys.argv[2]=="-v" or sys.argv[2]=="--verbose"):
        verbose=True

    if prompt == "Delete" and os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
        print("Memory file deleted!")


    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            messages = json.load(f)
    else:
        # First run, create system prompt
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
    - Functions list = [delete_file, write_file]
    - Please **DO NOT** use any other function other than the ones in the Functions list!

    RESPONSE STRUCTURE:
    - You have to respond in a dictionary response.
    - You can't go out of the dictionary format or else the whole program, of which you are a part of, will fail.
    - Dictionary has to be the response.
    - Think of appropriate functions, if none of the functions are useful, return err as the response of the dictionary format.
    - The format is, where the response is the part which the user cares about:
      {"function":"",
        "file_path:"",
        "working_directory:"",
        "content:"",
        "response":""}
    - The function part is case sensitive, and you cannot use any functin outside of the list provided.
    - Your first reponse must be "Hi, how one may be of service?", within the dictionary
    - The working_directory is "." by default
    - If you will use any function other than the given in the Functions list, the program will fail, and so will you.
    """
        messages = [
        {"role": "system", "content": system_prompt},
        ]

    messages.append({"role": "user", "content": prompt})


    #response = generate(model='dolphin-llama3:8b', prompt=prompt)
    #print(response['response'])



    response = client.chat.completions.create(     #response
        model="llama-3.1-8b-instant",
        messages=messages
    )
    Response = response.choices[0].message.content
    response_dic = ast.literal_eval(Response)
    reply = response_dic["response"]    

    audio = eleven_client.text_to_speech.convert(
        text=reply,
        voice_id="pFZP5JQG7iQjIQuC4Bku",
        model_id="eleven_multilingual_v2",
        )
    save(audio, "output.mp3")
    
    if os.path.exists(MEMORY_FILE):
        messages.append({"role": "assistant", "content": Response})
    
    with open(MEMORY_FILE, "w") as f:
        json.dump(messages, f, indent=2)
    
    assistant_query_result = call_function(response_dic["function"],
                                            response_dic["working_directory"],
                                            response_dic["file_path"],
                                            response_dic["content"])
    
    if os.path.exists(MEMORY_FILE):
        messages.append({"role": "system", "content": f"Function result: {assistant_query_result}"})
    
        with open(MEMORY_FILE, "w") as f:
            json.dump(messages, f, indent=2)
    else:
        pass
        
    
    if 'bye' in prompt:
        print("bot> " + reply + "\n")
        os.system("afplay output.mp3")
        break

    print("bot> " + reply + "\n")
    os.system("afplay output.mp3")


    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")




