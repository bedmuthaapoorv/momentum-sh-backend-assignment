from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import os
import shutil
import ast
from git import Repo
import stat
import errno
from Config.DatabaseConnector import Connection 
app = FastAPI()
connInstance=Connection()
class RepoInput(BaseModel):
    repo_url: HttpUrl

def clone_repo(repo_url: str, clone_path: str):
    if os.path.exists(clone_path):
        shutil.rmtree(clone_path, onerror=handle_remove_readonly)
    Repo.clone_from(repo_url, clone_path)

def handle_remove_readonly(func, path, exc_info):
    exc_type, exc_value, exc_traceback = exc_info
    if func in (os.unlink, os.rmdir) and exc_value.errno == errno.EACCES:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    else:
        raise

def extract_function_metadata(node, file_content, class_name, file_name):
    function_code = ast.get_source_segment(file_content, node)
    return {
        "class_name": class_name,
        "function_name": node.name,
        "args": [arg.arg for arg in node.args.args],
        "docstring": ast.get_docstring(node),
        "code": function_code
    }

def extract_classes_from_file(file_path: str):
    with open(file_path, "r") as file:
        file_content = file.read()
    tree = ast.parse(file_content)
    class_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    return class_names

def extract_functions_from_file(file_path: str):
    with open(file_path, "r") as file:
        file_content = file.read()
    tree = ast.parse(file_content)
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    class_name = None
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            break
    function_metadata = []
    for func_node in functions:
        function_metadata.append(extract_function_metadata(func_node, file_content, class_name, os.path.basename(file_path)))
    return function_metadata, class_name

def extract_functions_from_repo(clone_path: str):
    functions_metadata = {}
    class_names = set()
    for root, _, files in os.walk(clone_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                function_metadata, class_name = extract_functions_from_file(file_path)
                functions_metadata[file_path] = function_metadata
                if class_name:
                    class_names.add(class_name)
    return functions_metadata, list(class_names)

@app.post("/repos/")
async def analyze_repo(repo: RepoInput):
    repo_url = repo.repo_url
    #connInstance.insertRepo(repo_url)
    connInstance.getRepoId(repo_url)
    clone_path = "./cloned_repo"
    try:
        clone_repo(repo_url, clone_path)
        functions_metadata, class_names = extract_functions_from_repo(clone_path)
        all_classes = []
        for root, _, files in os.walk(clone_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    classes = extract_classes_from_file(file_path)
                    all_classes.extend(classes)
        return {
            "class_names": list(set(all_classes)),
            "file_names": list(functions_metadata.keys()),
            "function_metadata": functions_metadata
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(clone_path):
            shutil.rmtree(clone_path, onerror=handle_remove_readonly)

# Run the application (uncomment the following lines if running as a script)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
