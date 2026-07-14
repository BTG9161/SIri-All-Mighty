from pathlib import Path


memory_file = Path("MEMORY.md")

def memory(memory_piece: str, importance: int) -> str:
    global memory_file
    """
    To store a piece of memory.
    ARGS:
        memory_piece: Piece of memory that needs to be stored.
        importance: How important is the piece of memory.
    """

    with memory_file.open('a', encoding="utf-8") as file:
        file.write(f"\n- {memory_piece}, Importance: {importance}")

def memory_access() -> str:
    global memory_file
    """
    To access stored memories.
    """

    if not memory_file.exists():
        return ""
    
    with memory_file.open('r', encoding="utf-8") as file:
        return file.read()

