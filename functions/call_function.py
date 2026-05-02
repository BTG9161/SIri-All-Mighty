from functions.delete_file import delete_file
from functions.write_file import write_file



def call_function(function, wd=".", fp=None, content=""):
    if function == "delete_file":
        result = delete_file(wd, fp)
    
    if function == write_file:
        result = write_file(wd, fp, content)
    
    return result