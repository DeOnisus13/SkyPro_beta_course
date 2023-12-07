from pathlib import Path

ROOT_PATH = Path(__file__).parent
XLS_FILE_PATH = Path.joinpath(ROOT_PATH, "data", "operations.xls")
USER_SETTINGS_PATH = Path.joinpath(ROOT_PATH, "data", "user_settings.json")
JSON_OUT_PATH = Path.joinpath(ROOT_PATH, "data", "output_json.json")
