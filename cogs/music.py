# cogs/music.py - VERZIJA S MAKSIMALNIM BROJEM LOGOVA

import discord
from discord.ext import commands
import yt_dlp
import asyncio
import traceback # Uvozimo za detaljan ispis grešaka

# --- Postavke ---
YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

# --- Glavni Cog ---
class MusicCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.queues = {}  # Rječnik za redove pjesama -> {guild_id: [url1, url2, ...]}

    def get_queue(self, ctx: commands.Context):
        if ctx.guild.id not in self.queues:
            print(f"[QUEUE] Kreiram novi red za server: {ctx.guild.name}")
            self.queues[ctx.guild.id] = []
        return self.queues[ctx.guild.id]

    async def play_music_loop(self, ctx: commands.Context):
        print(f"[LOOP] Petlja za sviranje pokrenuta za server: {ctx.guild.name}")
        queue = self.get_queue(ctx)
        
        while len(queue) > 0:
            print(f"[LOOP] Veličina reda na početku petlje: {len(queue)}")
            try:
                vc_status = ctx.voice_client.is_connected() if ctx.voice_client else False
                print(f"[LOOP] Provjeravam voice client. Povezan: {vc_status}")
                if not vc_status:
                    print("[LOOP] Voice client nije spojen! Prekidam petlju.")
                    if ctx.guild.id in self.queues:
                        del self.queues[ctx.guild.id]
                    return

                url = queue.pop(0)
                print(f"[LOOP] Uzimam URL iz reda: {url}")

                async with ctx.typing():
                    print("[LOOP] Zovem create_source...")
                    player = await self.create_source(url)
                    print("[LOOP] Izvor uspješno kreiran.")
                
                print("[LOOP] Pokrećem voice_client.play()...")
                ctx.voice_client.play(player, after=lambda e: print(f"--- [CALLBACK] Player error: {e} ---") if e else print("--- [CALLBACK] Pjesma završila (after) ---"))
                
                await ctx.send(embed=discord.Embed(title="▶️ Sada svira", description=player.title, color=discord.Color.green()))
                print(f"[LOOP] Poslana poruka 'Sada svira': {player.title}")

                print("[LOOP] Ulazim u 'while is_playing' petlju. Čekam da pjesma završi.")
                while ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                    await asyncio.sleep(1)
                print("[LOOP] Izašao iz 'while is_playing' petlje.")
            
            except Exception as e:
                print(f"!!!!!! [LOOP] Neočekivana greška u petlji za sviranje !!!!!!")
                print(traceback.format_exc()) # Ispisuje cijeli trag greške
                await ctx.send(f"Došlo je do greške: {e}")
                continue # Pokušaj sa sljedećom pjesmom
        
        print("[LOOP] Red je prazan. Pokrećem timer za izlazak (120s)...")
        await asyncio.sleep(120)
        
        vc_status = ctx.voice_client and ctx.voice_client.is_connected()
        playing_status = ctx.voice_client.is_playing() if vc_status else False
        print(f"[LOOP] Timer istekao. Povezan: {vc_status}, Svira: {playing_status}")
        
        if vc_status and not playing_status:
            print("[LOOP] Bot ne svira i timer je istekao. Diskonektiram.")
            await ctx.voice_client.disconnect()

    @classmethod
    async def create_source(cls, url: str) -> discord.PCMVolumeTransformer:
        print(f"[SOURCE] Kreiram izvor za URL: {url}")
        with yt_dlp.YoutubeDL(YTDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        print("[SOURCE] Dobiven info od yt-dlp.")
        
        if 'entries' in info:
            info = info['entries'][0]
        
        audio_url = info['url']
        source = discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS)
        
        player = discord.PCMVolumeTransformer(source, volume=0.5)
        player.title = info.get('title', 'Nepoznat naslov')
        print(f"[SOURCE] Kreiran player s naslovom: {player.title}")
        return player

    @commands.command(name='p', aliases=['play'])
    async def play(self, ctx: commands.Context, *, query: str):
        print("\n" + "="*50)
        print(f"[PLAY] Komanda pozvana od: {ctx.author} | Query: '{query}'")
        queue = self.get_queue(ctx)

        if not ctx.author.voice:
            print("[PLAY] Korisnik NIJE u glasovnom kanalu. Prekidam.")
            return await ctx.send("Moraš biti u glasovnom kanalu da bi pustio glazbu.")

        if not ctx.voice_client:
            print("[PLAY] Voice client ne postoji. Pokušavam se spojiti...")
            await ctx.author.voice.channel.connect()
            print("[PLAY] Uspješno spojen.")

        async with ctx.typing():
            try:
                if "list=" in query:
                    print("[PLAY] Prepoznat 'list=' u query-ju. Obrađujem kao playlistu.")
                    with yt_dlp.YoutubeDL({'extract_flat': True, 'quiet': True}) as ydl:
                        info = ydl.extract_info(query, download=False)
                    if 'entries' in info:
                        count = len(info['entries'])
                        for entry in info['entries']:
                            if entry.get('url'):
                                queue.append(entry['url'])
                        print(f"[PLAY] Playlista obrađena. Dodano {count} pjesama. Veličina reda: {len(queue)}")
                        await ctx.send(f"✅ Dodano **{count}** pjesama iz playliste u red.")
                else:
                    print("[PLAY] Obrađujem kao pojedinačnu pjesmu/pretragu.")
                    with yt_dlp.YoutubeDL(YTDL_OPTIONS) as ydl:
                        info = ydl.extract_info(f"ytsearch1:{query}", download=False)
                    if not info or not info.get('entries'):
                        print("[PLAY] Pretraga nije vratila rezultate.")
                        return await ctx.send("Nisam uspio pronaći pjesmu.")
                    
                    song = info['entries'][0]
                    queue.append(song['webpage_url'])
                    print(f"[PLAY] Pjesma pronađena i dodana: {song['title']}. Veličina reda: {len(queue)}")
                    await ctx.send(embed=discord.Embed(title="✅ Dodano u red", description=f"[{song['title']}]({song['webpage_url']})", color=discord.Color.blue()))
            except Exception as e:
                print("!!!!!! [PLAY] Neočekivana greška prilikom pretrage !!!!!!")
                print(traceback.format_exc())
                return await ctx.send(f"Došlo je do greške prilikom pretrage: {e}")

        vc_playing = ctx.voice_client.is_playing()
        print(f"[PLAY] Provjeravam svira li bot... Rezultat: {vc_playing}")
        if not vc_playing:
            print("[PLAY] Bot ne svira. Kreiram novi zadatak 'play_music_loop'.")
            self.bot.loop.create_task(self.play_music_loop(ctx))
        else:
            print("[PLAY] Bot već svira. Pjesma je samo dodana u red.")

    @commands.command(name='skip', aliases=['s'])
    async def skip(self, ctx: commands.Context):
        print("\n" + "="*50)
        print(f"[SKIP] Komanda pozvana od: {ctx.author}")
        if ctx.voice_client and ctx.voice_client.is_playing():
            print("[SKIP] Zaustavljam player...")
            ctx.voice_client.stop()
            await ctx.message.add_reaction('⏭️')
        else:
            print("[SKIP] Bot ne svira ili nije spojen. Ignoriram komandu.")

    @commands.command(name='stop')
    async def stop(self, ctx: commands.Context):
        print("\n" + "="*50)
        print(f"[STOP] Komanda pozvana od: {ctx.author}")
        if ctx.voice_client:
            queue = self.get_queue(ctx)
            print("[STOP] Čistim red...")
            queue.clear()
            if ctx.voice_client.is_playing():
                print("[STOP] Zaustavljam player...")
                ctx.voice_client.stop()
            print("[STOP] Diskonektiram...")
            await ctx.voice_client.disconnect()
            await ctx.message.add_reaction('⏹️')
        else:
            print("[STOP] Bot nije spojen. Ignoriram komandu.")

async def setup(bot: commands.Cog):
    await bot.add_cog(MusicCog(bot))