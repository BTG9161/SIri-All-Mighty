from functions.delete_file import delete_file
from functions.write_file import write_file
from functions.terminal_access import terminal_access


def call_function(function="", wd=".", fp=None, content="", terminal=""):
    if function == "":
        return None

    elif function == "terminal_access":
        return terminal_access(terminal)
    
    elif function == "delete_file":
        return delete_file(wd, fp)
    
    elif function == "write_file":
        return write_file(wd, fp, content)
    
    else:
        return f"No function {function}"



