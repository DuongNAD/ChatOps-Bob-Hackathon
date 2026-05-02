import os
import pathspec

def get_project_tree(root_dir, ignore_dirs=['.git', '__pycache__', 'venv', '.venv', 'node_modules']):
    tree_str = ""
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        level = root.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * (level)
        tree_str += f"{indent}{os.path.basename(root)}/\n"
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            tree_str += f"{subindent}{f}\n"
    return tree_str

tree = get_project_tree('e:/project/IBM_Hackathon')
print(tree)
