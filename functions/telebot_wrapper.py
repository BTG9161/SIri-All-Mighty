handler = []

def command(name):
    def wrapper(func):
        handler.append((name, func))
        return func
    return wrapper


if __name__ == "__main__":
    @command("start")

    def hello():
        return "hello"
    
    print(handler)