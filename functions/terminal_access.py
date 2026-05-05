import subprocess


def terminal_access(content):
    try:
        result = subprocess.run(content,
                                shell=True,
                                capture_output=True,
                                text=True)
        if result.stderr.strip():
            return result.stderr.strip() and result.stdout.strip()
        
        return result.stdout.strip()
    
    
    except Exception as e:
        return str(e)