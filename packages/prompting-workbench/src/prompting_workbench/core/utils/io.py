import json
import os
from collections.abc import Iterator


def get_file_content(file_path):
    with open(file_path) as f:
        file_content = f.read()

    return file_content


def get_json_content(file_path):
    return json.load(open(file_path))


def write_file(file_path, content):
    with open(file_path, "w") as f:
        f.write(content)
    # print(f'[DEBUG] Wrote "{file_path}" successfully!')


def append_file(file_path, content):
    with open(file_path, "a+") as f:
        f.write(content)


def walk_dir_files(folder_path: str) -> Iterator[tuple[str, str]]:
    if not os.path.exists(folder_path):
        raise ValueError(f"Folder {folder_path} does not exist")

    for root, _subdirs, files in os.walk(folder_path):
        for file_name in files:
            yield root, file_name


def encode_file_to_base64(file_path: str) -> str:
    import base64

    if file_path.startswith("http://") or file_path.startswith("https://"):
        import requests

        response = requests.get(file_path)
        return base64.b64encode(response.content).decode("utf-8")

    if file_path.startswith("file://"):
        file_path = file_path.replace("file://", "")

    with open(file_path, "rb") as file_file:
        return base64.b64encode(file_file.read()).decode("utf-8")


def decode_base64_to_file(base64_string, file_path):
    import base64

    with open(file_path, "wb") as file_file:
        file_file.write(base64.b64decode(base64_string))


def guess_mimetype(file_path: str) -> str | None:
    """
    Guess the MIME type of a file based on its filename or URL. It can handle local files and Remote URLs.

    Parameters:
    file_path (str): The path to the file for which the MIME type is to be guessed.

    Returns:
    str: The guessed MIME type of the file, or None if the type cannot be determined.
    """
    if file_path.startswith("http://") or file_path.startswith("https://"):
        import requests

        response = requests.head(file_path)
        return response.headers.get("Content-Type")

    import mimetypes

    guess_file_path = file_path
    if file_path.startswith("file://"):
        guess_file_path = file_path.replace("file://", "")

    mime_type, _encoding = mimetypes.guess_type(guess_file_path)
    return mime_type
