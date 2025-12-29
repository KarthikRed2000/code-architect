# ast-parser.py

import ast
import os

def parse_codebase(directory):
    code_metadata = []
    if not os.path.isdir(directory):
        print(f"The directory {directory} does not exist.")
        return code_metadata
    
    print(f"Starting to parse codebase in directory: {directory}")
    for root, _, files in os.walk(directory):
        print(f"Parsing directory: {root}")
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    try:
                        source_code = f.read()
                        tree = ast.parse(source_code)
                        for node in ast.walk(tree):
                            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                                deps = get_dependencies(node) # Use your existing function
                                code_metadata.append({
                                    "type": "function" if isinstance(node, ast.FunctionDef) else "class",
                                    "name": node.name,
                                    "file": path,
                                    "content": ast.get_source_segment(source_code, node),
                                    "dependencies": ",".join(deps) # Store as comma-separated string
                                })
                    except Exception as e:
                        print(f"Could not parse {path}: {e}")
    return code_metadata

def get_dependencies(node):
    dependencies = []
    for child in ast.walk(node):
        # Check for variable and class usage
        if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
            dependencies.append(child.id)

        # Check for base classes in class definitions
        if isinstance(child, ast.ClassDef):
            for base in child.bases:
                if isinstance(base, ast.Name):
                    dependencies.append(base.id)

        # Check for imported modules
        if isinstance(child, ast.Import):
            for alias in child.names:
                dependencies.append(alias.name)
        
        # Check for from ... import ... statements
        if isinstance(child, ast.ImportFrom):
            for alias in child.names:
                dependencies.append(alias.name)
    return list(set(dependencies))

# Usage
data = parse_codebase("./messy-ecommerce")
print(f"Extracted {len(data)} code blocks!")