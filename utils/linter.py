# linter.py
import subprocess

def validate_code(code_string):
    with open("temp.py", "w") as f:
        f.write(code_string)
    
    # Run a simple syntax check
    result = subprocess.run(["python", "-m", "py_compile", "temp.py"], capture_output=True)
    
    if result.returncode != 0:
        return False, result.stderr.decode()
    return True, "Success"