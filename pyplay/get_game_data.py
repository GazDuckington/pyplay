import os, json, shutil
from subprocess import PIPE, run

GAME_DIR_PATTERN: str = "game"
GAME_GO_EXT: str = ".go"
GO_COMPILE_CMD: list = ["go", "build"]

def find_all_game_dirs(source):
    game_paths: list = []
    for _, dirs, _ in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)
        break
    
    return game_paths

def get_name_from_path(paths, to_strip):
    new_names: list = []
    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)

    return new_names

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def copy_or_overwrite(source, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(source, dest)

def make_json_metadata(path, game_dirs):
    data = {
        "gameTitles": game_dirs,
        "numberOfGames": len(game_dirs)
    }
    with open(path, "w")as f:
        json.dump(data, f)

def compile_go_code(path):
    code_file_name = None
    for _, _, files in os.walk(path):
        for file in files:
            if file.endswith(GAME_GO_EXT):
                code_file_name = file
                break
        break
    
    if code_file_name is None:
        return

    command = GO_COMPILE_CMD + [code_file_name] 
    run_cmd(command, path)

def run_cmd(cmd, path):
    cwd = os.getcwd()
    os.chdir(path)

    result = run(cmd, stdout=PIPE, stdin=PIPE, universal_newlines=True)
    print(result)

    os.chdir(cwd)

def main(source, target):
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)
    
    game_paths = find_all_game_dirs(source_path)
    new_game_dirs = get_name_from_path(game_paths, f"_{GAME_DIR_PATTERN}")

    create_dir(target_path)

    for src, dest in zip(game_paths, new_game_dirs):
        dest_path = os.path.join(target_path, dest)
        copy_or_overwrite(src, dest_path)
        compile_go_code(dest_path)

    json_path = os.path.join(target_path, "metadata.json")
    make_json_metadata(json_path, new_game_dirs)

if __name__ == "__main__":
    # args = sys.argv
    # if len(args) != 3:
    #     raise ValueError("Please pass a source and target directory")
    #
    # source, target = args[1:]
    # main(source, target)
    print('hellow')
