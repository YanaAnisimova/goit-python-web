import socket
import asyncio
import sys
from settings import *


async def client1(message, host, port):
    print(f'Connecting {host} / port {port}')

    reader, writer = await asyncio.open_connection(host, port) # limit=CHUNK_BYTES???
    writer.write(message.encode())
    writer.write(DELIMITER.encode())
    await writer.drain()

    print(f'Sent: {sys.getsizeof(message.encode())} bytes')

    data = await reader.readuntil(separator=DELIMITER.encode())

    print(f'Received: {data!r}')
    print('Close the connection')
    writer.close()


if __name__ == '__main__':

    data = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum. Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.'

    asyncio.run(client1(data, SERVER_HOST, SERVER_PORT))