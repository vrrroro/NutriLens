import os
import re
import ast

def clean_python(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()
    
    # ast.unparse removes all comments and formats code nicely
    try:
        parsed = ast.parse(source)
        clean_code = ast.unparse(parsed)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(clean_code)
        print(f"Cleaned {file_path}")
    except Exception as e:
        print(f"Error cleaning {file_path}: {e}")

def clean_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()
    
    # Remove Jinja comments {# ... #}
    source = re.sub(r'\{#[\s\S]*?#\}', '', source)
    # Remove HTML comments <!-- ... -->
    source = re.sub(r'<!--[\s\S]*?-->', '', source)
    
    # Remove multiple empty lines
    source = re.sub(r'\n\s*\n', '\n\n', source)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(source)
    print(f"Cleaned {file_path}")

def clean_css_js(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()
    
    if file_path.endswith('.css'):
        source = re.sub(r'/\*[\s\S]*?\*/', '', source)
    elif file_path.endswith('.js'):
        # multiline comments
        source = re.sub(r'/\*[\s\S]*?\*/', '', source)
        # single line comments, making sure we don't hit URLs (though none in this project)
        source = re.sub(r'(?<!:)\/\/.*', '', source)
    
    # Remove empty lines
    source = re.sub(r'\n\s*\n', '\n\n', source)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(source)
    print(f"Cleaned {file_path}")


base_dir = r"c:\Users\rohit\Downloads\NutriLens"
files = [
    os.path.join(base_dir, "app.py"),
    os.path.join(base_dir, "data", "nutrition_db.py"),
    os.path.join(base_dir, "data", "__init__.py"),
    os.path.join(base_dir, "templates", "index.html"),
    os.path.join(base_dir, "templates", "results.html"),
    os.path.join(base_dir, "static", "css", "style.css"),
    os.path.join(base_dir, "static", "js", "main.js")
]

for file_path in files:
    if not os.path.exists(file_path):
        continue
    if file_path.endswith('.py'):
        clean_python(file_path)
    elif file_path.endswith('.html'):
        clean_html(file_path)
    elif file_path.endswith(('.css', '.js')):
        clean_css_js(file_path)

print("Done cleaning all comments!")
