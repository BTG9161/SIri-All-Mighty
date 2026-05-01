import ast
string = """{'key1': 'value1', 'key2': 'value2'}"""
dic = ast.literal_eval(string)



print(dic)


