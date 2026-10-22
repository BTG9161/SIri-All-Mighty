import os
from pathlib import Path


memory_file = Path("MEMORY.md")

def memory(memory_piece: str, importance: int) -> str:
    """
    To store a piece of memory.
    ARGS:
        memory_piece: Piece of memory that needs to be stored.
        importance: How important is the piece of memory, in a scale of 1 to 10.
    
    NOTE: While creating a memory keep in mind that the memory should be in third person perspective, and not in first person.
    """
    global memory_file

    with memory_file.open('r', encoding="utf-8") as f:
        memories = f.read()
        if not "# MEMORIES" in memories:
            with memory_file.open('w', encoding="utf-8") as file:
                file.write("# MEMORIES \n")
    try:
        with memory_file.open('a', encoding="utf-8") as file:
            file.write(f"\n- {memory_piece}, Importance: {importance}")

        return f"Memory stored: {memory_piece} with importance {importance}."

    except Exception as e:
        return f"Error storing memory: {e}"


def memory_access() -> str:
    global memory_file
    """
    To access stored memories.
    """

    if not memory_file.exists():
        return ""
    
    with memory_file.open('r', encoding="utf-8") as file:
        return file.read()

def delete_memory() -> str:
    """
    To delete a specific memory or """

