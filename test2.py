string = """{'key1': 'value1', 'key2': 'value2'}"""

dic={}
for i in string:
    key = str()
    keyBool = True
    brace = False
    colon = 0
    keyColon = 0
    
    if i == "'":
        colon+=1
        keyColon+=1
    
    elif keyColon%2 == 0:
        keyBool = False
    
    elif brace == True and keyBool == True:
        key+=i
    
    elif i == "{":
        brace = True
    


