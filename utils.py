from json import load


def read_json_file(file_path: str):
    with open(file_path) as f:
        json_file = load(f)
    return json_file
