from settings import *
import socket
import sys


def server(host,
           port,
           max_number_of_connections,
           chunk_bytes,
           delimiter):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        print(f'SERVER HOST: {SERVER_HOST}')
        print(f'Listen {host} / port {port}')
        s.listen(max_number_of_connections)
        while True:
            conn, addr = s.accept()
            print(f'Connected by {addr}')

            with conn:
                message = []

                while True:
                    data = conn.recv(chunk_bytes)
                    if data.endswith(delimiter.encode()):
                        message.append(data.replace(delimiter.encode(), b''))
                        break
                    elif not data:
                        break

                    message.append(data)

                message = b''.join(message)
                # print(f'Message: {message.decode()}')
                print(f'Received: {sys.getsizeof(message)} bytes')
                conn.send(delimiter.encode())
                print(f'Sent delimiter: {delimiter}')


if __name__ == '__main__':

    server(LISTENING_SERVER_HOST,
           SERVER_PORT,
           MAX_NUMBER_OF_CONNECTIONS,
           CHUNK_BYTES,
           DELIMITER)
