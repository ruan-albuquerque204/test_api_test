import os
import json
from pathlib import Path

from dotenv import load_dotenv

from . import utils

load_dotenv()

DATA_FOLDER = Path(os.getenv("DATA_FOLDER", "data"))
USERS_JSON = DATA_FOLDER / "users.json"
DEBITS_JSON = DATA_FOLDER / "debits.json"

DATA_FOLDER.mkdir(parents=True, exist_ok=True)


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

    create_debit(fiscal_number)


def load_debits() -> dict | None:
    if not DEBITS_JSON.exists():
        return {}

    return json.loads(DEBITS_JSON.read_text("utf-8"))


def create_debit(fiscal_number: str):
    debits = {}
    if DEBITS_JSON.exists():
        try:
            debits: dict = json.loads(DEBITS_JSON.read_text("utf-8"))
        except:
            pass

    new_debits = utils.create_debit(10)

    DEBITS_JSON.write_text(json.dumps(debits | {fiscal_number: new_debits}, indent=4))

    return new_debits
