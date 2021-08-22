from settings import *
import socket
import sys
import asyncio


async def handle_client_connections(reader, writer):
    addr = writer.get_extra_info('peername')

    print(f'\nConnected by {addr}')

    data = b''
    while not reader.at_eof():
        chunk = await reader.read(CHUNK_BYTES)
        # print(f'Read {addr}: {chunk}')
        if not chunk:
            break
        elif chunk.endswith(DELIMITER.encode()):
            data += chunk.replace(DELIMITER.encode(), b'')
            break
        data += chunk

    print(f"Received {addr}: {sys.getsizeof(data)} bytes")
    print(f"Send delimiter {addr}: {DELIMITER!r}")

    writer.write(DELIMITER.encode())
    await writer.drain()

    print(f"Close the connection {addr}")
    writer.close()


async def main(host, port, max_number_of_connections):
    server = await asyncio.start_server(handle_client_connections,
                                        host,
                                        port,
                                        backlog=max_number_of_connections,) # limit=CHUNK_BYTES???

    print(f'SERVER HOST: {SERVER_HOST}')
    print(f'Listen {host} / port {port}')

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main(LISTENING_SERVER_HOST, SERVER_PORT, MAX_NUMBER_OF_CONNECTIONS))

