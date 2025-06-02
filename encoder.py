import base64
import json
from pathlib import Path
from settings import SAVE_FILE_PATH, DECODED_JSON_PATH
from utils import print_success, print_error


def encode_save_file() -> bool:
    try:
        input_path = Path(DECODED_JSON_PATH)
        if not input_path.exists():
            print_error("Decoded file not found.")
            return False

        with open(input_path, "r") as file:
            json_obj = json.load(file)
            encoded_str = json.dumps(json_obj)
            encoded_bytes = base64.b64encode(encoded_str.encode("utf-8"))

        with open(SAVE_FILE_PATH, "wb") as output_file:
            output_file.write(b'60z,')  # Prefix required for the game
            output_file.write(encoded_bytes)

        print_success("Re-encoded and saved as '.sf' file.")
        return True

    except Exception as e:
        print_error(f"Encoding failed: {e}")
        return False