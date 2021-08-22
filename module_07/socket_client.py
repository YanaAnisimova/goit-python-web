import socket
import sys
from settings import *


def client(host, port, chunk_bytes, delimiter):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port+1))
        print(f'Connecting {host} / port {port}')
        data = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum. Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.'
        s.connect((host, port))
        s.sendall(data.encode())
        print(f'Sent: {sys.getsizeof(data.encode())} bytes')
        s.send(delimiter.encode())
        while True:
            resp = s.recv(chunk_bytes)
            print(f'Received: {resp.decode()}')
            if resp == delimiter.encode() or not resp:
                break


if __name__ == '__main__':
    client(SERVER_HOST, SERVER_PORT, CHUNK_BYTES, DELIMITER)