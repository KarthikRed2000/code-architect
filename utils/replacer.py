import ast

def surgical_replace(file_path, target_function_name, new_code):
        with open(file_path, "r") as f:
            lines = f.readlines()

        # 1. Re-parse the file to find the current line numbers of the function
        tree = ast.parse("".join(lines))
        target_node = None
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name == target_function_name:
                target_node = node
                break

        if not target_node:
            print(f"Error: Could not find {target_function_name} in {file_path}")
            return

        # 2. Extract the line range (AST line numbers are 1-indexed)
        start_idx = target_node.lineno - 1
        end_idx = target_node.end_lineno

        # 3. Replace the old lines with the new code
        # We add a newline to ensure spacing is correct
        lines[start_idx:end_idx] = [new_code + "\n"]

        # 4. Write back to the file
        with open(file_path, "w") as f:
            f.writelines(lines)
        
        print(f"Successfully refactored {target_function_name} in {file_path}")