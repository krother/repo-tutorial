import os
from pathlib import Path
from dotenv import load_dotenv

BASE_PATH = Path(__file__).parent
load_dotenv(dotenv_path=BASE_PATH.parent / ".env", override=True, verbose=True)

DATA_PATH = BASE_PATH.parent / "data"

LANG = os.getenv("LANG")
