# main.py
import discord
from discord.ext import commands
import asyncio
import os
from config import BOT_TOKEN, PREFIX

# --- Osnovne postavke bota ---

# Definiramo "Intents" (namjere) koje bot koristi.
# One govore Discordu koje vrste događaja naš bot želi pratiti.
intents = discord.Intents.default()
intents.message_content = True  # Omogućuje čitanje sadržaja poruka za komande
intents.guilds = True           # Omogućuje praćenje servera (guilds)
intents.voice_states = True     # Omogućuje praćenje tko je u kojem glasovnom kanalu

# Kreiramo instancu bota s definiranim prefiksom i intentima
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None) # help_command=None za kasniju custom help komandu

# --- Događaji (Events) ---

# Događaj koji se aktivira kada je bot uspješno spojen i spreman za rad
@bot.event
async def on_ready():
    print(f'Bot je online kao {bot.user}')
    print(f'ID Bota: {bot.user.id}')
    print('--------------------')
    # Postavi status bota, npr. "Sluša /p"
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{PREFIX}p"))

# --- Funkcije za učitavanje ---

# Asinkrona funkcija koja će učitati sve naše module s komandama (Cogs)
async def load_cogs():
    # Prolazi kroz svaku datoteku u 'cogs' direktoriju
    for filename in os.listdir('./cogs'):
        # Učitaj samo .py datoteke koje NISU __init__.py
        if filename.endswith('.py') and not filename.startswith('__'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"✅ Učitan cog: {filename[:-3]}")

# --- Glavna funkcija za pokretanje ---

async def main():
    # Koristimo 'async with' da osiguramo pravilno spajanje i odspajanje bota
    async with bot:
        await load_cogs()
        await bot.start(BOT_TOKEN)

# Pokretanje glavne funkcije kada se skripta izvrši
if __name__ == "__main__":
    try:
        # asyncio.run() pokreće asinkroni 'main' program
        asyncio.run(main())
    except KeyboardInterrupt:
        # Omogućuje gašenje bota s Ctrl+C u terminalu
        print("\nBot se gasi.")