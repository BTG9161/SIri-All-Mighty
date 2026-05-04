from functions.delete_file import delete_file
from functions.write_file import write_file



def call_function(function="", wd=".", fp=None, content=""):
    if function == "":
        return None

    elif function == "delete_file":
        return delete_file(wd, fp)
    
    elif function == "write_file":
        return write_file(wd, fp, content)
    
    else:
        return f"No function {function}"



