import base64
import json
from pathlib import Path
from settings import SAVE_FILE_PATH, DECODED_JSON_PATH
from utils import print_success, print_error


def decode_save_file() -> bool:
    try:
        input_path = Path(SAVE_FILE_PATH)
        if not input_path.exists():
            print_error(f"Save file not found at {SAVE_FILE_PATH}")
            return False

        with open(input_path, "r") as file:
            raw_data = file.read()[4:]  # Skip the decryption block (e.g., '60z,')
            decoded_bytes = base64.b64decode(raw_data)
            decoded_str = decoded_bytes.decode("utf-8")
            json_obj = json.loads(decoded_str)

        Path(DECODED_JSON_PATH).parent.mkdir(parents=True, exist_ok=True)
        with open(DECODED_JSON_PATH, "w") as json_file:
            json.dump(json_obj, json_file, indent=4)

        print_success("Decoded and saved to 'data/cg_save.json'")
        return True

    except Exception as e:
        print_error(f"Decoding failed: {e}")
        return False