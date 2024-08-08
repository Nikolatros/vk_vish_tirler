from os import getenv
from dotenv import load_dotenv


# Load secret variables
load_dotenv()

TOKEN_USER = getenv("USER_TOKEN")
OWNER_ID = getenv("OWNER_ID")
VERSION = getenv("VERSION")
POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
POSTGRES_DB = getenv("POSTGRES_DB")
