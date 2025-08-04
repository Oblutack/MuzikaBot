# MuzikaBot 🎶

Jednostavan, ali moćan Discord glazbeni bot napravljen u Pythonu koristeći `discord.py`. Bot može puštati pjesme i playliste s YouTubea, preskakati pjesme i još mnogo toga.

## Značajke ✨

-   **Puštanje glazbe s YouTubea:** Pustite bilo koju pjesmu koristeći pretragu ili direktan link.
-   **Podrška za playliste:** Dodajte cijele YouTube playliste u red jednim potezom.
-   **Upravljanje redom:** Jednostavne komande za preskakanje (`/skip`) i zaustavljanje (`/stop`) glazbe.
-   **Jednostavnost korištenja:** Intuitivne komande dizajnirane za brz i lak pristup.
-   **Hosting-Ready:** Spreman za postavljanje (deployment) na platforme poput Render.com.

## Komande 🤖

Glavne komande koje bot trenutno podržava:

-   `/p [ime pjesme ili YouTube link]` - Pušta pjesmu ili je dodaje u red. Također radi i za playliste.
-   `/skip` - Preskače trenutnu pjesmu i pušta sljedeću iz reda.
-   `/stop` - Zaustavlja glazbu, čisti cijeli red i izbacuje bota iz glasovnog kanala.

## Postavljanje i pokretanje 🚀

Za pokretanje ovog bota, slijedite ove korake:

### 1. Preduvjeti

-   [Python 3.8+](https://www.python.org/downloads/)
-   [FFmpeg](https://ffmpeg.org/download.html) (mora biti dodan u sistemski PATH)

### 2. Kloniranje repozitorija

```bash
git clone https://github.com/[VašeGitHubKorisničkoIme]/[ImeRepozitorija].git
cd [ImeRepozitorija]

### 3. Instalacija ovisnosti

pip install -r requirements.txt

### 4. Konfiguracija

Bot zahtijeva tajni token za spajanje na Discord. Postavite "Secret" / "Environment" varijablu na vašoj hosting platformi (npr. Render, Replit):
- DISCORD_BOT_TOKEN: Vaš tajni bot token s Discord Developer Portala.
