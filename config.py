# config.py
import os
from dotenv import load_dotenv

# Učitaj varijable iz .env datoteke u okolišne varijable sustava
load_dotenv()

# Dohvati token i prefiks iz okolišnih varijabli
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
PREFIX = os.getenv("BOT_PREFIX", "/") # Koristi "/" kao default ako nije postavljen u .env

# Provjeri je li token uopće postavljen
if BOT_TOKEN is None:
    raise ValueError("Greška: DISCORD_BOT_TOKEN nije postavljen u .env datoteci!")