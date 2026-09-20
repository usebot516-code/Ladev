import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from discord import app_commands
from discord.ext import commands

# 1. SERVIDOR HTTP PARA O RENDER (Corrige o erro de Port Scan)
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(b"<h1>Bot Discord Online no Render 24/7!</h1><p>Comando ativo: /ping</p>")

    def log_message(self, format, *args):
        return

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    httpd = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    print(f"[RENDER] Servidor HTTP ativo na porta {port}!")
    httpd.serve_forever()

threading.Thread(target=run_web_server, daemon=True).start()

# 2. BOT DISCORD COM SLASH COMMAND /ping
intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        print("[SISTEMA] Sincronizando /ping...")
        await self.tree.sync()
        print("[SISTEMA] Comandos sincronizados!")

bot = MyBot()

@bot.event
async def on_ready():
    print(f"[ONLINE] Conectado como {bot.user.name}!")
    await bot.change_presence(activity=discord.Game(name="/ping | Online 24/7"))

@bot.tree.command(name="ping", description="Verifica a latencia do bot")
async def ping_slash(interaction: discord.Interaction):
    latencia_ms = round(bot.latency * 1000)
    await interaction.response.send_message(
        f"🏓 **Pong!**\n⏱️ Latência: {latencia_ms}ms\n☁️ Hospedagem: Render Web Service\n🔒 *(Apenas você pode ver isso)*",
        ephemeral=True
    )

@bot.command(name="ping")
async def ping_prefix(ctx):
    latencia_ms = round(bot.latency * 1000)
    await ctx.reply(f"🏓 Pong! Latência: {latencia_ms}ms")

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("[ERRO] DISCORD_TOKEN nao configurado no Render!")
        exit(1)
    bot.run(token)
