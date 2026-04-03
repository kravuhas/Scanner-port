import asyncio
from itertools import islice
import socket
from typing import Any, Iterable, List, Tuple


class PortScan:
    MAX_CONCURRENT = 2000
    CHUNK_SIZE = 1000
    TIMEOUT = 1  # em segundos (era 1000 ms, agora é 1 segundo)

    def __init__(self, host: str, ports: List[int]) -> None:
        self.host = host
        self.ports = ports

    def _chunked(self, array: List[Any], size: int) -> Iterable[List[Any]]:
        """Divide a lista em chunks de tamanho específico"""
        it = iter(array)
        while True:
            chunk = list(islice(it, size))
            if not chunk:
                break
            yield chunk

    async def _port_scan(self, port: int, semaphore: asyncio.Semaphore) -> Tuple[str, int] | None:
        """Tenta conectar em uma porta específica"""
        loop = asyncio.get_running_loop()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)

        try:
            async with semaphore:
                await asyncio.wait_for(
                    loop.sock_connect(sock, (self.host, port)),
                    timeout=self.TIMEOUT
                )
            sock.close()
            return (self.host, port)

        except asyncio.TimeoutError:
            sock.close()
            return None
        except Exception:
            sock.close()
            return None

    async def _handle_scan(self) -> None:
        """Gerencia o scan de portas em chunks"""
        semaphore = asyncio.Semaphore(self.MAX_CONCURRENT)

        for port_chunk in self._chunked(self.ports, self.CHUNK_SIZE):
            tasks = [
                asyncio.create_task(self._port_scan(port, semaphore))
                for port in port_chunk
            ]

            for task in asyncio.as_completed(tasks):
                result = await task

                if result:
                    print(f"[+] {result[0]}:{result[1]}")

    def start(self) -> None:
        """Inicia o scan"""
        asyncio.run(self._handle_scan())


if __name__ == "__main__":
    # Exemplo de uso
    host = "127.0.0.1"  # localhost
    ports = list(range(1, 1025))  # portas 1-1024

    scanner = PortScan(host, ports)
    scanner.start()
