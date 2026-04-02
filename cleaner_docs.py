import os
import ast

def strip_docstrings(node):
    if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef, ast.Module)):
        # Check if the first node in the body is a docstring
        if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant):
            if isinstance(node.body[0].value.value, str):
                node.body.pop(0)
    for child in ast.iter_child_nodes(node):
        strip_docstrings(child)
    return node

base_dir = r"c:\Users\rohit\Downloads\NutriLens"
files = [
    os.path.join(base_dir, "app.py"),
    os.path.join(base_dir, "data", "nutrition_db.py"),
    os.path.join(base_dir, "data", "__init__.py")
]

for file_path in files:
    if not os.path.exists(file_path):
        continue
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()
    try:
        parsed = ast.parse(source)
        parsed = strip_docstrings(parsed)
        clean_code = ast.unparse(parsed)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(clean_code)
        print(f"Cleaned docstrings in {file_path}")
    except Exception as e:
        print(f"Error {e}")
