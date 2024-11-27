import os
from dotenv import load_dotenv

load_dotenv()

STAGE = os.getenv("STAGE", "develop")

if STAGE == "develop":
    from .develop import *  # noqa
elif STAGE == "production":
    from .production import *  # noqa
