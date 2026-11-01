import json
from pathlib import Path

DATA_FOLDER = Path("data_dev")
DATA_FOLDER.mkdir(parents=True, exist_ok=True)
USERS_JSON = DATA_FOLDER / "users.json"


def load_users() -> dict:
    if not USERS_JSON.exists():
        USERS_JSON.write_text(str({}))
        return {}

    return json.loads(USERS_JSON.read_text("utf-8"))


def append_user(fiscal_number: str, name: str):
    USERS_JSON.write_text(
        json.dumps(
            json.loads(USERS_JSON.read_text("utf-8")) | {fiscal_number: name}, indent=4
        )
    )
